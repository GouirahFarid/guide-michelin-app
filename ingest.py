"""
Data ingestion script for Michelin restaurant CSV data.

Optimized with streaming batches and checkpointing for resume capability.
"""
import asyncio
import csv
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Set

import pandas as pd
from tqdm import tqdm

from config import get_settings
from database import (
    init_database,
    batch_insert_restaurants,
    batch_insert_embeddings,
    get_connection,
    close_pool
)
from embeddings import get_cached_embeddings

# Windows event loop fix for psycopg async
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

settings = get_settings()


# ============================================================================
# INGESTION CONFIG
# ============================================================================

@dataclass
class IngestConfig:
    """Configuration for data ingestion."""
    csv_path: str = "michelin_my_maps.csv"
    chunk_size: int = 500
    chunk_overlap: int = 50
    batch_size: int = 32  # Embedding batch size
    batch_stream_size: int = 500  # Restaurants per stream batch
    skip_existing: bool = True
    create_embeddings: bool = True
    resume: bool = True  # Auto-resume from progress file
    progress_file: str = "data/ingestion_progress.json"


# ============================================================================
# PROGRESS TRACKING
# ============================================================================

@dataclass
class IngestProgress:
    """Progress tracking for ingestion."""
    started_at: str
    last_update: str
    csv_path: str
    last_processed_index: int
    processed_count: int
    total_count: int
    restaurants_added: int
    embeddings_created: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "started_at": self.started_at,
            "last_update": self.last_update,
            "csv_path": self.csv_path,
            "last_processed_index": self.last_processed_index,
            "processed_count": self.processed_count,
            "total_count": self.total_count,
            "restaurants_added": self.restaurants_added,
            "embeddings_created": self.embeddings_created,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IngestProgress":
        return cls(**data)

    def save(self, path: str) -> None:
        """Save progress to file."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str) -> Optional["IngestProgress"]:
        """Load progress from file."""
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            data = json.load(f)
            return cls.from_dict(data)

    def delete(self, path: str) -> None:
        """Delete progress file."""
        if os.path.exists(path):
            os.remove(path)


async def get_processed_names() -> Set[str]:
    """Get set of restaurant names already in database."""
    async with get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT name FROM restaurants")
            rows = await cur.fetchall()
            return {row[0] for row in rows}


# ============================================================================
# CSV LOADING
# ============================================================================

def load_csv_in_batches(csv_path: str, batch_size: int = 500):
    """Load CSV in batches for streaming.

    Args:
        csv_path: Path to CSV file
        batch_size: Number of rows per batch

    Yields:
        Tuple of (batch_index, list of restaurant dictionaries)
    """
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        batch = []
        batch_index = 0
        for row in reader:
            restaurant = {
                "name": row.get("Name", ""),
                "address": row.get("Address", ""),
                "location": row.get("Location", ""),
                "price": row.get("Price", ""),
                "cuisine": row.get("Cuisine", ""),
                "longitude": float(row["Longitude"]) if row.get("Longitude") else None,
                "latitude": float(row["Latitude"]) if row.get("Latitude") else None,
                "phone_number": row.get("PhoneNumber", ""),
                "url": row.get("Url", ""),
                "website_url": row.get("WebsiteUrl", ""),
                "award": row.get("Award", ""),
                "green_star": bool(int(row.get("GreenStar", 0))),
                "facilities_and_services": row.get("FacilitiesAndServices", ""),
                "description": row.get("Description", ""),
            }
            batch.append(restaurant)
            if len(batch) >= batch_size:
                yield batch_index, batch
                batch = []
                batch_index += 1
        if batch:
            yield batch_index, batch


def get_total_csv_rows(csv_path: str) -> int:
    """Get total number of rows in CSV (excluding header)."""
    with open(csv_path, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f) - 1  # Subtract header


# ============================================================================
# TEXT CHUNKING (OPTIMIZED)
# ============================================================================

def create_restaurant_chunks(
    restaurant: Dict[str, Any],
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> List[Dict[str, Any]]:
    """Create searchable text chunks from a restaurant.

    OPTIMIZED: Most descriptions are short enough to be single chunk.
    Only split if text exceeds chunk_size.
    """
    # Create searchable text combining all fields
    searchable_text_parts = []
    if restaurant.get("name"):
        searchable_text_parts.append(f"Name: {restaurant['name']}")
    if restaurant.get("cuisine"):
        searchable_text_parts.append(f"Cuisine: {restaurant['cuisine']}")
    if restaurant.get("award"):
        searchable_text_parts.append(f"Award: {restaurant['award']}")
    if restaurant.get("description"):
        searchable_text_parts.append(restaurant["description"])
    if restaurant.get("facilities_and_services"):
        searchable_text_parts.append(f"Facilities: {restaurant['facilities_and_services']}")

    searchable_text = " | ".join(searchable_text_parts)

    # Create metadata
    metadata = {
        "restaurant_name": restaurant.get("name"),
        "location": restaurant.get("location"),
        "cuisine": restaurant.get("cuisine"),
        "award": restaurant.get("award"),
        "price": restaurant.get("price"),
    }

    # OPTIMIZATION: Skip chunking if text is short enough (95% of cases)
    if len(searchable_text) <= chunk_size:
        return [{
            "text": searchable_text,
            "metadata": metadata,
        }]

    # Only chunk for long descriptions
    chunks = []
    start = 0
    text_length = len(searchable_text)

    while start < text_length:
        end = start + chunk_size

        # Try to break at sentence boundary
        if end < text_length:
            for delimiter in ['. ', '! ', '? ', '.\n', '!\n', '?\n']:
                last_delimiter = searchable_text.rfind(delimiter, start, end)
                if last_delimiter != -1:
                    end = last_delimiter + len(delimiter)
                    break

        chunk_text = searchable_text[start:end].strip()
        if chunk_text:
            chunks.append({
                "text": chunk_text,
                "metadata": metadata,
            })

        start = end - chunk_overlap if end < text_length else text_length

    return chunks


# ============================================================================
# MAIN STREAMING INGESTION
# ============================================================================

async def ingest_data(config: IngestConfig = None) -> Dict[str, Any]:
    """Main ingestion function with streaming and checkpointing.

    Args:
        config: Ingestion configuration

    Returns:
        Summary of ingestion results
    """
    config = config or IngestConfig()
    start_time = time.time()

    print("=" * 60)
    print("🍽️  Michelin Restaurant Data Ingestion (STREAMING)")
    print("=" * 60)
    print(f"📁 CSV Path: {config.csv_path}")
    print(f"🔧 Chunk Size: {config.chunk_size}, Overlap: {config.chunk_overlap}")
    print(f"📦 Stream Batch Size: {config.batch_stream_size}")
    print(f"🤖 Create Embeddings: {config.create_embeddings}")
    print(f"⏭️  Skip Existing: {config.skip_existing}")
    print(f"🔄 Resume: {config.resume}")
    print("-" * 60)

    # Initialize database
    print("📊 Initializing database...")
    await init_database()
    print("✅ Database initialized")

    # Load or initialize progress
    progress = None
    start_index = 0
    if config.resume:
        progress = IngestProgress.load(config.progress_file)
        if progress:
            print(f"🔄 Resuming from index {progress.last_processed_index}")
            start_index = progress.last_processed_index + 1

    # Get total count
    total_count = get_total_csv_rows(config.csv_path)
    print(f"📖 Total restaurants in CSV: {total_count}")

    # Get existing restaurant names
    processed_names: Set[str] = set()
    if config.skip_existing:
        print("🔍 Checking for existing restaurants...")
        processed_names = await get_processed_names()
        print(f"✅ Found {len(processed_names)} existing restaurants")

    # Initialize progress if not resuming
    if not progress:
        progress = IngestProgress(
            started_at=datetime.now().isoformat(),
            last_update=datetime.now().isoformat(),
            csv_path=config.csv_path,
            last_processed_index=-1,
            processed_count=0,
            total_count=total_count,
            restaurants_added=0,
            embeddings_created=0,
        )

    # Initialize embeddings once
    embeddings_obj = None
    if config.create_embeddings:
        print("🔢 Loading embedding model...")
        embeddings_obj = get_cached_embeddings()
        print("✅ Embedding model loaded")

    # Stream and process batches
    print("\n" + "=" * 60)
    print("🚀 STREAMING INGESTION")
    print("=" * 60)

    total_embeddings = 0
    errors = []

    for batch_index, batch in load_csv_in_batches(config.csv_path, config.batch_stream_size):
        current_index = batch_index * config.batch_stream_size

        # Skip if resuming and before start index
        if config.resume and current_index <= start_index:
            continue

        # Filter out already processed restaurants
        if config.skip_existing:
            new_batch = [r for r in batch if r.get("name") not in processed_names]
            skipped = len(batch) - len(new_batch)
            if skipped > 0:
                print(f"⏭️  Batch {batch_index}: Skipping {skipped} existing restaurants")
            batch = new_batch

        if not batch:
            continue

        # Process this batch
        print(f"\n📦 Batch {batch_index} ({current_index}-{current_index + len(batch)}): {len(batch)} new restaurants")

        try:
            # Step 1: Batch insert restaurants
            restaurant_ids = await batch_insert_restaurants(batch, batch_size=config.batch_stream_size)
            print(f"   ✅ Inserted {len(restaurant_ids)} restaurants")

            # Step 2: Create chunks (only for this batch, small memory)
            if config.create_embeddings:
                all_chunks_data = []
                for restaurant, restaurant_id in zip(batch, restaurant_ids):
                    chunks = create_restaurant_chunks(
                        restaurant,
                        chunk_size=config.chunk_size,
                        chunk_overlap=config.chunk_overlap
                    )
                    for chunk in chunks:
                        all_chunks_data.append((
                            restaurant_id,
                            chunk["text"],
                            chunk.get("metadata", {})
                        ))

                print(f"   ✂️  Created {len(all_chunks_data)} chunks")

                # Step 3: Batch generate embeddings
                chunk_texts = [data[1] for data in all_chunks_data]
                all_embeddings = []

                total_sub_batches = (len(chunk_texts) + config.batch_size - 1) // config.batch_size
                for i in range(0, len(chunk_texts), config.batch_size):
                    sub_batch_num = i // config.batch_size + 1
                    batch_texts = chunk_texts[i:i + config.batch_size]
                    print(f"      🔄 Embedding sub-batch {sub_batch_num}/{total_sub_batches} ({len(batch_texts)} texts)...", flush=True)
                    batch_embeddings = embeddings_obj.embed_documents(batch_texts)
                    all_embeddings.extend(batch_embeddings)

                print(f"   🔢 Generated {len(all_embeddings)} embeddings")

                # Step 4: Batch insert embeddings
                embeddings_with_ids = [
                    (data[0], data[1], embedding, data[2])
                    for data, embedding in zip(all_chunks_data, all_embeddings)
                ]

                await batch_insert_embeddings(
                    embeddings_with_ids,
                    batch_size=1000
                )
                print(f"   💾 Inserted {len(embeddings_with_ids)} embeddings")

                total_embeddings += len(embeddings_with_ids)
                progress.embeddings_created += len(embeddings_with_ids)

            # Update progress
            progress.last_processed_index = current_index + len(batch) - 1
            progress.processed_count += len(batch)
            progress.restaurants_added += len(restaurant_ids)
            progress.last_update = datetime.now().isoformat()
            progress.save(config.progress_file)

            # Progress bar
            percent = (progress.processed_count / total_count) * 100
            print(f"   📊 Progress: {progress.processed_count}/{total_count} ({percent:.1f}%)")

        except Exception as e:
            print(f"   ❌ Error processing batch {batch_index}: {e}")
            errors.append({
                "batch": batch_index,
                "error": str(e),
                "index": current_index
            })
            # Save progress before continuing
            progress.save(config.progress_file)
            continue

    # Complete
    duration = time.time() - start_time

    # Clean up progress file
    if not errors:
        progress.delete(config.progress_file)
        print("\n✅ Progress file deleted (completed successfully)")

    summary = {
        "status": "completed" if not errors else "completed_with_errors",
        "message": "Data ingestion completed",
        "restaurants_processed": progress.processed_count,
        "restaurants_added": progress.restaurants_added,
        "restaurants_skipped": len(processed_names) if config.skip_existing else 0,
        "restaurants_failed": 0,
        "embeddings_created": progress.embeddings_created,
        "errors": errors[:10],
        "duration_seconds": duration,
    }

    print("\n" + "=" * 60)
    print("📊 INGESTION SUMMARY")
    print("=" * 60)
    print(f"✅ Restaurants Processed: {summary['restaurants_processed']}")
    print(f"➕ Restaurants Added: {summary['restaurants_added']}")
    print(f"⏭️  Restaurants Skipped: {summary['restaurants_skipped']}")
    print(f"🔢 Embeddings Created: {summary['embeddings_created']}")
    print(f"⏱️  Duration: {duration:.2f} seconds")
    print(f"🚄 Speed: {summary['restaurants_processed']/duration:.1f} restaurants/second")

    if errors:
        print(f"\n⚠️  Errors: {len(errors)} batches failed")

    return summary


# ============================================================================
# VERIFY INGESTION
# ============================================================================

async def verify_ingestion() -> Dict[str, Any]:
    """Verify that data was ingested correctly."""
    from database import get_pool

    pool = await get_pool()

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            # Count restaurants
            await cur.execute("SELECT COUNT(*) FROM restaurants")
            restaurant_count = (await cur.fetchone())[0]

            # Count embeddings
            await cur.execute("SELECT COUNT(*) FROM restaurant_embeddings")
            embedding_count = (await cur.fetchone())[0]

            # Get award distribution
            await cur.execute("""
                SELECT award, COUNT(*) as count
                FROM restaurants
                GROUP BY award
                ORDER BY count DESC
            """)
            award_dist = await cur.fetchall()

            # Get location distribution
            await cur.execute("""
                SELECT location, COUNT(*) as count
                FROM restaurants
                GROUP BY location
                ORDER BY count DESC
                LIMIT 10
            """)
            location_dist = await cur.fetchall()

    return {
        "restaurant_count": restaurant_count,
        "embedding_count": embedding_count,
        "award_distribution": dict(award_dist),
        "top_locations": dict(location_dist),
    }


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

async def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Ingest Michelin restaurant data")
    parser.add_argument("--csv", default="michelin_my_maps.csv", help="Path to CSV file")
    parser.add_argument("--chunk-size", type=int, default=500, help="Chunk size for embeddings")
    parser.add_argument("--chunk-overlap", type=int, default=50, help="Chunk overlap")
    parser.add_argument("--batch-size", type=int, default=500, help="Stream batch size")
    parser.add_argument("--no-embeddings", action="store_true", help="Skip embedding creation")
    parser.add_argument("--no-resume", action="store_true", help="Don't resume from progress file")
    parser.add_argument("--force", action="store_true", help="Force re-ingest (skip existing=false)")
    parser.add_argument("--verify", action="store_true", help="Verify ingestion after completion")

    args = parser.parse_args()

    config = IngestConfig(
        csv_path=args.csv,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        batch_stream_size=args.batch_size,
        create_embeddings=not args.no_embeddings,
        resume=not args.no_resume,
        skip_existing=not args.force,
    )

    # Run ingestion
    summary = await ingest_data(config)

    # Verify if requested
    if args.verify:
        print("\n🔍 Verifying ingestion...")
        verification = await verify_ingestion()
        print(f"   Restaurants in DB: {verification['restaurant_count']}")
        print(f"   Embeddings in DB: {verification['embedding_count']}")

    # Close connection pool
    await close_pool()

    return summary


if __name__ == "__main__":
    asyncio.run(main())

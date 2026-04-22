"""
Main entry point for the MichelinBot RAG application.

Run this to start the FastAPI server.
"""
import os
import uvicorn
import asyncio
import sys

from config import get_settings
from database import init_database
from ingest import ingest_data, IngestConfig

settings = get_settings()

# Windows event loop fix for psycopg async
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def ensure_database():
    """Ensure database is initialized."""
    try:
        await init_database()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Database initialization: {e}")


async def check_data():
    """Check if data exists in database."""
    from database import get_pool, get_connection

    pool = await get_pool()
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT COUNT(*) FROM restaurants")
            count = (await cur.fetchone())[0]
            return count > 0


def is_interactive():
    """Check if running in an interactive terminal."""
    return sys.stdout.isatty() and sys.stdin.isatty()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="MichelinBot RAG Server")
    parser.add_argument("--host", default=settings.host, help="Host to bind to")
    parser.add_argument("--port", type=int, default=settings.port, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--ingest", action="store_true", help="Run data ingestion before starting")
    parser.add_argument("--verify", action="store_true", help="Verify data and exit")
    parser.add_argument("--start-after-ingest", action="store_true", help="Auto-start server after ingestion (non-interactive)")

    args = parser.parse_args()

    print("=" * 60)
    print("🍽️  MichelinBot - RAG Restaurant Recommendation System")
    print("=" * 60)

    # Handle verification mode
    if args.verify:
        print("🔍 Verifying installation...")
        asyncio.run(ensure_database())
        from ingest import verify_ingestion
        verification = asyncio.run(verify_ingestion())
        print(f"\n📊 Database Contents:")
        print(f"   Restaurants: {verification['restaurant_count']}")
        print(f"   Embeddings: {verification['embedding_count']}")
        print(f"\n🏆 Award Distribution:")
        for award, count in verification['award_distribution'].items():
            print(f"   {award}: {count}")
        return

    # Handle ingestion mode
    if args.ingest:
        print("📥 Starting data ingestion...")
        asyncio.run(ensure_database())
        config = IngestConfig()
        summary = asyncio.run(ingest_data(config))
        print(f"\n✅ Ingestion complete!")
        print(f"   Restaurants: {summary['restaurants_added']}")
        print(f"   Embeddings: {summary['embeddings_created']}")

        # Auto-start if flag is set
        if args.start_after_ingest:
            print("\n🚀 Starting server...")
        # Interactive prompt only if in interactive mode
        elif is_interactive():
            try:
                response = input("\n🚀 Start server now? (y/n): ")
                if response.lower() != 'y':
                    return
            except (EOFError, KeyboardInterrupt):
                print("\nNon-interactive mode detected. Exiting after ingestion.")
                return
        else:
            # Non-interactive mode (Docker), just exit after ingestion
            print("\nIngestion complete. Use --start-after-ingest flag to auto-start server.")
            return

    # Ensure database is ready
    print("🔧 Initializing...")
    asyncio.run(ensure_database())

    # Check if data exists
    has_data = asyncio.run(check_data())
    if not has_data:
        print("\n⚠️  WARNING: No restaurant data found in database!")
        print("   Run with --ingest flag to load data:")
        print("   python main.py --ingest")
        print("")

        if is_interactive():
            try:
                response = input("Start server anyway? (y/n): ")
                if response.lower() != 'y':
                    print("Exiting. Run 'python main.py --ingest' first.")
                    return
            except (EOFError, KeyboardInterrupt):
                print("\nNon-interactive mode detected. Exiting.")
                return
        else:
            # In Docker/Ci, just start anyway (might be testing)
            print("Starting server anyway (non-interactive mode)...")

    print("\n" + "=" * 60)
    print("🚀 Starting Server")
    print("=" * 60)
    print(f"   Host: {args.host}")
    print(f"   Port: {args.port}")
    print(f"   Docs: http://{args.host}:{args.port}/docs")
    print(f"   Health: http://{args.host}:{args.port}/health")
    print("=" * 60)
    print("\n🍽️  MichelinBot is ready! Ask about restaurants:")
    print("   - '3-star restaurants in Munich'")
    print("   - 'Japanese fine dining with great views'")
    print("   - 'Romantic restaurants under €€€€'")
    print("\n")

    # Start server
    uvicorn.run(
        "app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()

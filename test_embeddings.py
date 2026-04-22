"""
Test script to verify embeddings work correctly.

Run this with: python test_embeddings.py
"""
import sys
import time
import os

# Set UTF-8 encoding for Windows
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"


def test_embeddings():
    """Test embedding generation."""
    print("[TEST] Testing Embeddings...")
    print("-" * 50)

    try:
        # Import after print so we see progress
        from embeddings import get_cached_embeddings

        print("[LOAD] Loading embedding model (this may take a minute)...")
        start = time.time()

        embeddings = get_cached_embeddings()

        load_time = time.time() - start
        print(f"[OK] Model loaded in {load_time:.2f} seconds")

        # Test single embedding
        print("\n[TEST] Testing single query embedding...")
        test_query = "Japanese fine dining in Munich"
        start = time.time()
        vector = embeddings.embed_query(test_query)
        elapsed = time.time() - start

        print(f"[OK] Query embedded in {elapsed:.4f} seconds")
        print(f"     Vector dimension: {len(vector)}")
        print(f"     First 5 values: {vector[:5]}")

        # Test batch embeddings
        print("\n[TEST] Testing batch embeddings (5 documents)...")
        test_docs = [
            "A 3-star restaurant in Munich with Japanese cuisine",
            "Creative French dining in Paris with great views",
            "Traditional Italian pasta in Rome",
            "Modern sushi restaurant in Tokyo",
            "German cuisine in Berlin",
        ]
        start = time.time()
        vectors = embeddings.embed_documents(test_docs)
        elapsed = time.time() - start

        print(f"[OK] Batch embedded in {elapsed:.4f} seconds")
        print(f"     Documents processed: {len(vectors)}")
        print(f"     Each vector dimension: {len(vectors[0])}")

        # Test similarity
        print("\n[TEST] Testing cosine similarity...")
        from embeddings import cosine_similarity

        similarity = cosine_similarity(vectors[0], vectors[1])
        print(f"     Similarity between doc 1 and 2: {similarity:.4f}")

        similarity2 = cosine_similarity(vectors[0], vectors[0])
        print(f"     Similarity between doc 1 and itself: {similarity2:.4f}")

        print("\n" + "=" * 50)
        print("[SUCCESS] All tests passed!")
        print("=" * 50)

        return True

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_chunking():
    """Test text chunking."""
    print("\n[TEST] Testing Text Chunking...")
    print("-" * 50)

    from ingest import create_restaurant_chunks, chunk_text

    # Sample restaurant data
    sample_restaurant = {
        "name": "Test Restaurant",
        "cuisine": "Modern French",
        "award": "3 Stars",
        "description": "A wonderful restaurant with exceptional food and service. The chef creates amazing dishes using local ingredients combined with international flavors. Guests can enjoy a beautiful view of the garden while dining.",
        "facilities_and_services": "Terrace, private dining",
        "location": "Paris, France",
        "price": "€€€€",
    }

    chunks = create_restaurant_chunks(sample_restaurant, chunk_size=500, chunk_overlap=50)

    print(f"[OK] Created {len(chunks)} chunks")
    for i, chunk in enumerate(chunks, 1):
        print(f"\n     Chunk {i} ({len(chunk['text'])} chars):")
        print(f"     {chunk['text'][:100]}...")

    return len(chunks) > 0


if __name__ == "__main__":
    # Run tests
    success = test_embeddings()

    if success:
        test_chunking()
        print("\n[SUCCESS] All tests completed successfully!")
        print("\n[INFO] The embeddings system is working correctly.")
        print("       You can now run the full ingestion:")
        print("       docker compose --profile ingest up ingest")
    else:
        print("\n[ERROR] Tests failed. Please check the error messages above.")
        sys.exit(1)

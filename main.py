"""
Main entry point for the MichelinBot LLM-Only application.

Run this to start the FastAPI server.
"""
import os
import uvicorn
import sys

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from config import get_settings

settings = get_settings()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="MichelinBot LLM-Only Server")
    parser.add_argument("--host", default=settings.host, help="Host to bind to")
    parser.add_argument("--port", type=int, default=settings.port, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    args = parser.parse_args()

    print("=" * 60)
    print("[MichelinBot] - LLM-Only Restaurant Recommendation")
    print("=" * 60)
    print("Mode: LLM Direct (No Database)")
    print("=" * 60)
    print("\n[Starting Server]")
    print("=" * 60)
    print(f"   Host: {args.host}")
    print(f"   Port: {args.port}")
    print(f"   Docs: http://{args.host}:{args.port}/docs")
    print(f"   Health: http://{args.host}:{args.port}/health")
    print("=" * 60)
    print("\n[MichelinBot] Ready! Ask about restaurants:")
    print("   - 'Best 3-star restaurants'")
    print("   - 'Romantic dinner recommendations'")
    print("   - 'Japanese fine dining'")
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

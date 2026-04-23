"""
Main entry point for the MichelinBot LLM-Only application.

Run this to start the FastAPI server.
"""
import os
import uvicorn
import sys
import logging

# Configure logging before imports
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    # Enable debug logging if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    logger.info("=" * 60)
    logger.info("[MichelinBot] - AI Restaurant Recommendation")
    logger.info("=" * 60)
    logger.info("Mode: LangGraph Workflow with LLM")
    logger.info("=" * 60)
    logger.info("[Starting Server]")
    logger.info("=" * 60)
    logger.info(f"   Host: {args.host}")
    logger.info(f"   Port: {args.port}")
    logger.info(f"   Docs: http://{args.host}:{args.port}/docs")
    logger.info(f"   Health: http://{args.host}:{args.port}/health")
    logger.info("=" * 60)
    logger.info("[MichelinBot] Ready! Ask about restaurants:")
    logger.info("   - 'Best 3-star restaurants'")
    logger.info("   - 'Romantic dinner recommendations'")
    logger.info("   - 'Japanese fine dining'")
    logger.info("=" * 60)

    # Start server
    uvicorn.run(
        "app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="debug" if args.debug else "info",
    )


if __name__ == "__main__":
    main()

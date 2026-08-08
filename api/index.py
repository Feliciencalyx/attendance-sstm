import sys
import os

# Include backend path for Vercel Serverless execution environment
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.main import app

# Vercel serverless WSGI/ASGI handler
__all__ = ["app"]

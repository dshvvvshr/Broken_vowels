"""Core Directive Gateway - FastAPI Application."""

from fastapi import FastAPI

app = FastAPI(
    title="Core Directive Gateway",
    description="A simple FastAPI gateway application",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to Core Directive Gateway"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

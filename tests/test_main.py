"""Tests for the chat completions API."""

import pytest
from fastapi.testclient import TestClient

from app.main import app, wrap_with_core_directive
from app.models import Message
from app.core_directive import CORE_DIRECTIVE


client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Chat Completions API"
    assert "/v1/chat/completions" in data["endpoints"]


def test_health_endpoint():
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_completions_adds_core_directive():
    """Test that chat completions adds Core Directive."""
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hello!"}]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "chat.completion"
    assert data["model"] == "gpt-3.5-turbo"
    assert len(data["choices"]) == 1
    assert "Core Directive applied" in data["choices"][0]["message"]["content"]


def test_chat_completions_with_existing_system_message():
    """Test that Core Directive is prepended to existing system message."""
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "Custom instructions"},
                {"role": "user", "content": "Hello!"}
            ]
        }
    )
    assert response.status_code == 200


def test_wrap_with_core_directive_no_system_message():
    """Test wrapping adds system message when none exists."""
    messages = [Message(role="user", content="Hello")]
    wrapped = wrap_with_core_directive(messages)
    
    assert len(wrapped) == 2
    assert wrapped[0].role == "system"
    assert CORE_DIRECTIVE in wrapped[0].content
    assert wrapped[1].role == "user"


def test_wrap_with_core_directive_with_existing_system_message():
    """Test wrapping prepends to existing system message."""
    messages = [
        Message(role="system", content="Custom instruction"),
        Message(role="user", content="Hello")
    ]
    wrapped = wrap_with_core_directive(messages)
    
    assert len(wrapped) == 2
    assert wrapped[0].role == "system"
    assert CORE_DIRECTIVE in wrapped[0].content
    assert "Custom instruction" in wrapped[0].content
    assert wrapped[1].role == "user"


def test_chat_completions_response_structure():
    """Test the response has correct structure."""
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "test-model",
            "messages": [{"role": "user", "content": "Test"}]
        }
    )
    data = response.json()
    
    assert "id" in data
    assert data["id"].startswith("chatcmpl-")
    assert "created" in data
    assert "choices" in data
    assert "usage" in data
    assert "prompt_tokens" in data["usage"]
    assert "completion_tokens" in data["usage"]
    assert "total_tokens" in data["usage"]

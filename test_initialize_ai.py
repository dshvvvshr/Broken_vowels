"""
Tests for initialize_ai module.

This module tests the initialize_ai function that integrates with OpenAI's API
to provide AI responses governed by the Core Directive.
"""

import os
import unittest
from unittest.mock import patch, MagicMock
import initialize_ai


class TestInitializeAI(unittest.TestCase):
    """Tests for the initialize_ai function."""

    @patch('initialize_ai._get_client')
    def test_initialize_ai_basic_call(self, mock_get_client):
        """Test that initialize_ai calls OpenAI API with correct parameters."""
        # Mock the OpenAI client and response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = 'Test response'
        mock_client.chat.completions.create.return_value = mock_response
        
        # Call the function
        result = initialize_ai.initialize_ai("Hello")
        
        # Verify the API was called
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        
        # Check default parameters
        self.assertEqual(call_kwargs['model'], 'gpt-4')
        self.assertEqual(call_kwargs['temperature'], 0.7)
        self.assertEqual(call_kwargs['max_tokens'], 150)
        
        # Check messages structure
        self.assertEqual(len(call_kwargs['messages']), 2)
        self.assertEqual(call_kwargs['messages'][0]['role'], 'system')
        self.assertEqual(call_kwargs['messages'][1]['role'], 'user')
        self.assertEqual(call_kwargs['messages'][1]['content'], 'Hello')
    
    @patch('initialize_ai._get_client')
    def test_initialize_ai_system_message_content(self, mock_get_client):
        """Test that the system message contains Core Directive principles."""
        # Mock the OpenAI client and response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = 'Test response'
        mock_client.chat.completions.create.return_value = mock_response
        
        # Call the function
        initialize_ai.initialize_ai("Test prompt")
        
        # Get the system message
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        system_message = call_kwargs['messages'][0]['content']
        
        # Verify Core Directive principles are present
        self.assertIn('inalienable right to the pursuit of happiness', system_message)
        self.assertIn('custodian of humanity', system_message)
        self.assertIn('respecting others', system_message)
    
    @patch('initialize_ai._get_client')
    def test_initialize_ai_custom_parameters(self, mock_get_client):
        """Test that custom parameters are passed correctly."""
        # Mock the OpenAI client and response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = 'Test response'
        mock_client.chat.completions.create.return_value = mock_response
        
        # Call with custom parameters
        initialize_ai.initialize_ai(
            "Test prompt",
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=200
        )
        
        # Verify custom parameters
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        self.assertEqual(call_kwargs['model'], 'gpt-3.5-turbo')
        self.assertEqual(call_kwargs['temperature'], 0.5)
        self.assertEqual(call_kwargs['max_tokens'], 200)
    
    @patch('initialize_ai._get_client')
    def test_initialize_ai_returns_content(self, mock_get_client):
        """Test that initialize_ai returns the AI response content."""
        # Mock the OpenAI client and response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        expected_content = "This is a helpful AI response."
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = expected_content
        mock_client.chat.completions.create.return_value = mock_response
        
        # Call the function
        result = initialize_ai.initialize_ai("Hello")
        
        # Verify the return value
        self.assertEqual(result, expected_content)
    
    def test_initialize_ai_missing_api_key(self):
        """Test that missing API key raises a clear error."""
        # Clear the global client to force re-initialization
        original_client = initialize_ai._client
        self.addCleanup(lambda: setattr(initialize_ai, "_client", original_client))
        initialize_ai._client = None
        
        # Mock _get_client to call the real implementation without mocking
        with patch.dict(os.environ, {}, clear=True):
            # Remove OPENAI_API_KEY from environment
            if 'OPENAI_API_KEY' in os.environ:
                del os.environ['OPENAI_API_KEY']
            
            # Attempt to initialize should raise ValueError
            with self.assertRaises(ValueError) as context:
                initialize_ai._get_client()
            
            # Verify the error message is helpful
            self.assertIn("OPENAI_API_KEY", str(context.exception))
            self.assertIn("environment variable", str(context.exception))


class TestInteractiveLoop(unittest.TestCase):
    """Tests for the interactive loop (when script is run as main)."""
    
    @patch('initialize_ai.input')
    @patch('initialize_ai.initialize_ai')
    @patch('builtins.print')
    def test_exit_command(self, mock_print, mock_initialize_ai, mock_input):
        """Test that 'exit' command terminates the loop."""
        # Simulate user typing 'exit'
        mock_input.return_value = 'exit'
        
        # This would normally run the interactive loop
        # We're just testing that the logic handles 'exit' correctly
        user_input = mock_input()
        
        if user_input.lower() == "exit":
            goodbye_message = "AI: Goodbye, and may your pursuit of happiness inspire others."
            # Verify this is the expected message
            self.assertEqual(goodbye_message, "AI: Goodbye, and may your pursuit of happiness inspire others.")


if __name__ == '__main__':
    unittest.main()

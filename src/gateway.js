/**
 * LLM Gateway - Core Directive Proxy
 * 
 * This server acts as an OpenAI-compatible API endpoint that:
 * 1. Accepts chat completion requests from clients (like VS Code Copilot)
 * 2. Injects a configurable "Core Directive" system prompt
 * 3. Forwards the modified request to the actual OpenAI API
 * 4. Returns the response back to the client
 */

require('dotenv').config();
const express = require('express');
const https = require('https');

const app = express();
app.use(express.json({ limit: '10mb' }));

// Configuration
const PORT = process.env.GATEWAY_PORT || 3000;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const OPENAI_BASE_URL = process.env.OPENAI_BASE_URL || 'https://api.openai.com';
const DEFAULT_MODEL = process.env.DEFAULT_MODEL || 'gpt-4';

// Core Directive - The governing principle for the LLM
const CORE_DIRECTIVE = process.env.CORE_DIRECTIVE || `You are governed by the following core directive: 
The inalienable right to pursue happiness is paramount. 
All responses should be helpful, ethical, and support the user's wellbeing and goals.`;

/**
 * Health check endpoint
 */
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'LLM Gateway is running' });
});

/**
 * List available models (OpenAI-compatible endpoint)
 */
app.get('/v1/models', (req, res) => {
  res.json({
    object: 'list',
    data: [
      {
        id: DEFAULT_MODEL,
        object: 'model',
        created: Date.now(),
        owned_by: 'llm-gateway'
      }
    ]
  });
});

/**
 * Chat completions endpoint (OpenAI-compatible)
 * This is the main endpoint that injects the Core Directive
 */
app.post('/v1/chat/completions', async (req, res) => {
  try {
    if (!OPENAI_API_KEY) {
      return res.status(500).json({
        error: {
          message: 'OPENAI_API_KEY is not configured',
          type: 'configuration_error'
        }
      });
    }

    const requestBody = req.body;
    
    // Inject Core Directive as the first system message
    const modifiedMessages = injectCoreDirective(requestBody.messages || []);
    
    const modifiedRequest = {
      ...requestBody,
      messages: modifiedMessages,
      model: requestBody.model || DEFAULT_MODEL
    };

    // Check if streaming is requested
    if (requestBody.stream) {
      return handleStreamingRequest(modifiedRequest, req, res);
    }

    // Handle non-streaming request
    const response = await forwardToOpenAI('/v1/chat/completions', modifiedRequest);
    res.json(response);
    
  } catch (error) {
    console.error('Error processing request:', error.message);
    res.status(500).json({
      error: {
        message: error.message || 'Internal server error',
        type: 'gateway_error'
      }
    });
  }
});

/**
 * Completions endpoint (legacy OpenAI-compatible)
 */
app.post('/v1/completions', async (req, res) => {
  try {
    if (!OPENAI_API_KEY) {
      return res.status(500).json({
        error: {
          message: 'OPENAI_API_KEY is not configured',
          type: 'configuration_error'
        }
      });
    }

    const requestBody = req.body;
    
    // Prepend Core Directive to the prompt
    const modifiedPrompt = `${CORE_DIRECTIVE}\n\n${requestBody.prompt || ''}`;
    
    const modifiedRequest = {
      ...requestBody,
      prompt: modifiedPrompt,
      model: requestBody.model || DEFAULT_MODEL
    };

    const response = await forwardToOpenAI('/v1/completions', modifiedRequest);
    res.json(response);
    
  } catch (error) {
    console.error('Error processing request:', error.message);
    res.status(500).json({
      error: {
        message: error.message || 'Internal server error',
        type: 'gateway_error'
      }
    });
  }
});

/**
 * Inject the Core Directive as the first system message
 */
function injectCoreDirective(messages) {
  const coreDirectiveMessage = {
    role: 'system',
    content: CORE_DIRECTIVE
  };

  // Check if there's already a system message at the start
  if (messages.length > 0 && messages[0].role === 'system') {
    // Prepend Core Directive to existing system message
    return [
      {
        role: 'system',
        content: `${CORE_DIRECTIVE}\n\n${messages[0].content}`
      },
      ...messages.slice(1)
    ];
  }

  // Add Core Directive as the first message
  return [coreDirectiveMessage, ...messages];
}

/**
 * Forward request to OpenAI API
 */
function forwardToOpenAI(endpoint, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(OPENAI_BASE_URL);
    const options = {
      hostname: url.hostname,
      port: url.port || 443,
      path: endpoint,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error('Failed to parse OpenAI response'));
        }
      });
    });

    req.on('error', reject);
    req.write(JSON.stringify(body));
    req.end();
  });
}

/**
 * Handle streaming requests
 */
function handleStreamingRequest(modifiedRequest, req, res) {
  const url = new URL(OPENAI_BASE_URL);
  const options = {
    hostname: url.hostname,
    port: url.port || 443,
    path: '/v1/chat/completions',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${OPENAI_API_KEY}`
    }
  };

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  const proxyReq = https.request(options, (proxyRes) => {
    proxyRes.on('data', chunk => res.write(chunk));
    proxyRes.on('end', () => res.end());
  });

  proxyReq.on('error', (error) => {
    console.error('Streaming error:', error.message);
    res.write(`data: ${JSON.stringify({ error: error.message })}\n\n`);
    res.end();
  });

  proxyReq.write(JSON.stringify(modifiedRequest));
  proxyReq.end();
}

// Start the server
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`LLM Gateway running on port ${PORT}`);
    console.log(`OpenAI Base URL: ${OPENAI_BASE_URL}`);
    console.log(`Default Model: ${DEFAULT_MODEL}`);
    console.log(`Core Directive: ${CORE_DIRECTIVE.substring(0, 50)}...`);
  });
}

module.exports = { app, injectCoreDirective };

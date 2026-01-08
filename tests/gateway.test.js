/**
 * Tests for LLM Gateway
 */

const request = require('supertest');
const { app, injectCoreDirective } = require('../src/gateway');
const https = require('https');

describe('LLM Gateway', () => {
  describe('Health Check', () => {
    it('should return ok status', async () => {
      const response = await request(app).get('/health');
      expect(response.status).toBe(200);
      expect(response.body.status).toBe('ok');
      expect(response.body.message).toBe('LLM Gateway is running');
    });
  });

  describe('Models Endpoint', () => {
    it('should return list of available models', async () => {
      const response = await request(app).get('/v1/models');
      expect(response.status).toBe(200);
      expect(response.body.object).toBe('list');
      expect(response.body.data).toBeInstanceOf(Array);
      expect(response.body.data.length).toBeGreaterThan(0);
      expect(response.body.data[0]).toHaveProperty('id');
      expect(response.body.data[0]).toHaveProperty('object', 'model');
    });
  });

  describe('Core Directive Injection', () => {
    it('should inject core directive when no system message exists', () => {
      const messages = [
        { role: 'user', content: 'Hello' }
      ];
      
      const result = injectCoreDirective(messages);
      
      expect(result.length).toBe(2);
      expect(result[0].role).toBe('system');
      expect(result[0].content).toContain('inalienable right to pursue happiness');
      expect(result[1].role).toBe('user');
      expect(result[1].content).toBe('Hello');
    });

    it('should prepend core directive to existing system message', () => {
      const messages = [
        { role: 'system', content: 'You are a helpful assistant.' },
        { role: 'user', content: 'Hello' }
      ];
      
      const result = injectCoreDirective(messages);
      
      expect(result.length).toBe(2);
      expect(result[0].role).toBe('system');
      expect(result[0].content).toContain('inalienable right to pursue happiness');
      expect(result[0].content).toContain('You are a helpful assistant.');
      expect(result[1].role).toBe('user');
    });

    it('should handle empty messages array', () => {
      const messages = [];
      
      const result = injectCoreDirective(messages);
      
      expect(result.length).toBe(1);
      expect(result[0].role).toBe('system');
      expect(result[0].content).toContain('inalienable right to pursue happiness');
    });
  });

  describe('Chat Completions Endpoint', () => {
    it('should return error when OPENAI_API_KEY is not set', async () => {
      // Save original env
      const originalKey = process.env.OPENAI_API_KEY;
      const originalDotenv = process.env.DOTENV_CONFIG_PATH;
      
      // Set to empty string to simulate missing key
      process.env.OPENAI_API_KEY = '';
      // Prevent dotenv from reloading
      process.env.DOTENV_CONFIG_PATH = '/dev/null';
      
      // Re-require the module to pick up the new env
      jest.resetModules();
      const { app: freshApp } = require('../src/gateway');
      
      const response = await request(freshApp)
        .post('/v1/chat/completions')
        .send({
          model: 'gpt-4',
          messages: [{ role: 'user', content: 'Hello' }]
        });
      
      expect(response.status).toBe(500);
      expect(response.body.error.message).toContain('OPENAI_API_KEY is not configured');
      
      // Restore original env
      if (originalKey !== undefined) {
        process.env.OPENAI_API_KEY = originalKey;
      } else {
        delete process.env.OPENAI_API_KEY;
      }
      if (originalDotenv) {
        process.env.DOTENV_CONFIG_PATH = originalDotenv;
      } else {
        delete process.env.DOTENV_CONFIG_PATH;
      }
    });
  });

  describe('Completions Endpoint', () => {
    it('should return error when OPENAI_API_KEY is not set', async () => {
      // Save original env
      const originalKey = process.env.OPENAI_API_KEY;
      const originalDotenv = process.env.DOTENV_CONFIG_PATH;
      
      // Set to empty string to simulate missing key
      process.env.OPENAI_API_KEY = '';
      // Prevent dotenv from reloading
      process.env.DOTENV_CONFIG_PATH = '/dev/null';
      
      // Re-require the module to pick up the new env
      jest.resetModules();
      const { app: freshApp } = require('../src/gateway');
      
      const response = await request(freshApp)
        .post('/v1/completions')
        .send({
          model: 'gpt-4',
          prompt: 'Hello'
        });
      
      expect(response.status).toBe(500);
      expect(response.body.error.message).toContain('OPENAI_API_KEY is not configured');
      
      // Restore original env
      if (originalKey !== undefined) {
        process.env.OPENAI_API_KEY = originalKey;
      } else {
        delete process.env.OPENAI_API_KEY;
      }
      if (originalDotenv) {
        process.env.DOTENV_CONFIG_PATH = originalDotenv;
      } else {
        delete process.env.DOTENV_CONFIG_PATH;
      }
    });
  });

  describe('Streaming Response', () => {
    it('should handle streaming requests', async () => {
      // Save original env
      const originalKey = process.env.OPENAI_API_KEY;
      
      // Mock API key for streaming test
      process.env.OPENAI_API_KEY = 'test-key';
      
      jest.resetModules();
      const { app: freshApp } = require('../src/gateway');
      
      // Mock https.request for streaming
      const mockRequest = jest.spyOn(https, 'request');
      const mockOn = jest.fn();
      const mockWrite = jest.fn();
      const mockEnd = jest.fn();
      
      mockRequest.mockImplementation((options, callback) => {
        // Simulate successful response
        const mockRes = {
          on: jest.fn((event, handler) => {
            if (event === 'data') {
              // Simulate streaming data
              handler(Buffer.from('data: {"choices":[{"delta":{"content":"test"}}]}\n\n'));
            } else if (event === 'end') {
              handler();
            }
          })
        };
        
        setTimeout(() => callback(mockRes), 10);
        
        return {
          on: mockOn,
          write: mockWrite,
          end: mockEnd
        };
      });
      
      const response = await request(freshApp)
        .post('/v1/chat/completions')
        .send({
          model: 'gpt-4',
          messages: [{ role: 'user', content: 'Hello' }],
          stream: true
        });
      
      // Should set up streaming headers
      expect(mockWrite).toHaveBeenCalled();
      
      // Restore
      mockRequest.mockRestore();
      if (originalKey !== undefined) {
        process.env.OPENAI_API_KEY = originalKey;
      } else {
        delete process.env.OPENAI_API_KEY;
      }
    });
  });

  describe('Error Handling', () => {
    it('should handle malformed JSON requests', async () => {
      const response = await request(app)
        .post('/v1/chat/completions')
        .set('Content-Type', 'application/json')
        .send('{"invalid": json}');
      
      expect(response.status).toBe(400);
    });

    it('should handle missing messages field', async () => {
      // Set API key for this test
      const originalKey = process.env.OPENAI_API_KEY;
      process.env.OPENAI_API_KEY = 'test-key';
      
      jest.resetModules();
      const { app: freshApp } = require('../src/gateway');
      
      // Mock https.request to simulate API call
      const mockRequest = jest.spyOn(https, 'request');
      mockRequest.mockImplementation((options, callback) => {
        const mockRes = {
          on: jest.fn((event, handler) => {
            if (event === 'data') {
              handler(Buffer.from(JSON.stringify({
                choices: [{ message: { content: 'response' } }]
              })));
            } else if (event === 'end') {
              handler();
            }
          })
        };
        
        setTimeout(() => callback(mockRes), 10);
        
        return {
          on: jest.fn(),
          write: jest.fn(),
          end: jest.fn()
        };
      });
      
      const response = await request(freshApp)
        .post('/v1/chat/completions')
        .send({
          model: 'gpt-4'
          // messages field missing
        });
      
      // Should handle gracefully
      expect(response.status).toBe(200);
      
      mockRequest.mockRestore();
      if (originalKey !== undefined) {
        process.env.OPENAI_API_KEY = originalKey;
      } else {
        delete process.env.OPENAI_API_KEY;
      }
    });

    it('should handle network errors gracefully', async () => {
      const originalKey = process.env.OPENAI_API_KEY;
      process.env.OPENAI_API_KEY = 'test-key';
      
      jest.resetModules();
      const { app: freshApp } = require('../src/gateway');
      
      // Mock network error
      const mockRequest = jest.spyOn(https, 'request');
      mockRequest.mockImplementation(() => {
        return {
          on: jest.fn((event, handler) => {
            if (event === 'error') {
              handler(new Error('Network error'));
            }
          }),
          write: jest.fn(),
          end: jest.fn()
        };
      });
      
      const response = await request(freshApp)
        .post('/v1/chat/completions')
        .send({
          model: 'gpt-4',
          messages: [{ role: 'user', content: 'test' }]
        });
      
      expect(response.status).toBe(500);
      expect(response.body.error).toBeDefined();
      
      mockRequest.mockRestore();
      if (originalKey !== undefined) {
        process.env.OPENAI_API_KEY = originalKey;
      } else {
        delete process.env.OPENAI_API_KEY;
      }
    });
  });

  describe('OpenAI API Integration', () => {
    it('should successfully forward requests to OpenAI', async () => {
      const originalKey = process.env.OPENAI_API_KEY;
      process.env.OPENAI_API_KEY = 'test-key';
      
      jest.resetModules();
      const { app: freshApp } = require('../src/gateway');
      
      // Mock successful OpenAI response
      const mockRequest = jest.spyOn(https, 'request');
      mockRequest.mockImplementation((options, callback) => {
        // Verify correct headers
        expect(options.headers['Authorization']).toBe('Bearer test-key');
        expect(options.headers['Content-Type']).toBe('application/json');
        
        const mockRes = {
          on: jest.fn((event, handler) => {
            if (event === 'data') {
              handler(Buffer.from(JSON.stringify({
                id: 'chatcmpl-123',
                object: 'chat.completion',
                model: 'gpt-4',
                choices: [{
                  message: { role: 'assistant', content: 'Hello!' },
                  finish_reason: 'stop'
                }]
              })));
            } else if (event === 'end') {
              handler();
            }
          })
        };
        
        setTimeout(() => callback(mockRes), 10);
        
        return {
          on: jest.fn(),
          write: jest.fn(),
          end: jest.fn()
        };
      });
      
      const response = await request(freshApp)
        .post('/v1/chat/completions')
        .send({
          model: 'gpt-4',
          messages: [{ role: 'user', content: 'Hello' }]
        });
      
      expect(response.status).toBe(200);
      expect(response.body.choices).toBeDefined();
      expect(response.body.choices[0].message.content).toBe('Hello!');
      
      mockRequest.mockRestore();
      if (originalKey !== undefined) {
        process.env.OPENAI_API_KEY = originalKey;
      } else {
        delete process.env.OPENAI_API_KEY;
      }
    });

    it('should handle OpenAI API errors', async () => {
      const originalKey = process.env.OPENAI_API_KEY;
      process.env.OPENAI_API_KEY = 'test-key';
      
      jest.resetModules();
      const { app: freshApp } = require('../src/gateway');
      
      // Mock OpenAI error response
      const mockRequest = jest.spyOn(https, 'request');
      mockRequest.mockImplementation((options, callback) => {
        const mockRes = {
          on: jest.fn((event, handler) => {
            if (event === 'data') {
              handler(Buffer.from(JSON.stringify({
                error: {
                  message: 'Invalid API key',
                  type: 'invalid_request_error'
                }
              })));
            } else if (event === 'end') {
              handler();
            }
          })
        };
        
        setTimeout(() => callback(mockRes), 10);
        
        return {
          on: jest.fn(),
          write: jest.fn(),
          end: jest.fn()
        };
      });
      
      const response = await request(freshApp)
        .post('/v1/chat/completions')
        .send({
          model: 'gpt-4',
          messages: [{ role: 'user', content: 'test' }]
        });
      
      expect(response.status).toBe(200);
      expect(response.body.error).toBeDefined();
      
      mockRequest.mockRestore();
      if (originalKey !== undefined) {
        process.env.OPENAI_API_KEY = originalKey;
      } else {
        delete process.env.OPENAI_API_KEY;
      }
    });
  });

  describe('Completions Endpoint (Legacy)', () => {
    it('should inject Core Directive into prompt', async () => {
      const originalKey = process.env.OPENAI_API_KEY;
      process.env.OPENAI_API_KEY = 'test-key';
      
      jest.resetModules();
      const { app: freshApp } = require('../src/gateway');
      
      let capturedBody = null;
      const mockRequest = jest.spyOn(https, 'request');
      mockRequest.mockImplementation((options, callback) => {
        const mockRes = {
          on: jest.fn((event, handler) => {
            if (event === 'data') {
              handler(Buffer.from(JSON.stringify({
                choices: [{ text: 'response' }]
              })));
            } else if (event === 'end') {
              handler();
            }
          })
        };
        
        setTimeout(() => callback(mockRes), 10);
        
        return {
          on: jest.fn(),
          write: jest.fn((data) => {
            capturedBody = JSON.parse(data);
          }),
          end: jest.fn()
        };
      });
      
      await request(freshApp)
        .post('/v1/completions')
        .send({
          model: 'gpt-4',
          prompt: 'Hello world'
        });
      
      // Verify Core Directive was prepended
      expect(capturedBody.prompt).toContain('inalienable right to pursue happiness');
      expect(capturedBody.prompt).toContain('Hello world');
      
      mockRequest.mockRestore();
      if (originalKey !== undefined) {
        process.env.OPENAI_API_KEY = originalKey;
      } else {
        delete process.env.OPENAI_API_KEY;
      }
    });
  });
});

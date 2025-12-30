/**
 * Tests for LLM Gateway
 */

const request = require('supertest');
const { app, injectCoreDirective } = require('../src/gateway');

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
});

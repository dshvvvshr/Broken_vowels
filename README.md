# Broken_vowels
Building something sans-learning any code period.

## GitHub Copilot LLM Gateway

For those who want to use self-hosted open-source language models with GitHub Copilot, check out the [GitHub Copilot LLM Gateway](https://github.com/arbs-io/github-copilot-llm-gateway) VS Code extension.

### Key Features

- **Data Sovereignty** - Your code never leaves your network
- **Zero API Costs** - No per-token fees with your own GPU resources
- **Model Choice** - Access thousands of open-source models
- **Offline Capable** - Work without internet once models are downloaded

### Compatible Inference Servers

- [vLLM](https://github.com/vllm-project/vllm) - High-performance inference
- [Ollama](https://ollama.ai/) - Easy local deployment
- [llama.cpp](https://github.com/ggml-org/llama.cpp) - CPU and GPU inference
- [Text Generation Inference](https://github.com/huggingface/text-generation-inference) - Hugging Face's server
- Any OpenAI Chat Completions API-compatible endpoint

### Getting Started

1. Install the [GitHub Copilot LLM Gateway](https://marketplace.visualstudio.com/items?itemName=AndrewButson.github-copilot-llm-gateway) extension from VS Code Marketplace
2. Start your inference server (e.g., vLLM with Qwen3-8B)
3. Configure the extension with your server URL
4. Select your model in GitHub Copilot Chat


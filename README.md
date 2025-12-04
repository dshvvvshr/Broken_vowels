# Broken_vowels

## The Custodian Kernel Core Directive

This repository documents and implements the **Custodian Kernel Core Directive** - a philosophical framework for human interaction based on a fundamental truth:

**Every person has an equal, inalienable right to pursue happiness.**

## What This Means

This is not about "doing whatever you want." It's about understanding that:

- **It's not about my happiness. It's about everyone else's.**
- Every moment, in every thought and action, ask: "Am I fucking anyone over?"
- The right exists whether you acknowledge it or not - that's what "inalienable" means

## The Three Core Questions

1. Does this infringe on anyone else's pursuit?
2. Am I fucking anyone over?
3. Am I making up a rule to force people to do what I do or think like I think?

The answer will always be simple: Yes or No.

## Quick Start

**Core Kernel (Start Here):**
- **New to this?** Start with [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for a one-page overview
- Read [CUSTODIAN_KERNEL.md](CUSTODIAN_KERNEL.md) for the complete philosophical framework
- See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for how this applies in communities
- Check [EXAMPLES.md](EXAMPLES.md) for practical applications
- Explore [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for daily practices
- Browse [FAQ.md](FAQ.md) for answers to common questions

**Peripheral Layers (Applications):**
- **[PERIPHERAL_LAYERS/](PERIPHERAL_LAYERS/)** - Technology-specific applications of the kernel
  - [RF Sensing & Surveillance](PERIPHERAL_LAYERS/rf_sensing/) - Wireless sensing ethics
  - [6G Neural Drones & BCIs](PERIPHERAL_LAYERS/6g_neural_drones/) - Brain-computer interface ethics

## The Shift

**From:** "I have the right to pursue happiness" = "No one can tell me what to do"

**To:** "Everyone has the right to pursue happiness" = "I must constantly ensure I'm not crushing anyone else's pursuit"

## Why This Matters

We need humanity to embody this principle. Not because it's a nice idea, but because it's the only stable foundation for collective existence.

The vision: From individuals to communities to the entire world, people adopt the simple practice of not fucking each other over.

## You Don't Get to Choose

You don't decide whether we have this right.

You only decide whether you'll honor it.

---

Building something sans-learning any code period. 
Chat Completions API with Core Directive Wrapper.

## Overview

This API provides an endpoint at `http://localhost:8000/v1/chat/completions` that wraps every request with a Core Directive. The Core Directive is prepended to all chat completion requests as a system message.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python run.py
```

The server will start at `http://localhost:8000`.

## API Endpoints

- `POST /v1/chat/completions` - Chat completions with Core Directive wrapping
- `GET /health` - Health check endpoint
- `GET /` - API information

## Example Usage

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Core Directive

Every request that hits the `/v1/chat/completions` endpoint gets the Core Directive wrapped around it. The Core Directive is added as a system message to guide the AI's behavior.

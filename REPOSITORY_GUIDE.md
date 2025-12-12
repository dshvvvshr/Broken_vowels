# Repository Guide

Welcome to the Broken_vowels repository! This guide helps you navigate the documentation and understand the project structure.

## 📚 Documentation Index

### Getting Started
- **[README.md](README.md)** - Main project overview and quick start guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - One-page overview of the Core Directive

### Core Concepts
- **[CUSTODIAN_KERNEL.md](CUSTODIAN_KERNEL.md)** - Complete philosophical framework
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Daily practices and implementation
- **[EXAMPLES.md](EXAMPLES.md)** - Practical applications and use cases
- **[FAQ.md](FAQ.md)** - Frequently asked questions

### Contributing
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to this project
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Community standards
- **[SECURITY.md](SECURITY.md)** - Security policy and reporting vulnerabilities
- **[LICENSE](LICENSE)** - Public domain dedication (Unlicense)

### Technical Documentation
- **[.env.example](.env.example)** - Environment configuration template
- **[package.json](package.json)** - Node.js project configuration
- **[requirements.txt](requirements.txt)** - Python dependencies

## 🏗️ Project Structure

```
Broken_vowels/
├── .github/              # GitHub configuration
│   ├── ISSUE_TEMPLATE/   # Issue templates
│   ├── workflows/        # CI/CD workflows
│   ├── dependabot.yml    # Dependency updates
│   └── pull_request_template.md
├── PERIPHERAL_LAYERS/    # Technology-specific applications
│   ├── rf_sensing/       # RF sensing and surveillance ethics
│   └── 6g_neural_drones/ # Brain-computer interface ethics
├── app/                  # Python application
│   ├── __init__.py
│   ├── core_directive.py # Core governance kernel
│   ├── main.py           # FastAPI application
│   └── models.py         # Data models
├── src/                  # Node.js application
│   └── gateway.js        # LLM Gateway implementation
├── tests/                # Test files
│   ├── gateway.test.js   # Node.js tests
│   └── test_main.py      # Python tests
├── Core Python modules   # Root-level Python modules
│   ├── ai_client.py      # AI client integration
│   ├── core_directive.py # Core directive
│   ├── evaluator.py      # Evaluation engine
│   ├── gateway.py        # Gateway architecture
│   └── test_governance.py # Governance tests
├── Web files
│   ├── index.html        # Web interface
│   ├── server.py         # Simple web server
│   └── run.py            # Application runner
└── Documentation         # All markdown files listed above
```

## 🎯 Main Components

### 1. LLM Gateway (Node.js)
- **Location**: `src/gateway.js`
- **Purpose**: OpenAI-compatible API gateway with Core Directive injection
- **Start**: `npm start`
- **Test**: `npm test`

### 2. Core Directive Governance (Python)
- **Location**: `core_directive.py`, `evaluator.py`, `gateway.py`
- **Purpose**: Governance kernel for AI systems
- **Test**: `python -m unittest test_governance -v`

### 3. FastAPI Application (Python)
- **Location**: `app/main.py`
- **Purpose**: Chat completions API with Core Directive wrapper
- **Start**: `python run.py`

## 🚀 Quick Start Paths

### For Developers
1. Read [README.md](README.md)
2. Review [CONTRIBUTING.md](CONTRIBUTING.md)
3. Check `.env.example` for configuration
4. Run tests to verify setup

### For Philosophers/Ethicists
1. Start with [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. Deep dive into [CUSTODIAN_KERNEL.md](CUSTODIAN_KERNEL.md)
3. Explore [EXAMPLES.md](EXAMPLES.md) for applications
4. Check [FAQ.md](FAQ.md) for common questions

### For Users
1. Read [README.md](README.md) for overview
2. Follow quick start guide for installation
3. Configure `.env` file
4. Start the gateway or application

### For Contributors
1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Review [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
3. Check [SECURITY.md](SECURITY.md) for security guidelines
4. Use issue templates when reporting bugs or requesting features

## 🔧 Development Workflow

1. **Fork and Clone**: Fork the repository and clone to your machine
2. **Install Dependencies**: 
   - Node.js: `npm install`
   - Python: `pip install -r requirements.txt`
3. **Create Branch**: `git checkout -b feature/your-feature`
4. **Make Changes**: Edit code, add tests, update docs
5. **Test**: Run tests to ensure everything works
6. **Commit**: Use clear, descriptive commit messages
7. **Push**: Push to your fork
8. **Pull Request**: Open a PR with description

## 📊 CI/CD Workflows

All workflows are in `.github/workflows/`:

- **python-tests.yml** - Runs Python tests on multiple versions
- **node-tests.yml** - Runs Node.js tests on multiple versions
- **lint.yml** - Lints Python and JavaScript code
- **codeql.yml** - Security scanning with CodeQL

## 🛡️ Security

- Review [SECURITY.md](SECURITY.md) for security policy
- Never commit secrets or API keys
- Use `.env` files for sensitive configuration
- Report vulnerabilities privately through GitHub Security Advisories

## 📄 License

This project is released into the public domain under the [Unlicense](LICENSE).
The Core Directive belongs to humanity.

## 🤝 Community

- **Issues**: Use templates in `.github/ISSUE_TEMPLATE/`
- **Pull Requests**: Follow the PR template
- **Discussions**: Open for questions and ideas
- **Code of Conduct**: See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## 📞 Support

- Check [FAQ.md](FAQ.md) for common questions
- Search existing issues
- Open a new issue using the appropriate template
- Read documentation thoroughly before asking

---

*Building the ethical plumbing of civilization, one commit at a time.*

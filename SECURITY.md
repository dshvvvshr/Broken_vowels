# Security Policy

## Supported Versions

We actively maintain the latest version of this project. Security updates are applied to:

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| < latest| :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Open a Public Issue

Please do not disclose security vulnerabilities through public GitHub issues.

### 2. Report Privately

Send a detailed report to the repository maintainers via:
- GitHub Security Advisories (preferred)
- Direct message to repository owner

### 3. Include in Your Report

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)
- Your contact information (optional)

### 4. What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 5 business days
- **Status Updates**: Regular updates on progress
- **Resolution Timeline**: Depends on severity and complexity

### 5. Responsible Disclosure

We request that you:
- Give us reasonable time to address the issue before public disclosure
- Make a good faith effort to avoid privacy violations, data destruction, and service interruption
- Only interact with test accounts you own or with explicit permission

## Security Best Practices

### API Keys and Secrets

- **Never commit** API keys, tokens, or secrets to the repository
- Use environment variables (`.env` files) for sensitive data
- The `.env.example` file shows required variables without sensitive values
- Rotate credentials if they are accidentally exposed

### Dependencies

- Keep dependencies up to date
- Review dependency security advisories
- Use `npm audit` (Node.js) or `pip-audit` (Python) regularly

### Gateway Security

When using the LLM Gateway:

1. **Protect Your API Keys**
   - Store OpenAI API keys securely
   - Never expose them in client-side code
   - Use environment variables

2. **Network Security**
   - Use HTTPS in production
   - Consider rate limiting
   - Implement authentication for production deployments

3. **Input Validation**
   - The gateway validates inputs
   - Additional validation may be needed for specific use cases

4. **Monitoring**
   - Monitor for unusual API usage
   - Track failed requests
   - Set up alerts for anomalies

## Core Directive Security Implications

The Core Directive ("No action may interfere with another person's inalienable right to pursue happiness") has security implications:

- **Privacy**: Respect user privacy and data sovereignty
- **Consent**: Obtain proper consent for data collection and processing
- **Transparency**: Be transparent about data usage and AI behavior
- **Non-interference**: Don't create systems that manipulate or coerce users

## Vulnerability Disclosure Policy

When we receive a security report:

1. **Confirmation**: We confirm receipt and begin investigation
2. **Assessment**: We assess severity and impact
3. **Fix Development**: We develop and test a fix
4. **Disclosure**: We coordinate disclosure with the reporter
5. **Release**: We release the fix and publish an advisory
6. **Credit**: We credit the reporter (unless they prefer anonymity)

## Security Updates

- Security updates are released as soon as possible
- Critical vulnerabilities may warrant immediate releases
- Users are notified through GitHub releases and security advisories

## Contact

For security concerns, please use GitHub's security advisory feature or contact the repository maintainers directly.

---

*Security is part of honoring everyone's right to pursue happiness safely.*

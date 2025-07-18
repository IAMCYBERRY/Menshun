---
name: Security Issue
about: Report a security vulnerability (Use private disclosure for sensitive issues)
title: '[SECURITY] '
labels: 'security'
assignees: ''
---

## ⚠️ IMPORTANT SECURITY NOTICE

**For critical security vulnerabilities, please DO NOT create a public issue.**

Instead, please report sensitive security issues privately by:
1. Emailing: security@menshun.com
2. Using GitHub's private vulnerability reporting feature
3. Contacting the maintainers directly

---

## 🔒 Security Issue Type
- [ ] Authentication/Authorization bypass
- [ ] Data exposure/leak
- [ ] Injection vulnerability (SQL, XSS, etc.)
- [ ] Privilege escalation
- [ ] Cryptographic weakness
- [ ] Configuration vulnerability
- [ ] Dependency vulnerability
- [ ] Other: _______________

## 📊 Severity Assessment
- [ ] **Critical** - Complete system compromise, data breach
- [ ] **High** - Significant security impact, privileged access
- [ ] **Medium** - Limited security impact, requires user interaction
- [ ] **Low** - Minimal security impact, specific conditions required

## 🎯 Affected Components
- [ ] Frontend (React application)
- [ ] Backend API (FastAPI)
- [ ] Database (PostgreSQL)
- [ ] Authentication (Azure AD/MSAL)
- [ ] Authorization (Role-based access)
- [ ] Credential management
- [ ] Audit logging
- [ ] Docker/Kubernetes deployment
- [ ] Other: _______________

## 🔍 Vulnerability Description
**Brief summary:**
[Provide a clear, concise description of the vulnerability]

**Technical details:**
[Detailed technical description of the issue]

## 🔄 Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Observe the security issue]

**Prerequisites:**
- User role required: [e.g. Authenticated user, Admin]
- Specific configuration: [if any]
- Network access: [e.g. Internal network, Internet]

## 💥 Impact Assessment
**What can an attacker achieve?**
- [ ] Access unauthorized data
- [ ] Modify sensitive information
- [ ] Gain administrative privileges
- [ ] Execute arbitrary code
- [ ] Denial of service
- [ ] Other: _______________

**Affected data types:**
- [ ] User credentials
- [ ] Privileged access tokens
- [ ] Audit logs
- [ ] Directory role assignments
- [ ] Service account credentials
- [ ] Configuration data
- [ ] Other: _______________

## 🛡️ Security Controls Bypassed
- [ ] Authentication
- [ ] Authorization
- [ ] Input validation
- [ ] Output encoding
- [ ] Rate limiting
- [ ] Audit logging
- [ ] Encryption
- [ ] Other: _______________

## 🖥️ Environment Information
- Menshun Version: [e.g. 1.0.0]
- Deployment Method: [e.g. Docker Compose, Kubernetes]
- Operating System: [e.g. Ubuntu 22.04]
- Browser (if applicable): [e.g. Chrome 120]
- Azure AD tenant type: [e.g. Single tenant, Multi-tenant]

## 📋 Proof of Concept
```
[Include minimal proof of concept code/steps - be careful not to provide full exploits]
```

**Screenshots/Evidence:**
[Attach screenshots showing the vulnerability - redact sensitive data]

## 🔧 Proposed Mitigation
**Immediate workarounds:**
- [Temporary mitigation steps]

**Suggested fixes:**
- [Technical recommendations for fixing the issue]

## 📚 References
- CVE ID (if applicable): 
- Related security advisories:
- Standards/guidelines:
  - [OWASP Top 10](https://owasp.org/www-project-top-ten/)
  - [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## 🕐 Timeline
**Discovery date:** [When was this discovered?]
**First occurrence:** [When did this issue first appear?]
**Disclosure timeline preference:**
- [ ] Immediate public disclosure
- [ ] Coordinated disclosure (90 days)
- [ ] Extended timeline required (justify below)

## 👤 Reporter Information
**Reporting on behalf of:**
- [ ] Individual security researcher
- [ ] Security company
- [ ] Bug bounty program
- [ ] Internal security team
- [ ] Customer/user
- [ ] Other: _______________

**Public attribution:**
- [ ] Yes, please credit me publicly
- [ ] No, anonymous reporting preferred
- [ ] Credit organization only

**Contact information for follow-up:**
[Provide secure contact method if needed]

## 📝 Additional Notes
[Any additional context, related issues, or special considerations]

---

## 🛡️ Security Team Use Only

**Triage Status:**
- [ ] Confirmed vulnerability
- [ ] Investigating
- [ ] Not a security issue
- [ ] Duplicate of existing issue

**Response Priority:**
- [ ] Emergency (patch within 24 hours)
- [ ] High (patch within 1 week)
- [ ] Medium (patch within 1 month)
- [ ] Low (include in next release)

**Internal Tracking:**
- Internal ID: 
- Assigned to: 
- Target fix date:
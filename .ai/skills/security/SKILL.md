---
name: security
description: "Use when designing or implementing application security controls for the Grocery Platform."
---

# Security Engineering Skill

## 1. Purpose

This skill establishes mandatory application-security engineering practices for the Grocery Platform. Treat security as a system requirement throughout design, implementation, and review, not as something added after implementation. These standards do not finalize authentication, authorization, business workflows, or infrastructure.

## 2. Security Principles

- Apply least privilege and defense in depth.
- Use secure defaults and deny by default.
- Enforce security server-side with explicit authorization decisions.
- Fail safely without exposing sensitive details.
- Minimize sensitive data collection, retention, and exposure.
- Validate all untrusted input.
- Do not trust client-controlled state or frontend restrictions as security controls.

## 3. Authentication vs Authorization

```text
Authentication = who is the actor?
Authorization = what is the actor allowed to do?
Tenant isolation = which shop's data can the actor access?
```

Authentication must not be treated as authorization. A successfully authenticated merchant does not automatically gain access to every platform resource. Do not prescribe or implement an authentication mechanism in this skill.

## 4. Authorization

Every protected operation needs an authorization decision enforced server-side. Enforce object-level and action/workflow authorization, scope list endpoints to authorized objects, and authorize access through related objects. Protect platform-level privileges explicitly. Hidden UI elements and other frontend restrictions are not authorization controls.

Follow [.ai/skills/multi-tenancy/SKILL.md](../multi-tenancy/SKILL.md) for tenant isolation requirements.

## 5. Tenant Security

Shop-level isolation is a security boundary. Never trust client-provided `shop_id`, `tenant_id`, or `merchant_id` as proof of access, and never treat IDs as authorization. Prevent cross-shop reads, writes, deletes, relationship traversal, and unauthorized tenant reassignment.

Apply the same protection to background jobs, analytics, notifications, and management commands. Follow `.ai/skills/multi-tenancy/SKILL.md` for detailed tenant-isolation rules; do not replace or finalize its implementation here.

## 6. Input Validation

Validate all untrusted input on the server, including request data, query and path parameters, uploaded files, JSON payloads, text, numeric values, quantities, identifiers, URLs, and user-provided metadata. Do not rely on frontend validation. Prefer framework and serializer validation with domain-level validation where appropriate.

## 7. Injection Prevention

Prevent SQL injection, command injection, template injection, unsafe dynamic queries, unsafe HTML rendering, unsafe shell execution, and unsafe deserialization. Prefer the Django ORM and parameterized database operations. Raw SQL or shell execution requires a justified technical reason and careful handling; never interpolate untrusted input into executable commands or query text.

## 8. Secrets and Configuration

Never commit API keys, database credentials, tokens, passwords, signing keys, or other secrets. Never hardcode credentials or log secrets. Keep `.env` local and use `.env.example` with placeholders only. Use environment-based configuration as appropriate, without prescribing a secrets-management vendor.

## 9. Sensitive Data

Minimize and protect sensitive information, which may include customer phone numbers and delivery addresses, credentials, tokens, payment-related information, internal identifiers, and merchant information. Do not assume every customer field has the same sensitivity. Collect and expose only information required by approved product behavior.

## 10. API Security

Follow the contract and implementation standards in `.ai/skills/api-design/SKILL.md` and `.ai/skills/drf/SKILL.md`. API designs and implementations must account for authentication requirements, authorization, object-level access, request validation, response-data minimization, pagination, safe error responses, appropriate HTTP methods, content types, and request-size limits where appropriate.

Consider rate limiting and protection against enumeration where relevant, without selecting an implementation or infrastructure here. Use the approved `/api/v1/` versioning approach. Do not define actual endpoints in this skill.

## 11. Error Handling

Errors must fail safely. User-facing responses must not expose secrets, production stack traces, SQL or database internals, tenant data, or unnecessary implementation details. Internal logs may contain appropriate diagnostic information, subject to the logging rules below. Return only information necessary to the caller.

## 12. Logging and Auditability

Log security-relevant events where appropriate, including authentication and authorization events, sensitive administrative actions, important state changes, suspicious access patterns, and tenant-boundary violations. Do not log passwords, tokens, secrets, or unnecessary sensitive customer information. Logs must support investigation without becoming a source of data leakage.

## 13. File Upload Security

For file-upload features, validate file type and size; do not trust extensions or client-provided MIME types. Generate safe storage names, prevent executable uploads, validate storage permissions, and avoid unintentionally exposing private files. Do not choose a storage provider here.

## 14. Customer-Facing Security

The initial customer flow does not require traditional password accounts. Treat all customer-provided information as untrusted input. A WhatsApp number alone must not become authorization. Keep shop-specific customer identity isolated, expose only intended public or shop-scoped data, and do not let customer identifiers expose private merchant or customer information.

Do not invent or implement a customer authentication system.

## 15. Merchant Security

Protect merchant data isolation, privileged merchant operations, shop configuration, and merchant, customer, and order information. Prevent unauthorized shop switching. Handle merchant credentials securely once the authentication architecture is finalized. Do not define the final merchant role structure.

## 16. Super Admin Security

Platform-wide access is highly privileged. Require explicit authorization and least privilege for platform-wide operations. Protect destructive operations and maintain appropriate auditability for important administrative actions. Do not define the Super Admin authentication or permission implementation.

## 17. Database Security

Use least-privileged database access, appropriate integrity constraints, and tenant isolation. Do not use unsafe dynamic SQL or expose database internals through APIs. Protect database credentials. Follow `.ai/skills/database-design/SKILL.md` for schema-specific standards; this section does not define a schema.

## 18. Transactions and Security-Sensitive Operations

Consider database transactions for related writes that must succeed or fail together, including authorization-sensitive state changes, order or inventory changes, ownership changes, and administrative operations where applicable. Do not define specific business workflows or wrap every operation in a transaction without reason.

## 19. Concurrency and Race Conditions

Consider concurrent requests for security-sensitive operations, including duplicate operations, repeated submissions, inventory or ownership changes, and permission-sensitive updates. Do not assume client-side prevention eliminates race conditions. Use appropriate database integrity and transaction controls where required.

## 20. Abuse and Rate Limiting

Consider controls against repeated authentication attempts, API abuse, enumeration, repeated order submissions, excessive file uploads, expensive endpoints, and notification abuse. Rate limiting may be required, but this skill does not select a specific implementation or infrastructure.

## 21. CORS, CSRF, Cookies, and Browser Security

Explicitly configure CORS; do not allow permissive origins unnecessarily. Apply CSRF protection appropriate to the eventual authentication mechanism. If cookies are used, configure their security attributes appropriately. Require secure transport in production and do not expose credentials unnecessarily. Do not prescribe an authentication mechanism here.

## 22. Security Headers

Use appropriate security headers where applicable, such as Content-Security-Policy, X-Content-Type-Options, Referrer-Policy, frame protection, and secure cookie attributes. Do not mandate an exact production header configuration before deployment architecture is finalized.

## 23. Dependency and Supply-Chain Security

Minimize dependencies, review them before adoption, avoid abandoned or untrusted packages, keep security-sensitive dependencies updated, review dependency vulnerabilities, and control versions appropriately. Do not prescribe a specific dependency scanner.

## 24. Secure Django Practices

Use Django security features and do not disable protections without justification. Use the ORM safely, validate forms and serializers, configure production settings securely, never use `DEBUG=True` in production, and protect secret settings. If passwords are implemented later, use Django's secure password-handling facilities. Do not define final deployment configuration here.

## 25. Security Testing

Include negative as well as successful cases. Test unauthorized access, cross-tenant access, object-level authorization, privilege escalation, tenant reassignment, malicious input, relevant injection attempts, file-upload validation, sensitive-data exposure, authentication failures once authentication exists, and important administrative operations.

## 26. Security Review Checklist

Before completing security-sensitive work, ask:

- Who is the actor? Is the actor authenticated where required and authorized for this operation?
- Which shop / tenant does the operation belong to?
- Can another shop access this data or operation?
- Can a client manipulate ownership or gain access by guessing an ID?
- Can related objects leak information?
- Can input cause injection or unsafe execution?
- Could errors leak sensitive information? Are secrets exposed?
- Do logs expose sensitive data?
- Are concurrent requests safe?
- Are relevant negative security tests present?

## 27. AI Agent Security Workflow

Before implementing security-sensitive functionality, the AI agent MUST:

1. Read `AGENTS.md`.
2. Read `.ai/project-context/product.md`.
3. Read the relevant domain documentation.
4. Read `.ai/skills/django/SKILL.md`.
5. Read `.ai/skills/drf/SKILL.md` when APIs are involved.
6. Read `.ai/skills/api-design/SKILL.md` when API contracts are involved.
7. Read `.ai/skills/database-design/SKILL.md` when schema or database changes are involved.
8. Read `.ai/skills/multi-tenancy/SKILL.md` when tenant-scoped functionality is involved.
9. Identify trust boundaries and sensitive data.
10. Identify authorization requirements and possible abuse cases.
11. Design positive and negative security tests.
12. Ask for clarification if security behavior is ambiguous.
13. Only then implement.

## 28. Git Workflow

Follow the repository's mandatory task-based Git workflow:

```text
git status
git checkout main
git pull origin main
git checkout -b <task-id>/<short-description>
```

Never work directly on `main`. Inspect existing changes first; do not discard them automatically. Destructive Git commands require explicit approval. Ask for a task ID before creating a new task branch when one is not provided. Keep commits small and task-related, never commit secrets, push the task branch, and create a PR to `main`. Do not force-push or rewrite history without authorization. Follow `AGENTS.md` for the complete workflow.

## 29. AI Agent Rules

AI coding agents MUST:

- Never bypass authorization for convenience.
- Never trust client-controlled ownership fields.
- Never expose secrets or log credentials and tokens.
- Never disable security protections without explicit justification.
- Never assume authentication means authorization or that IDs provide security.
- Never assume frontend validation is sufficient.
- Never expose cross-tenant data or weaken security to make tests pass.
- Never invent security architecture.
- Ask when security requirements are ambiguous.

## 30. What This Skill Does Not Define

This skill does not define the authentication mechanism or provider, User model, role model, final authorization matrix, permission classes, Shop or Membership model, actual API endpoints or database models, specific infrastructure or security services, final deployment security architecture, or business workflows. Define these separately through approved project, architecture, and domain documentation.

## 31. Relationship With Other Skills

This skill works with:

```text
.ai/skills/django/
.ai/skills/drf/
.ai/skills/database-design/
.ai/skills/api-design/
.ai/skills/multi-tenancy/
.ai/skills/testing/
```

Security requirements apply across all of these skills. Keep them consistent with `AGENTS.md` and `.ai/project-context/product.md`.

## Final Requirement

Create only `.ai/skills/security/SKILL.md`.

Do not modify application code, create models, migrations, APIs, authentication, permissions, or infrastructure. Do not define the final authentication architecture or authorization matrix.
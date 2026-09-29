---
name: testing
description: "Use when designing, writing, organizing, or reviewing tests for the Grocery Platform."
---

# Testing Skill

## 1. Purpose

Automated testing is a required part of engineering, not an optional final step. Tests protect business correctness, API contracts, database integrity, tenant isolation, security, and regression prevention.

## 2. Testing Principles

- Test observable behavior rather than implementation details.
- Prefer deterministic, repeatable tests with explicit setup.
- Isolate tests appropriately and keep them readable.
- Avoid unnecessary mocking and brittle assertions.
- Test important negative cases as well as successful cases.
- Consider a regression test for every bug fix.
- Do not weaken production behavior merely to make tests pass.

## 3. Testing Pyramid

Use each test level where it provides useful confidence:

- Unit tests for focused logic.
- Integration tests for interactions between application components.
- API tests for HTTP contracts and behavior.
- Database tests for constraints, relationships, and transactional behavior.
- Security tests for authorization and trust boundaries.
- End-to-end tests where a complete user workflow needs validation.

Choose the appropriate mix for the change. Do not prescribe a percentage distribution.

## 4. Django Testing

Test models, model constraints and methods, services or domain logic, forms where applicable, management commands, and admin behavior where relevant. Test signals only when they are actually used. Prefer Django's supported testing facilities unless there is a justified reason to use another approach.

## 5. DRF/API Testing

For APIs that exist, test request validation, successful responses, status codes, response structure, invalid input, missing required fields, unsupported methods, authentication behavior once implemented, authorization, object-level access, pagination, filtering or searching where implemented, error responses, and tenant isolation. Do not define actual endpoints in this skill.

## 6. Business Rule Testing

Test documented business rules at the appropriate layer, including valid and invalid state transitions, required conditions, boundary conditions, domain invariants, ownership rules, and historical behavior where relevant. Do not invent Grocery Platform workflows that have not been finalized.

## 7. Multi-Tenant Testing

Tenant isolation is a mandatory security test area. Every tenant-scoped domain should cover:

**Positive cases:**

- A merchant can access their own shop data.
- A merchant can create and update allowed data for their shop.
- A merchant can perform authorized workflows.

**Negative cases:**

- Merchant A cannot list, retrieve, update, or delete Shop B data.
- Merchant A cannot access Shop B related objects or change an object's shop ownership.
- Customer data cannot leak between shops.

Test background jobs, analytics, notifications, and management commands when those features exist. Follow `.ai/skills/multi-tenancy/SKILL.md`.

## 8. Security Testing

Include negative security cases for unauthorized access, privilege escalation, object-level authorization, tenant-boundary violations, malicious input, injection risks where applicable, sensitive-data exposure, file-upload validation, unsafe ownership changes, and administrative access. Follow `.ai/skills/security/SKILL.md`.

## 9. Database Testing

Test important database guarantees, including required fields, uniqueness and tenant-scoped uniqueness, check constraints, foreign-key relationships, deletion behavior, transactional behavior, and concurrency-sensitive behavior where appropriate. Verify actual database behavior, not only Python validation. Follow `.ai/skills/database-design/SKILL.md`.

## 10. Fixtures and Test Data

Keep test data minimal, readable, and representative of documented domain relationships. Avoid unnecessary duplication, production data, real secrets, and sensitive customer information. Make tenant boundaries explicit in multi-tenancy tests.

Use factories, fixtures, or helpers only when they improve maintainability. Avoid large global fixtures that make individual tests difficult to understand. Do not mandate a third-party factory library.

## 11. Mocking

Prefer real application components when testing database behavior, serializers, domain validation, authorization logic, and tenant isolation. Mock external systems where appropriate, such as third-party APIs, external notification or payment providers if introduced, or external storage when integration testing it is unnecessary. Do not mock the behavior under test.

## 12. Transactions and Concurrency Testing

Test concurrent behavior when race conditions matter, such as duplicate submissions, inventory modifications, state transitions, ownership changes, or unique constraints. A single sequential test does not prove concurrency safety.

## 13. Error and Edge-Case Testing

Cover relevant empty, missing, invalid, duplicate, nonexistent, unauthorized, invalid-state, conflicting-state, malformed, and boundary-value cases, including maximum and minimum values where applicable. Do not create arbitrary edge cases unrelated to the documented domain.

## 14. API Contract Testing

Verify contracts established by the API Design and DRF skills. Cover request and response fields, status codes, validation errors, pagination, filtering, ordering, authentication and authorization behavior, and backward compatibility where applicable. Avoid over-testing irrelevant response-format details.

## 15. Regression Testing

When fixing a defect:

1. Reproduce it with a test where practical.
2. Implement the fix.
3. Where feasible, confirm the regression test fails before the fix and passes afterward.
4. Run relevant existing tests.

Treat a bug fix without appropriate regression coverage carefully.

## 16. Test Naming

Name tests to describe behavior. Prefer `test_merchant_cannot_access_another_shop_order` over `test_order_1`. A failure should be understandable without reading the implementation first.

## 17. Test Organization

Keep tests close to the relevant domain/application, logically grouped, and easy to discover. Separate tests by concern when the suite grows. Let the exact structure evolve with project size; do not impose unnecessary test-directory complexity.

## 18. Test Isolation and Cleanup

Tests must not depend on execution order, another test's database state, local machine state, developer-specific configuration, production resources, or manually created external data. Each test must establish the state it requires and clean up appropriately.

## 19. External Services

Test external integrations at appropriate levels: unit tests with controlled mocks or stubs, integration tests where valuable, and failure cases such as timeouts, errors, and malformed external responses. Do not make the whole suite depend on live external services unless tests are specifically designated as integration tests.

## 20. Performance-Aware Testing

Use tests to identify obvious N+1 queries, inefficient query patterns, repeated database access, unbounded result sets, and expensive operations. Do not turn every unit test into a performance benchmark. Add performance-specific tests where domain and query behavior warrant them.

## 21. Migration Testing

When migrations are introduced, verify they apply successfully, have correct dependencies, and handle data migrations carefully. Verify important constraints and do not make destructive migrations without explicit approval. Do not create migrations for models that have not been finalized.

## 22. Test Coverage

Coverage is a useful signal, not the sole measure of quality. Do not optimize blindly for a percentage. Prioritize security boundaries, business-critical logic, tenant isolation, authorization, database constraints, important API contracts, and high-risk workflows.

## 23. Running Tests

Before completing a change, run focused tests relevant to it and broader tests when appropriate. Report failures honestly, distinguish existing failures from failures introduced by the change, and do not skip failing tests without justification. Do not prescribe exact commands where project tooling is not finalized.

## 24. Test-Driven Development / Implementation Order

Do not mandate TDD for every task. Use tests before or alongside implementation when useful. For complex business rules, define expected behavior before implementation; for bug fixes, prefer regression tests; and for security boundaries, define negative cases explicitly.

## 25. AI Agent Testing Workflow

Before implementing a change, an AI coding agent MUST:

1. Read `AGENTS.md`.
2. Read `.ai/project-context/product.md`.
3. Read the relevant domain documentation.
4. Read `.ai/skills/django/SKILL.md`.
5. Read `.ai/skills/drf/SKILL.md` when APIs are involved.
6. Read `.ai/skills/api-design/SKILL.md` when API contracts are involved.
7. Read `.ai/skills/database-design/SKILL.md` when schema changes are involved.
8. Read `.ai/skills/multi-tenancy/SKILL.md` when tenant-scoped behavior is involved.
9. Read `.ai/skills/security/SKILL.md` when security-sensitive behavior is involved.
10. Identify positive cases.
11. Identify negative cases.
12. Identify boundary and edge cases.
13. Identify regression risks.
14. Implement appropriate tests.
15. Run the relevant test suite.
16. Report test results.
17. Ask for clarification if expected behavior is ambiguous.

## 26. Git Workflow

Follow the repository's mandatory task-based Git workflow:

```text
git status
git checkout main
git pull origin main
git checkout -b <task-id>/<short-description>
```

Never work directly on `main`. Inspect existing changes first and do not discard them automatically. Destructive Git commands require explicit approval. Ask for a task ID when one is required but not provided. Keep commits small and task-related, never commit secrets, push the task branch, and create a PR to `main`. Do not force-push or rewrite history without authorization. Follow `AGENTS.md` for the complete workflow.

## 27. AI Agent Rules

AI coding agents MUST:

- Never skip relevant tests merely to make a task pass.
- Never remove tests because they expose a real defect.
- Never weaken security behavior to satisfy a test.
- Never invent expected behavior or test implementation details unnecessarily.
- Always consider negative cases and tenant isolation for tenant-scoped functionality.
- Add regression coverage for important bug fixes.
- Report test failures honestly and distinguish environment failures from application failures.
- Ask when expected behavior is ambiguous.

## 28. What This Skill Does Not Define

This skill does not define actual domain models or API endpoints, authentication implementation, the final authorization matrix, specific permission classes, exact business workflows, production infrastructure, third-party testing libraries, the final CI/CD pipeline, or a specific coverage percentage.

## 29. Relationship With Other Skills

This skill works with:

```text
django/
drf/
database-design/
api-design/
multi-tenancy/
security/
```

Testing validates behavior and constraints established by those skills. Keep tests and guidance consistent with `AGENTS.md` and approved project and domain documentation.

## Final Requirement

Create only `.ai/skills/testing/SKILL.md`. Do not modify application code, create models, migrations, APIs, authentication, permissions, or business workflows. Do not invent domain behavior that has not been approved.
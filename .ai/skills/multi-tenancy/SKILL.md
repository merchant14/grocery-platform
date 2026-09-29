---
name: multi-tenancy
description: "Use when designing or implementing shop-level tenant context, data isolation, or cross-tenant access protection."
---

# Multi-Tenancy Skill

## 1. Purpose

This skill establishes mandatory engineering rules for preventing cross-shop data access. The primary security boundary is the shop / tenant. Merchant-owned data is accessible only within the appropriate shop context. Super Admin has platform-wide access according to the approved authorization model.

## 2. Core Tenant Isolation Principle

A merchant must never read, modify, delete, or otherwise access another shop's tenant-owned data. This applies to REST APIs, Django views and Admin, background jobs, management commands, internal services, database queries, scheduled tasks, notifications, analytics, and other application workflows.

Enforce tenant isolation server-side. Frontend filtering is never a security boundary.

## 3. Tenant Context

Every tenant-scoped operation must have a trusted tenant context, derived from trusted server-side information such as the authenticated actor's authorized shop relationship or another approved server-side mechanism.

Do not trust client-provided `shop_id`, `tenant_id`, or `merchant_id` as proof of authorization. A client-provided shop identifier is only a resource reference until authorization verifies access.

## 4. Authentication Independence

The final authentication mechanism is not finalized. This skill does not prescribe JWT, session authentication, OAuth, API keys, custom authentication, or another specific implementation.

```text
Authentication identifies the actor.
Authorization determines which shops that actor may access.
Tenant isolation enforces that access at the data/query level.
```

The final authentication architecture will be defined separately.

## 5. Tenant Ownership

Every tenant-owned entity must have a clear ownership relationship to its shop / tenant. Before implementing a model, determine whether the entity belongs to a shop, can exist globally or across shops, who owns it, whether it can move between shops, what happens if the shop is deactivated, and what happens to historical records.

Do not assume every model needs a `shop` foreign key. Some entities may be platform-global. Domain specifications determine ownership.

## 6. Platform-Global vs Tenant-Owned Data

Distinguish platform-global data, intentionally shared across the platform, from tenant-owned data belonging to an individual shop.

Conceptual platform-global examples include platform configuration, master catalog information, platform-level campaign definitions, and platform analytics. Conceptual tenant-owned examples include merchant catalog configuration, shop-specific pricing, shop inventory, shop orders, shop customer identity, and shop-specific analytics.

These examples must follow final domain specifications. Do not turn them into models in this skill.

## 7. Queryset Isolation

Scope tenant-owned querysets to the authorized tenant context. Avoid `Model.objects.all()` for tenant-owned data. Prefer a server-derived scope, conceptually:

```python
Model.objects.filter(shop=authorized_shop)
```

The exact implementation depends on the final architecture. Tenant filtering must happen server-side and must not depend on the client supplying the correct shop ID.

## 8. Object-Level Authorization

Isolation applies to individual objects as well as list queries. For example, prevent `GET /api/v1/orders/{another_shop_order_id}/` even if an attacker knows or guesses the identifier.

Apply the same protection to retrieve, update, partial update, delete, workflow actions, related resources, and nested resources. An object identifier is not proof of authorization.

## 9. Create Operations

Do not let a client establish ownership by sending a `shop_id`. The server must determine or verify the authorized shop context. If a request is intentionally scoped to a shop, verify the authenticated actor may operate within it.

## 10. Update Operations

Before modifying tenant-owned data:

1. Resolve the target object within an appropriately scoped context.
2. Verify tenant ownership and access.
3. Verify the actor's authorization.
4. Perform the update.

Do not retrieve objects globally and rely on frontend restrictions. Avoid patterns that could update another tenant's record.

## 11. Delete Operations

Deletion must also be tenant-scoped. A merchant must never delete another shop's data by supplying its identifier. Before deletion, verify ownership and authorization and respect domain deletion rules, historical-data requirements, and database constraints. Do not assume every tenant-owned resource should be deletable.

## 12. Cross-Tenant Access Prevention

Explicitly protect against access such as Merchant A to Shop B data, Merchant B to Shop A data, a Shop A customer to Shop B customer data, or a Shop A API context to Shop B resources.

Tests must attempt unauthorized cross-tenant access and verify it is denied. Do not rely only on happy-path tests.

## 13. IDs Are Not Security

UUIDs and numeric IDs do not provide tenant isolation. `ID != Authorization`. Enforce authorization independently, even when resource identifiers are difficult to guess.

## 14. URL Tenant Scope

A URL may contain a shop identifier, such as `/api/v1/shops/{shop_id}/products/`, but the URL itself does not establish authorization. Verify the actor may access the shop.

Likewise, `/api/v1/orders/{order_id}/` must verify that the order belongs to an authorized shop before returning it.

## 15. Nested Resources

Enforce tenant isolation at every level of nested endpoints. For `/shops/{shop_id}/products/{product_id}`, verify both that the actor can access the shop and that the product belongs to that shop or is otherwise legitimately accessible in that context. URL parameters alone do not establish the relationship.

## 16. Related Objects

Maintain isolation through relationships. For example, access to a Shop A order must not allow a merchant to use its customer relationship to access another shop's customer data. Evaluate whether related objects cross tenant boundaries.

## 17. Shared / Master Data

Some platform data may intentionally be global. For example, the platform may maintain a master catalog while shops maintain their own catalog configuration. Authorized tenants may read global data where product requirements allow it.

Global visibility does not make tenant-owned modifications global. A merchant modifying a shop-specific representation must not accidentally modify platform-global master data. The exact master-catalog relationship belongs in the Catalog domain specification.

## 18. Customer Isolation

Customer identity is shop-specific according to the product requirements. Customer identity for Shop A is not automatically the identity for Shop B. Do not create a globally shared customer identity across merchants by assumption.

A customer's WhatsApp number must not expose another shop's customer history. Scope customer data according to the final Customer domain specification.

## 19. Analytics Isolation

Merchant analytics may access only data belonging to the merchant's authorized shop or shops. Platform analytics may aggregate across shops only when the actor has platform-level authorization. Do not expose platform-wide totals to ordinary merchants or infer tenant scope from frontend query parameters.

## 20. Background Jobs

Tenant isolation applies to asynchronous and background processing. Each tenant-scoped task must carry or resolve a trusted tenant context. Do not operate on tenant-owned data using only an unverified client-provided `shop_id`.

When a job receives an object identifier, it must still operate according to the object's authorized tenant context.

## 21. Notifications

Notifications must preserve tenant boundaries. A Shop A order must not accidentally trigger a Shop B merchant notification. Use trusted relationships from underlying domain objects, and validate recipient and shop context server-side rather than trusting client-provided identifiers.

## 22. Management Commands

Management commands may operate across tenants when explicitly designed as platform-level operations. Tenant-scoped commands must require explicit tenant context; platform-wide commands must be clearly identified. Do not accidentally run tenant-specific logic across every shop. Destructive commands require appropriate safeguards.

## 23. Django Admin

Django Admin does not automatically provide tenant isolation. If merchant users eventually receive admin access, scope their accessible objects appropriately. Super Admin may have platform-wide access according to the final authorization design. The final Admin implementation belongs in the relevant application and security design.

## 24. Data Integrity

Where appropriate, database relationships and constraints should support tenant isolation. Consider ownership relationships, uniqueness scoped by shop, foreign keys, composite uniqueness, and preventing cross-tenant relationships.

Do not assume global `unique=True` is correct for tenant-owned data. A value may need to be unique within a shop rather than across the platform. Exact constraints belong in domain and database specifications.

## 25. Tenant-Scoped Uniqueness

When a business value only needs to be unique within a shop, model uniqueness conceptually as `(shop, value)` rather than assuming `value` is globally unique. Add tenant-scoped uniqueness only when the domain requires it.

## 26. Tenant Context Must Not Be Mutable by Clients

Clients must not move records between shops by changing `shop_id`, `tenant_id`, or `merchant_id` through an API update. A move between tenants, if ever allowed, must be an explicitly authorized domain operation. Do not expose generic PATCH behavior that permits unauthorized tenant reassignment.

## 27. Security Boundary

Tenant isolation is a security requirement, not merely a query optimization. Any implementation that lets Merchant A read or write Shop B data is a security defect. Treat cross-tenant access vulnerabilities as high priority.

## 28. Testing Tenant Isolation

Every tenant-scoped domain should test:

- Positive cases: an authorized merchant accesses, creates, updates, and performs allowed workflows on their own shop data.
- Negative cases: a merchant cannot retrieve, update, delete, or list another shop's data; change ownership; or access another shop's customer data.
- Background cases: tenant-scoped background operations cannot cross shops.
- Platform-level cases: an authorized Super Admin can access platform-wide data, while merchants cannot access privileged platform data unless explicitly allowed.

## 29. API Design Requirements

API contracts should clearly identify whether an endpoint is platform-wide, shop-scoped, object-scoped, public/customer-facing, merchant-only, or Super-Admin-only. A client-supplied shop ID alone never establishes access.

Follow `.ai/skills/api-design/` and `.ai/skills/drf/` for API contract and implementation standards.

## 30. Service / Domain Logic

Perform tenant validation at the appropriate domain boundary. Do not rely on every caller remembering to perform a manual tenant check. Centralize tenant-sensitive behavior for complex domain operations where appropriate, but do not create unnecessary abstraction layers solely for tenant filtering. Follow the project's Django architecture and domain specifications.

## 31. Query Review

When implementing tenant-owned functionality, review list, detail, create, update, delete, related-object, aggregation, and background queries. Ask:

> Can this query ever return or modify data belonging to another shop?

If the answer is potentially yes, the implementation is not complete.

## 32. AI Agent Workflow

Before implementing tenant-scoped functionality, an AI agent MUST:

1. Read `AGENTS.md`.
2. Read `.ai/project-context/product.md`.
3. Read the relevant domain documentation.
4. Read `.ai/skills/django/SKILL.md`.
5. Read `.ai/skills/drf/SKILL.md` when APIs are involved.
6. Read `.ai/skills/api-design/SKILL.md` when API contracts are involved.
7. Read `.ai/skills/database-design/SKILL.md` when schema changes are involved.
8. Determine whether data is platform-global or tenant-owned.
9. Determine how tenant context is established.
10. Verify authorization requirements.
11. Design positive and cross-tenant negative tests.
12. Only then implement the change.

If tenant ownership or authorization behavior is ambiguous, ask before implementation.

## 33. Git Workflow

Follow the repository's mandatory task-based Git workflow. Before making code changes:

```text
git status
git checkout main
git pull origin main
git checkout -b <task-id>/<short-description>
```

Do not work directly on `main`. Inspect existing working-tree changes first; do not discard them automatically or use destructive Git commands without explicit approval. If no task ID is provided for a new task, ask for it before creating the branch. Follow the complete Git workflow defined by the repository and `AGENTS.md`.

## 34. AI Agent Rules

AI coding agents MUST:

- Treat tenant isolation as a security boundary.
- Never trust client-provided `shop_id` as authorization.
- Never use unscoped querysets for tenant-owned resources.
- Never assume object IDs provide security.
- Never allow unauthorized tenant reassignment.
- Never expose cross-tenant related objects.
- Never assume frontend filtering provides isolation.
- Consider list, detail, create, update, delete, and workflow operations.
- Test cross-tenant access explicitly.
- Distinguish platform-global data from tenant-owned data.
- Never invent tenant relationships or change tenant-isolation architecture without approval.
- Ask for clarification when ownership, scope, or authorization is ambiguous.

## 35. What This Skill Does Not Define

This skill does not define the authentication mechanism, user model, final role model, shop model or membership implementation, JWT/session/OAuth implementation, specific permission classes, actual database schema or API endpoints, customer/order/catalog/inventory schemas, final authorization matrix, or specific business workflows. Define those in relevant architecture, security, database, API, and domain specifications.

## 36. Relationship With Other Skills

This skill works together with:

```text
.ai/skills/django/
.ai/skills/drf/
.ai/skills/database-design/
.ai/skills/api-design/
.ai/skills/security/
.ai/skills/testing/
```

Responsibilities:

```text
django/           General Django engineering
drf/              DRF implementation
database-design/  Database and schema design
api-design/       REST API contracts
multi-tenancy/    Tenant isolation
security/         Security requirements
testing/          Testing standards
```

All skills must remain consistent with `AGENTS.md` and the project's canonical product and domain documentation.

## Final Requirement

Create only `.ai/skills/multi-tenancy/SKILL.md`. Do not modify application code, create models, migrations, API endpoints, authentication, or permissions; do not define the final authorization matrix, Grocery Platform business workflows, or a specific authentication mechanism.
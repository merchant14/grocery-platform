---
name: drf
description: "Use when designing or implementing REST APIs with Django REST Framework in this repository."
---

# Django REST Framework Skill

## 1. Purpose

This skill defines the standard approach for building REST APIs with Django, Django REST Framework (DRF), and PostgreSQL. The backend follows a modular monolith architecture. APIs use the versioned prefix `/api/v1/`.

## 2. API Design Principles

APIs should be consistent, predictable, explicit, resource-oriented, versioned, secure, testable, and backward-conscious. Do not introduce GraphQL, gRPC, or another API architecture unless explicitly approved.

## 3. API Versioning

Use `/api/v1/` as the standard API prefix. Future breaking API changes should use a new API version when required. Do not introduce unnecessary versioning mechanisms or version numbers inside individual application names.

## 4. Views and ViewSets

Choose DRF views according to endpoint complexity:

- Use `ModelViewSet` for standard CRUD resources when all standard operations are appropriate.
- Use `ReadOnlyModelViewSet` when a resource is intentionally read-only through the API.
- Use `APIView` when an operation does not naturally map to standard CRUD behavior or requires a specialized workflow.
- Use `@action` when an operation belongs naturally to an existing resource but is not standard CRUD.

Do not use `APIView` everywhere by default. Do not use `ModelViewSet` simply for convenience when a resource requires significantly different behavior.

## 5. Serializers

Serializers handle API representation and input validation, including request validation, response serialization, field-level and object-level validation, and nested representation where appropriate. Do not put large business workflows or unrelated domain operations inside serializers. Delegate complex workflows to appropriate domain or service logic.

## 6. Validation

Validate input at the API boundary. Validation should cover required fields, data types, allowed values, formats, cross-field validation, and domain constraints where appropriate. Do not rely only on frontend validation; treat all client input as untrusted. Where a rule is fundamentally a database invariant, enforce it at the database level where appropriate.

## 7. Business Logic

Keep API views thin. A typical request flow is:

```text
HTTP Request
    ↓
URL routing
    ↓
Authentication
    ↓
Permission checks
    ↓
Serializer validation
    ↓
Domain/business operation
    ↓
Database
    ↓
Serializer
    ↓
HTTP Response
```

Do not place large business workflows in URL configuration, views, or serializers. Use domain or service logic when the workflow is complex enough to justify it. Do not introduce service classes for trivial CRUD operations.

## 8. Authentication and Permissions

Authentication and authorization are separate concerns. Endpoints must not rely on authentication alone; authorization must determine whether the authenticated actor can perform the requested operation.

For tenant-owned resources, never trust a client-provided `shop_id` as proof of access. The server must derive or verify tenant ownership from trusted authentication or context.

The exact authentication mechanism is not finalized. Do not implement or prescribe JWT, session authentication, OAuth, or a custom authentication mechanism in this skill. Follow the approved authentication and security architecture when finalized.

## 9. Multi-Tenant API Safety

The Grocery Platform is multi-tenant at the shop level. Merchant requests must not access another merchant's shop-owned data. Do not use an unscoped `Model.objects.all()` queryset for a tenant-owned resource. Enforce tenant filtering server-side; a frontend-provided `shop_id` must never be the sole authorization mechanism.

The final multi-tenancy implementation will be defined separately in `.ai/skills/multi-tenancy/` and the relevant domain specifications.

## 10. Querysets

Scope querysets intentionally. Avoid `Model.objects.all()` when an endpoint should expose only a subset of records. Use appropriate filtering, ordering, `select_related()`, `prefetch_related()`, and pagination. Avoid N+1 queries. Optimize based on actual query requirements rather than blindly.

## 11. HTTP Methods

Use HTTP methods according to their intended semantics:

```text
GET     → retrieve/read
POST    → create
PUT     → full replacement
PATCH   → partial update
DELETE  → delete
```

Do not use `POST` for every operation for convenience. Use an explicit API design for workflow operations that are not standard CRUD.

## 12. HTTP Status Codes

Use meaningful status codes that accurately represent the result. Typical examples include `200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`, and `500 Internal Server Error`. Do not return `200 OK` for every outcome or expose internal exception details in API responses.

## 13. Error Responses

API errors should be consistent and machine-readable. Validation errors should identify affected fields where appropriate. Do not expose stack traces, database credentials, internal secrets, authentication tokens, or sensitive implementation details. The standardized API error format will be documented separately once finalized; do not invent a custom schema in this skill.

## 14. Pagination

Paginate collection endpoints when result sets can become large. Do not return unlimited records by default. Follow the approved API specification for pagination strategy and response format. Do not introduce multiple pagination mechanisms without a documented reason.

## 15. Filtering, Searching, and Ordering

Collection endpoints may support filtering, searching, and ordering where useful. Make these capabilities explicit, documented, validated, and scoped to authorized data. Do not expose arbitrary database fields for filtering or ordering without considering security and performance.

## 16. URLs and Routing

Use clear REST-oriented URL structures and resource names rather than implementation details. For example:

```text
/api/v1/shops/
/api/v1/products/
/api/v1/orders/
```

Avoid action-oriented URLs such as `/api/v1/get-products/`, `/api/v1/create-order/`, or `/api/v1/delete-product/`; normally, the HTTP method communicates the operation. Use nested resources only when the relationship is meaningful and improves clarity. Avoid unnecessarily deep URL nesting.

## 17. API Naming

Use lowercase URL paths, plural resource names where appropriate, and consistent naming. Use hyphenated path segments when needed. Python code should continue using `snake_case`. Do not expose Python implementation details in API URLs.

## 18. Response Design

Responses should be predictable and consistent. Do not expose Django model objects directly. Serialize responses through DRF serializers or an explicitly approved response structure. Avoid unnecessary fields and do not expose internal database fields merely because they exist.

## 19. Authentication Context

When behavior depends on the authenticated actor, use trusted server-side authentication context. Do not accept client-provided `user_id`, `merchant_id`, `shop_id`, or `role` as authoritative identity or authorization information when it should come from authentication context. Client-provided identifiers may be used as resource references only after authorization checks.

## 20. Transactions

Use database transactions for API operations that perform multiple related writes which must succeed or fail together. For example:

```python
from django.db import transaction

with transaction.atomic():
    ...
```

Do not wrap every endpoint in a transaction unnecessarily. Complex transactional workflows should live in domain or service logic rather than making the view responsible for transaction orchestration.

## 21. Performance

Avoid N+1 queries, unnecessary database calls, loading entire tables, returning huge collections, and repeated queries inside loops. Use `select_related()`, `prefetch_related()`, `values()`, `values_list()`, `exists()`, and `count()` where appropriate. Keep performance optimizations understandable.

## 22. Security

DRF APIs must validate client input, enforce authentication where required, enforce authorization and tenant isolation, avoid exposing sensitive fields, avoid leaking internal errors, avoid logging secrets or tokens, use secure configuration, and protect state-changing endpoints according to the chosen authentication mechanism. Never assume frontend restrictions provide security.

## 23. Testing APIs

API tests should cover relevant:

- Success cases: valid request, expected response, and expected database state.
- Validation cases: missing required fields, invalid values or formats, and invalid combinations.
- Authorization cases: unauthenticated requests, unauthorized actors, authorized actors, and cross-tenant access attempts.
- Edge cases: resource not found, duplicate operations, invalid state transitions, and concurrent or conflicting operations where relevant.

Tests should verify both HTTP behavior and important database effects.

## 24. API Documentation

Every finalized API should eventually document its HTTP method, URL, authentication requirements, permissions, request parameters and body, response body, HTTP status codes, validation errors, and important edge cases. Keep API documentation in the appropriate project documentation area. Do not unnecessarily duplicate business rules between API and domain documentation.

## 25. API Development Workflow

Before implementing an API:

1. Read `AGENTS.md`.
2. Read `.ai/project-context/product.md`.
3. Read the relevant domain documentation.
4. Read the relevant Django skill.
5. Read relevant multi-tenancy, security, and API documentation when available.
6. Confirm the API behavior is defined.
7. Ask before implementing if business behavior is ambiguous.
8. Implement the smallest appropriate API.
9. Add or update tests.
10. Run Django checks.
11. Review database and query behavior.
12. Review authorization and tenant isolation.
13. Update API documentation if the contract changed.

## 26. Git Workflow

Follow the repository's mandatory task-based Git workflow. Before making code changes:

```text
git status
git checkout main
git pull origin main
git checkout -b <task-id>/<short-description>
```

Do not work directly on `main`. If the working tree contains existing changes, inspect them first; do not discard them automatically or run destructive Git commands without explicit approval. If no task ID is provided for a new development task, ask for it before creating the branch. Follow the complete Git workflow defined in the repository's development skills and `AGENTS.md`.

## 27. AI Agent Rules

AI coding agents MUST:

- Read relevant project documentation before implementation.
- Never invent API behavior or business rules.
- Never bypass authorization for convenience.
- Never trust client-provided tenant context.
- Never expose sensitive model fields automatically.
- Never create unnecessary endpoints or add custom frameworks without approval.
- Never modify unrelated APIs.
- Add tests for meaningful API behavior.
- Keep API changes focused on the requested task.
- Ask for clarification when API behavior affects business rules, authorization, database design, or tenant isolation.

## 28. What This Skill Does Not Define

This skill does not define specific Grocery Platform endpoints, final API request or response schemas, the authentication mechanism, the final authorization model or multi-tenancy implementation, user roles, shop/product/inventory/customer/cart/order/campaign/notification/analytics models, or business workflows. Define those in the relevant project or domain documentation.

## 29. Relationship With Other Skills

This DRF skill works together with:

```text
.ai/skills/django/
.ai/skills/database-design/
.ai/skills/api-design/
.ai/skills/multi-tenancy/
.ai/skills/security/
.ai/skills/testing/
```

This skill focuses specifically on Django REST Framework implementation standards. When another approved skill provides more specific guidance, follow it while remaining consistent with `AGENTS.md` and the project's canonical product and domain documentation.

## Final Requirement

Create only `.ai/skills/drf/SKILL.md`. Do not modify application code, create API endpoints, serializers, views, models, or migrations, or implement authentication or permissions.
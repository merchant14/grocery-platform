---
name: api-design
description: "Use when designing REST API contracts for the Grocery Platform, independent of their DRF implementation."
---

# API Design Skill

## 1. Purpose

This skill establishes consistent REST API contract-design standards for the project. APIs should be resource-oriented, predictable, consistent, explicit, versioned, secure, backward-conscious, and easy for frontend and backend teams and AI coding agents to consume. The version prefix is `/api/v1/`; Django REST Framework is used for implementation.

## 2. API Contract First

Design the API contract before implementation when an endpoint represents a meaningful domain operation. Define its HTTP method, URL, authentication and authorization requirements, path and query parameters, request and response bodies, success status codes, error responses, validation behavior, and important edge cases.

Do not implement an API from a vague feature description. Clarify ambiguous behavior before implementation.

## 3. REST Resource Design

Design APIs around resources rather than implementation functions. Prefer:

```text
GET    /api/v1/products/
POST   /api/v1/products/
GET    /api/v1/products/{id}/
PATCH  /api/v1/products/{id}/
DELETE /api/v1/products/{id}/
```

Avoid action-oriented paths such as `/api/v1/get-products/`, `/api/v1/create-product/`, `/api/v1/update-product/`, and `/api/v1/delete-product/`. Normally, the HTTP method communicates the operation.

## 4. Resource Naming

Use lowercase URLs, plural resource names where appropriate, consistent naming, and hyphenated path segments when needed. For example:

```text
/api/v1/shops/
/api/v1/products/
/api/v1/orders/
```

Do not expose Python class names or internal implementation details through URLs.

## 5. Resource Identity

Resources should have a stable identifier without exposing internal implementation details unnecessarily. The project's primary-key strategy is not finalized. Do not prescribe integer IDs, UUIDs, or another strategy here; use the identifier strategy defined by database and domain architecture once finalized.

## 6. HTTP Method Semantics

Use HTTP methods according to their intended meaning:

```text
GET     Read
POST    Create
PUT     Full replacement
PATCH   Partial update
DELETE  Delete
```

Do not use `POST` for every operation simply because it is convenient. For non-CRUD domain operations, design an explicit workflow endpoint.

## 7. CRUD vs Workflow APIs

Use resource-oriented endpoints for standard CRUD operations. Not every business operation is CRUD. A domain may eventually have operations conceptually similar to `accept`, `reject`, `cancel`, `complete`, `publish`, or `approve`.

Do not automatically represent a meaningful domain command or state transition as an arbitrary field update such as `PATCH /resource/{id}/` with `{"status": "..."}`. Design an explicit workflow API where appropriate. Actual Grocery Platform workflows belong in domain specifications, not this skill.

## 8. State Transitions

For resources with a lifecycle or state machine, document valid states, valid transitions, who may perform each transition, invalid transitions, and expected API behavior for invalid transitions. Do not let clients arbitrarily change protected state fields merely because a field exists in a serializer. Actual state machines belong in domain documentation.

## 9. Nested Resources

Use nested URLs only when the relationship is meaningful and improves API clarity. For example, `/api/v1/shops/{shop_id}/products/` may be appropriate when an operation is explicitly scoped to a shop.

Avoid excessive nesting, such as `/api/v1/shops/{shop_id}/categories/{category_id}/products/{product_id}/variants/`, when a simpler resource URL provides the same clarity. Do not create nested URLs solely because database relationships are nested.

## 10. Query Parameters

Use query parameters for collection behavior such as filtering, searching, ordering, and pagination. For example:

```text
/api/v1/products/?category=...
/api/v1/orders/?status=...
```

Query parameters should be explicit, documented, validated, authorization-aware, and consistent. Do not expose arbitrary model fields as query parameters.

## 11. Filtering

Filtering should represent meaningful domain or query behavior. Concepts may include status, category, availability, date range, or shop, but actual supported filters must be defined by the endpoint or domain specification. Do not expose every database field automatically.

## 12. Searching

Design search intentionally and document the parameter name, fields searched, matching behavior, case sensitivity where relevant, support for partial matching, and performance characteristics where important. Do not implement unrestricted database-wide search through arbitrary query parameters.

## 13. Ordering

Expose only approved ordering fields. For example, `/api/v1/products/?ordering=name`. Do not expose arbitrary database expressions or internal fields. Clearly document the syntax if multiple ordering fields are supported.

## 14. Pagination Contract

Use pagination for collection APIs when result sets may become large. The contract must define page-size behavior, default and maximum page sizes, how the client requests another page, response metadata, and collection structure.

Do not return unlimited collections by default. The exact pagination implementation will be finalized separately; do not invent a pagination response format here.

## 15. Request Bodies

Request bodies should contain only fields the client is allowed to provide. Do not expose internal fields merely because they exist in a model. Client requests should not automatically be allowed to set server- or workflow-controlled fields such as `created_at`, `updated_at`, `shop_id`, `user_id`, `role`, or `internal_status`.

## 16. Server-Owned Fields

Distinguish client-controlled fields from server-controlled fields. Server-controlled values are determined by authentication context, tenant context, business rules, the database, server-generated timestamps, or workflow logic. Clients must not override server-controlled values.

## 17. Multi-Tenant API Contracts

The platform is multi-tenant at the shop level. Contracts must make tenant scope clear without trusting client input as authorization. A request containing `shop_id` does not automatically grant access to that shop; the server must verify the authenticated actor has access.

The final implementation belongs in `.ai/skills/multi-tenancy/` and domain specifications.

## 18. Authentication and Authorization

Every protected API contract should document:

```text
Authentication:
Required / Not required

Authorization:
Who can perform this operation
```

Authentication identifies the actor; authorization determines whether that actor can perform the operation. Do not treat them as the same concern. The authentication mechanism is not finalized. Do not prescribe JWT, sessions, OAuth, or another mechanism here.

## 19. API Response Design

Responses should be predictable, consistent, explicit, and minimal but sufficient. Return only fields required by the contract, not entire database records by default. Avoid leaking internal IDs that should not be public, secrets, tokens, internal implementation details, or sensitive fields.

Define the exact response-envelope strategy consistently across the project. Do not invent a project-wide envelope format without approval.

## 20. Collection vs Detail Responses

Collection and detail responses may differ when justified, such as returning a smaller representation in a list and additional information in a detail response. Make differences intentional and documented. Do not create inconsistent representations for the same resource without a reason.

## 21. HTTP Status Codes

Use status codes according to their meaning. Common examples include `200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`, and `500 Internal Server Error`.

Do not return `200 OK` for every result. Choose status codes based on the operation and outcome.

## 22. Validation Errors

Validation errors should be predictable, machine-readable, field-specific where appropriate, and safe to expose. For example, this is an illustrative structure only:

```json
{
  "field": [
    "Human-readable validation message."
  ]
}
```

Do not finalize a project-wide error schema in this skill.

## 23. Business Errors

Where appropriate, distinguish business-rule failures from malformed requests. Conceptual examples include an invalid state transition, unavailable resource, duplicate business operation, or operation not permitted.

Document expected status behavior for important business errors. Do not expose internal exception messages directly.

## 24. Idempotency

Consider idempotency where duplicate requests could cause unintended side effects, such as creating an important transaction, retrying a network request, triggering an external notification, or handling a future payment-related operation. Do not introduce an idempotency-key mechanism automatically for every endpoint.

When idempotency is required, document which operations are idempotent, how duplicates are identified, expected retry behavior, and how long idempotency information is retained where applicable.

## 25. Concurrency

Contracts for state-changing operations should consider concurrent requests, such as two clients attempting the same transition. Define deterministic API behavior. Where correctness depends on concurrency control, use appropriate database transactions and constraints. Do not rely only on frontend behavior to prevent conflicts.

## 26. Partial Updates

Use `PATCH` for partial updates where appropriate. Document which fields may and may not be updated, validation behavior, whether omitted fields remain unchanged, and whether setting a field to null is allowed.

Do not allow clients to update protected workflow or state fields through generic PATCH behavior.

## 27. PUT vs PATCH

Use `PUT` when the contract represents full resource replacement and `PATCH` when it represents partial modification. Do not use them interchangeably without documenting the semantics.

## 28. DELETE Semantics

Before defining DELETE behavior, determine whether the resource is deletable, whether deletion is physical or logical, what happens to related resources and historical records, and whether the operation should instead deactivate or archive the resource. Do not assume every resource should expose DELETE.

Soft-delete behavior is not defined by this skill; follow the relevant domain and database specification.

## 29. API Versioning

All APIs use `/api/v1/`. Do not silently make breaking changes to an existing contract. When a breaking change cannot be avoided, use an appropriate API versioning strategy. Avoid versioning every minor change; backward-compatible additions should generally remain in the existing version when possible.

## 30. Backward Compatibility

Consider existing clients before removing or renaming fields, changing field types or response structure, changing required request fields, status codes, error behavior, or endpoint semantics. Do not make breaking changes silently.

## 31. API Documentation

Document every finalized endpoint's method, URL, purpose, authentication, authorization, path and query parameters, request body, success response, error responses, status codes, validation rules, state transitions, and important edge cases.

Keep documentation synchronized with implementation. When a contract changes, update its documentation in the same task.

## 32. Frontend/Backend Contract

The API contract is the agreement between frontend and backend. Frontend developers should not have to infer field names, required fields, status values, error formats, pagination behavior, or allowed operations. Backend developers should not silently change contracts because a frontend implementation is inconvenient. Make and document contract changes intentionally.

## 33. API Design Workflow

Before designing an endpoint:

1. Read `AGENTS.md`.
2. Read `.ai/project-context/product.md`.
3. Read the relevant domain documentation.
4. Read `.ai/skills/django/SKILL.md`.
5. Read `.ai/skills/drf/SKILL.md`.
6. Read `.ai/skills/database-design/SKILL.md` when database behavior matters.
7. Read multi-tenancy and security documentation when relevant.
8. Identify the resource and operation.
9. Determine whether it is CRUD or a workflow operation.
10. Define authentication and authorization requirements.
11. Define request and response contracts.
12. Define validation behavior.
13. Define status codes and errors.
14. Consider concurrency and idempotency where relevant.
15. Document the contract.
16. Only then implement it.

If business behavior is ambiguous, ask before designing the API.

## 34. Git Workflow

Follow the repository's mandatory task-based Git workflow. Before making code changes:

```text
git status
git checkout main
git pull origin main
git checkout -b <task-id>/<short-description>
```

Do not work directly on `main`. Inspect existing working-tree changes before proceeding; do not discard them automatically or use destructive Git commands without explicit approval. If no task ID is provided for a new task, ask for it before creating the branch. Follow the complete Git workflow defined by the repository and `AGENTS.md`.

## 35. AI Agent Rules

AI coding agents MUST:

- Read relevant domain documentation before designing an API.
- Never invent business behavior or endpoint contracts when requirements are ambiguous.
- Never expose model fields automatically.
- Never trust client-provided tenant context or allow clients to control server-owned fields.
- Never create unnecessary endpoints.
- Never use POST for every operation for convenience.
- Never expose arbitrary database fields through filters or ordering.
- Never silently introduce breaking API changes or change a contract without understanding its consumers.
- Keep API contracts consistent across domains.
- Add or update API documentation when contracts change.
- Ask for clarification when API behavior, authorization, tenant scope, state transitions, or error semantics are unclear.

## 36. What This Skill Does Not Define

This skill does not define actual Grocery Platform endpoints or request/response schemas, the authentication mechanism or authorization implementation, user roles, domain APIs, actual business state machines, database schema, or final tenant-isolation implementation. Define those in the appropriate domain and project specifications.

## 37. Relationship With Other Skills

This API Design skill works together with:

```text
.ai/skills/django/
.ai/skills/drf/
.ai/skills/database-design/
.ai/skills/multi-tenancy/
.ai/skills/security/
.ai/skills/testing/
```

Responsibilities:

```text
django/          General Django engineering
drf/             Django REST Framework implementation
api-design/      REST API contract and design
database-design/ Database/schema design
multi-tenancy/   Tenant isolation architecture
security/        Security requirements
testing/         Testing standards
```

All skills must remain consistent with `AGENTS.md` and the project's canonical product and domain documentation.

## Final Requirement

Create only `.ai/skills/api-design/SKILL.md`. Do not modify application code, create API endpoints, serializers, views, models, or migrations, implement authentication or permissions, or define Grocery Platform business workflows.
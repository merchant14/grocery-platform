# AI Development Instructions

## 1. Project Overview

This repository contains the backend for a multi-tenant grocery-store platform. Its primary actors are Super Admins, Merchants / Shopkeepers, and Customers. The backend is developed as a Django modular monolith and is responsible for the platform's server-side application. Detailed product behavior is defined only in project and domain documentation.

## 2. Technology Stack

The approved technology stack is Python 3.12+, Django 5.x, Django REST Framework, PostgreSQL, Docker, and Git. Do not assume additional technologies have been approved.

## 3. Architecture

The backend follows a **Modular Monolith Architecture**. All current domains exist within one Django project, and Django apps represent business domains. The project is not using microservices at this stage. Keep domains logically separated and avoid unnecessary coupling between apps.

## 4. Django Application Structure

The current domain apps are:

```text
users
shops
catalog
inventory
customers
cart
orders
campaigns
notifications
analytics
```

Each app represents a business domain. Use standard Django conventions initially. Do not require custom `services/`, `repositories/`, `domain/`, or `interfaces/` folders in every app; introduce such structures only when a domain's complexity justifies them.

## 5. API Development Principles

- Use Django REST Framework and REST architecture.
- Version APIs under `/api/v1/`.
- Prefer class-based views.
- Use `ModelViewSet` for standard CRUD resources and `ReadOnlyModelViewSet` where appropriate.
- Use `APIView` or custom ViewSet actions for complex workflows.
- Use serializers for request and response validation.
- Keep complex business logic out of views.
- Do not define endpoints until requirements are documented.

## 6. Business Logic

Views should coordinate requests and responses; complex business workflows should not be implemented directly inside views. Place business logic in an appropriate domain-level service or module when complexity requires it. Do not require a service layer for every simple CRUD operation or add unnecessary abstractions.

## 7. Database Principles

- PostgreSQL is the primary database, and the Django ORM is the default database access layer.
- Use database constraints where appropriate.
- Model foreign keys and relationships to reflect documented business relationships.
- Add indexes based on actual query and access patterns.
- Do not introduce raw SQL without a documented technical reason.
- Commit database migrations to Git when application models are introduced.
- Do not define the database schema based on assumptions.

## 8. Multi-Tenancy

The platform is multi-tenant at the shop level. Merchant-owned data must be isolated by shop / tenant. A merchant must never be able to access or modify another merchant's shop data.

Never trust a client-provided `shop_id` as proof of authorization. Derive authorization from the authenticated user's relationship with the shop. The final tenancy implementation is not yet defined; follow documented decisions rather than inventing one.

## 9. Security

- Never commit secrets or `.env` files. Use `.env.example` to document configuration.
- Validate all client input and apply authorization on the server; never rely on frontend restrictions for security.
- Do not expose sensitive customer or merchant information unnecessarily.
- Do not log passwords, tokens, credentials, or sensitive personal information.
- Follow least-privilege principles.
- Do not select an authentication mechanism unless it is documented elsewhere.

## 10. Testing

- Add tests for new business functionality.
- Test business rules, API behavior, permissions, and tenant isolation.
- Cover relevant edge cases.
- Keep tests deterministic.
- Do not mandate a testing framework that has not been approved.

## 11. Documentation

Documentation is part of the project. Follow this documentation hierarchy:

```text
Root AGENTS.md
	↓
Project architecture documentation
	↓
Domain documentation
	↓
Implementation
```

Each Django domain should eventually contain domain-specific documentation, for example `orders/README.md`, `catalog/README.md`, and `shops/README.md`. Domain documentation should describe its purpose, business rules, database relationships, API behavior, permissions, edge cases, and testing requirements. Create these files only when requested or otherwise required by the task.

## 12. Architecture Decision Records

Document significant architectural decisions as ADRs, for example under `docs/decisions/`. An ADR should explain its context, problem, decision, alternatives considered, consequences, and status. Do not create ADR files until there is a decision to record.

## 13. AI Agent Workflow

AI coding agents must:

1. Read `AGENTS.md` before modifying code.
2. Read relevant project documentation.
3. Read relevant domain documentation before modifying a domain.
4. Understand existing code before changing it.
5. Avoid undocumented business assumptions.
6. Avoid changing architecture without explicit approval.
7. Keep changes scoped to the requested task.
8. Avoid unnecessary refactoring.
9. Add or update tests for relevant changes.
10. Update documentation when behavior or architecture changes.

## 14. Handling Ambiguity

If a requirement is ambiguous and the ambiguity can change business behavior, database structure, security, API behavior, or architecture, ask for clarification rather than inventing a rule. For minor implementation details that do not affect product behavior, use standard engineering judgment.

## 15. No Premature Engineering

Avoid unnecessary complexity. Do not introduce microservices, event-driven architecture, Kafka, Kubernetes, GraphQL, repository patterns, CQRS, event sourcing, or complex domain frameworks unless explicitly approved later. Prefer the simplest architecture that correctly satisfies documented requirements.

## 16. Change Discipline

When modifying existing code:

- Understand existing behavior first.
- Do not rewrite unrelated code.
- Do not change public APIs without approval.
- Do not change database behavior without documenting the impact.
- Do not remove existing functionality without approval.
- Keep commits and pull requests focused.

## 17. Source of Truth and Conflicts

When information conflicts, do not silently choose a behavior. Identify the conflict and request clarification when necessary. AI assumptions, generated code, outdated comments, and personal preference are not authoritative over explicit project requirements.

## 18. Current Project Status

The project is in the foundation and architecture stage. The following are not finalized; do not implement them based on assumptions:

- User authentication implementation
- Role model implementation
- Shop database schema
- Catalog database schema
- Inventory schema
- Customer schema
- Cart schema
- Order schema
- Campaign schema
- Notification architecture
- Analytics architecture
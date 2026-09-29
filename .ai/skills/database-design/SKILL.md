---
name: database-design
description: "Use when designing or changing PostgreSQL schemas, Django ORM models, or migrations in this repository."
---

# Database Design Skill

## 1. Purpose

This skill defines database-design standards for PostgreSQL, the Django ORM, Django migrations, and relational data modeling. PostgreSQL is the primary database, and the project follows a modular monolith architecture. Database design must support data integrity, clear relationships, tenant isolation, query efficiency, maintainability, and safe schema evolution. This skill does not define the Grocery Platform's actual schema.

## 2. General Database Principles

- Design around documented domain requirements.
- Prefer relational modeling and explicit relationships.
- Maintain data integrity at the database level where appropriate.
- Avoid unnecessary duplication and premature optimization.
- Keep schemas understandable and design for real access and query patterns.
- Do not introduce database complexity without a clear requirement.

Do not design the entire application schema in this skill.

## 3. Django ORM First

Use the Django ORM for normal database operations. Prefer `Model.objects.filter(...)` over raw SQL.

Use raw SQL only when the ORM cannot reasonably express the operation, PostgreSQL-specific functionality is genuinely required, or there is a demonstrated performance or technical reason. Review any raw SQL for SQL injection, portability, maintainability, transaction behavior, and query performance. Do not use raw SQL merely because it appears shorter.

## 4. Primary Keys

Do not assume a primary-key strategy unless it has been explicitly approved. The project decision regarding integer IDs, UUIDs, or another strategy must be documented before domain models are implemented. Do not introduce different primary-key strategies across domains without an explicit architectural reason.

## 5. Foreign Keys

Use Django relationships for relational data:

- Use `models.ForeignKey(...)` for a many-to-one relationship.
- Use `models.OneToOneField(...)` only for a genuinely one-to-one relationship.
- Use `models.ManyToManyField(...)` when the domain genuinely represents a many-to-many relationship.

Do not use generic foreign keys simply to avoid defining proper relationships.

## 6. Relationship Design

Every relationship must have a clear domain meaning. Before creating one, determine which entity owns it, whether it is optional, its cardinality, what happens when a related record is deleted, whether historical records must remain valid, and whether the relationship needs additional attributes. Do not create relationships merely because two entities happen to reference each other.

## 7. `on_delete` Behavior

Choose `on_delete` behavior based on documented domain semantics. Possible strategies include `models.CASCADE`, `models.PROTECT`, `models.SET_NULL`, and `models.SET_DEFAULT`. Do not automatically use `CASCADE`.

Consider data ownership, historical records, audit requirements, referential integrity, and whether deletion should be allowed at all. The domain specification should determine the correct behavior.

## 8. NULL and Blank

Understand the difference between `null=True` and `blank=True`. Use `null=True` for database-level NULL values only when the field genuinely needs absence or a third state at the database level. Use `blank=True` for Django validation requirements where appropriate.

Do not use `null=True` everywhere because a field is optional. For strings, avoid unnecessary database NULL values when an empty string has the required semantics. The choice must reflect domain meaning.

## 9. Required vs Optional Fields

Make an intentional required/optional decision for every field. Before making a field nullable, determine whether information is genuinely optional, can be known later, whether empty means something different from unknown, whether the API allows omission, and whether the workflow requires it at a particular stage. Do not make fields nullable simply to make development easier.

## 10. Unique Constraints

Use database-level uniqueness when a business invariant requires it. Prefer Django constraints such as:

```python
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=["..."],
            name="...",
        )
    ]
```

A serializer or view check alone is not sufficient protection against concurrent writes. If uniqueness matters, enforce it at the database level. Do not add `unique=True` without understanding the actual uniqueness requirement.

## 11. Check Constraints

Use `CheckConstraint` for stable invariants that must always hold, such as non-negative numeric values, values in a valid range, or known invariants between state fields. Do not duplicate complex business workflows inside database constraints.

## 12. Indexes

Base indexes on actual query patterns. Consider frequently filtered, joined, or ordered fields; foreign keys where appropriate; composite query patterns; and unique constraints. Do not index every field.

Every index has storage, write, maintenance, and migration costs. Give each index a clear reason.

## 13. Composite Indexes

Use composite indexes when queries commonly filter or order by multiple fields together. For example:

```python
models.Index(
    fields=["shop", "status"],
    name="...",
)
```

The index should correspond to a real query pattern. Consider field order carefully; do not create composite indexes merely because fields often appear together in models.

## 14. Query-Driven Database Design

Consider how data will actually be queried. Before adding an index or denormalized field, identify who queries it, which filters and sorts are used, query frequency, and potential dataset size. Consider database and API design together, but do not let API convenience alone justify poor relational design.

## 15. Denormalization

Prefer normalized relational data by default. Consider denormalization only for a demonstrated performance requirement, a justified read-heavy workload, historical snapshots, or values that must intentionally remain unchanged when source data changes.

When denormalizing, document why, the source of truth, how consistency is maintained, and add appropriate tests. Do not duplicate data merely to avoid a simple join.

## 16. Derived Data

Do not persist derived or calculated values without a clear reason. For example, `total = quantity × unit_price` is derived.

If a derived value must be stored for historical accuracy, performance, or auditability, document why it is stored, its source values, when it is calculated, whether it can change, and which value is authoritative.

## 17. Historical Data

Consider records referenced by historical business transactions before changing or deleting them. Transactions may need to preserve historical information even when current catalog or configuration data changes. Do not assume a foreign key should cascade-delete historical records. The relevant domain specification must define historical-data behavior.

## 18. Tenant / Shop Isolation

The platform is multi-tenant at the shop level. Database design must support safe shop-level isolation. Make ownership explicit for entities that belong to a shop. Do not rely solely on frontend filtering or API code without considering database constraints and relationships.

The final tenant-isolation implementation is defined separately in `.ai/skills/multi-tenancy/` and relevant domain specifications. Do not invent it here.

## 19. Audit and Timestamps

When domain requirements call for lifecycle tracking, consider fields such as:

```text
created_at
updated_at
```

Add other audit fields only when clearly required. Do not add audit columns to every table automatically; the domain specification determines the necessary historical and audit information.

## 20. Soft Delete

Do not introduce soft deletion automatically. Before using it, determine why records must remain physically stored, whether deleted records remain queryable, how uniqueness constraints account for deleted records, whether relationships continue to work, and whether the domain requires these semantics.

Soft delete must be a documented project-wide or domain-specific decision. Do not implement it independently in one model without architectural justification.

## 21. Status Fields

Use status fields only when a domain has a meaningful state machine or lifecycle. Status values must be explicit, documented, stable, and validated. Do not use arbitrary strings for domain states. Actual business states belong in domain specifications; do not define Grocery Platform statuses here.

## 22. Enumerations and Choices

Use Django choices or enums when a field has a controlled set of stable values. Domain specifications define the actual values. Do not use enums to replace free-form text when values are expected to change dynamically.

## 23. Money and Decimal Data

Represent monetary values using an appropriate exact numeric type. Do not use floating-point fields for currency. Define precision and scale according to domain and business requirements. Do not infer currency from formatting. If multiple currencies are eventually supported, model currency explicitly; do not assume multi-currency support unless product requirements require it.

## 24. Quantities

Choose numeric field types based on the actual domain; do not assume all quantities are integers. Grocery products may need different quantity semantics depending on how they are sold. The domain specification must determine whether quantities are integer, decimal, weight-based, unit-based, or another representation. Do not hard-code assumptions in this skill.

## 25. Naming Conventions

Use consistent database and model naming:

```text
PascalCase for models
snake_case for fields
snake_case for related names where appropriate
```

Use meaningful names and avoid abbreviations unless they are established domain terminology. Constraint and index names should be explicit, stable, concise, and unique as required by the database.

## 26. Migration Strategy

Use Django migrations for all schema changes. Typical commands are:

```text
python manage.py makemigrations
python manage.py migrate
```

Review generated migrations and commit them with related code. Never delete migration history to solve a normal migration problem. Avoid unnecessary migration churn, understand data implications before destructive changes, treat production schema changes as potentially high-risk, and make data migrations intentional and reviewed.

## 27. Data Migrations

Use data migrations when existing records need transformation as part of a schema change. They should be deterministic, safe to run through the migration system, careful with existing data, mindful of full-table operations and production dataset size, and realistically reversible where possible. Do not put unrelated business operations into migrations.

## 28. Destructive Schema Changes

Use particular care when dropping or renaming columns, changing field types or nullability, removing constraints, deleting tables, or changing relationship semantics.

Before a destructive migration, understand existing data, application dependencies, production usage, migration order, and rollback implications. Do not perform destructive database changes just to make a development environment pass.

## 29. Transactions and Data Integrity

Use transactions when multiple database writes must succeed or fail together. For example:

```python
from django.db import transaction

with transaction.atomic():
    ...
```

Database constraints should protect invariants regardless of which application path performs a write. Application validation and database constraints should complement each other.

## 30. Concurrency

Consider concurrent writes when designing important invariants. Application-level checks such as `if not Model.objects.filter(...).exists(): Model.objects.create(...)` may not prevent race conditions.

Where necessary, use appropriate unique constraints, transactions, row locking, or atomic updates. Do not introduce locking without understanding its performance and transaction implications.

## 31. Performance

Make database performance work evidence-driven. Identify the query, understand dataset size and query patterns, check for N+1 behavior, and determine whether indexes are appropriate. Avoid premature optimization. Do not add caching, denormalization, partitioning, or complex database structures without a demonstrated requirement.

## 32. PostgreSQL-Specific Features

Use PostgreSQL-specific features when they provide meaningful value. Document why the feature is needed and consider Django ORM support, migration support, and operational complexity. Do not use PostgreSQL-specific functionality merely because it is available; database complexity must remain justified.

## 33. Testing Database Behavior

Database-related tests should verify project-specific invariants such as unique and check constraints, relationship behavior, required and optional fields, tenant isolation, transaction behavior, important state invariants, and data-migration behavior where applicable. Do not unnecessarily test Django's own framework behavior.

## 34. Database Development Workflow

Before designing or modifying a model:

1. Read `AGENTS.md`.
2. Read `.ai/project-context/product.md`.
3. Read the relevant domain documentation.
4. Read `.ai/skills/django/SKILL.md`.
5. Read relevant API, multi-tenancy, or security documentation when applicable.
6. Identify actual domain requirements.
7. Identify relationships and ownership.
8. Identify important invariants.
9. Identify important query patterns.
10. Design the smallest appropriate schema.
11. Implement models.
12. Generate migrations.
13. Review migrations.
14. Add relevant tests.
15. Run Django checks.
16. Review query behavior where relevant.

If a required business rule or relationship is ambiguous, ask before designing the schema.

## 35. Git Workflow

Follow the repository's mandatory task-based Git workflow. Before making database or code changes:

```text
git status
git checkout main
git pull origin main
git checkout -b <task-id>/<short-description>
```

Do not work directly on `main`. If the working tree contains existing changes, inspect them first; do not discard them automatically or use destructive Git commands without explicit approval. If no task ID is provided for a new task, ask for it before creating the branch. Follow the complete Git workflow defined by the repository's development skills and `AGENTS.md`.

## 36. AI Agent Rules

AI coding agents MUST:

- Read existing domain requirements before designing schemas.
- Never invent business rules or relationships without domain justification.
- Never assume an unapproved primary-key strategy.
- Never add indexes without a reason.
- Never add nullable fields simply to avoid validation problems.
- Never add soft delete without approval.
- Never introduce denormalization without justification.
- Never delete migration history to solve migration problems.
- Never perform destructive schema changes without understanding their impact.
- Never modify unrelated models.
- Never create database structures solely for hypothetical future requirements.
- Ask for clarification when schema design affects business behavior, tenant isolation, historical data, or data integrity.

## 37. What This Skill Does Not Define

This skill does not define actual Grocery Platform models or tables, user/shop/product/inventory/customer/cart/order/campaign/notification/analytics schemas, the final authentication or authorization model, final tenant-isolation implementation, specific business states, or API contracts. Define those in the appropriate project or domain specifications.

## 38. Relationship With Other Skills

This database-design skill works together with:

```text
.ai/skills/django/
.ai/skills/drf/
.ai/skills/api-design/
.ai/skills/multi-tenancy/
.ai/skills/security/
.ai/skills/testing/
```

This skill focuses on database and schema design. The Django skill defines general Django engineering practices, the DRF skill defines API implementation practices, the multi-tenancy skill will define the final tenant-isolation approach, the security skill defines security-specific requirements, and the testing skill defines testing standards.

All skills must remain consistent with `AGENTS.md` and the project's canonical product and domain documentation.

## Final Requirement

Create only `.ai/skills/database-design/SKILL.md`. Do not modify application code, create models, migrations, database tables, or API endpoints; do not implement authentication or permissions or define Grocery Platform business rules.
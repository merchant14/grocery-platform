# Users & Merchant Accounts Domain Specification

## 1. Domain Purpose

The Users & Merchant Accounts domain defines the business concepts around platform user identity, merchant account identity, merchant-to-shop access, account lifecycle, and access boundaries needed for future authorization. It describes required concepts and behavior without selecting implementation details.

This domain does not own shop profiles, catalog or products, inventory, customer identity, carts, orders, campaigns, notifications, or analytics. Those belong to their respective domains.

## 2. Actors

### Super Admin

A platform-level actor who can perform approved administrative operations across the platform according to the eventual authorization design. This specification does not define the Super Admin permission set.

### Merchant

A business/shop operator who accesses merchant functionality for one or more shops only as allowed by approved membership and access rules. The number of shops and the account structure are not yet decided.

### Customer

Customers are not part of the merchant-account identity model. Customer identity is shop-specific and belongs to the Customers domain. Existing product requirements do not establish a customer authentication/account mechanism; none is defined here.

## 3. User vs Merchant vs Shop

These are distinct business concepts:

```text
User
    =
platform identity / person accessing the system

Merchant
    =
business/operator identity

Shop
    =
tenant/store being operated
```

Do not assume `1 User = 1 Merchant = 1 Shop`. The architecture must remain capable of supporting multiple people accessing the same merchant/shop in the future, as required by the product context. The exact cardinalities and relationships remain unresolved.

## 4. Merchant Account Model

The merchant account is the conceptual business/operator identity through which merchant activity is associated with shop access. The Shop domain owns shop identity, profile, and lifecycle context; this domain describes who may access a shop, subject to approved rules.

The exact merchant entity, ownership/administration model, and cardinality between users, merchants, and shops are not finalized. Do not assume that a merchant can operate multiple shops or that a shop can belong to only one merchant. These decisions require approval; see [Unresolved Decisions](#18-unresolved-decisions).

Merchant and shop remain distinct domain concepts unless an approved domain decision changes that understanding.

## 5. Merchant Membership / Access

Distinguish **user identity** (who is accessing the platform) from **access to a merchant or shop** (which merchant functionality and shop context that identity may use).

The current MVP concept allows merchant-side access to potentially be shared by a small number of people, approximately two or three. The architecture must not prevent future individual user identities and shop-level roles. This is an extensibility requirement, not approval of a shared-credential design or a specific membership model.

A future access relationship may conceptually involve a user, merchant, shop, role, or status. These are concepts only; this specification does not finalize fields, schema, or relationships. Membership lifecycle and access-granting rules require decisions.

## 6. Roles

The approved actor concepts relevant here are **Super Admin** and **Merchant / Shopkeeper**. This names actor categories; it does not decide whether or how they map to implementation roles.

No detailed merchant sub-roles, such as Manager, Cashier, Inventory Manager, or Staff, are approved. Additional role-based permissions may be considered later, but role names, definitions, and assignment rules are unresolved.

## 7. Account Lifecycle

The product context supports onboarding concepts that distinguish pending/review, approved, and rejected outcomes for a merchant/shop application. These are conceptual onboarding outcomes; exact status names and their relationship to user or merchant-account states are not finalized.

Do not treat additional account states, such as suspended or deactivated, as approved lifecycle states. Who activates or deactivates an account, how lifecycle status affects access, whether reactivation is possible, and how historical data is handled are unresolved.

## 8. Merchant Onboarding Relationship

The product requirements describe two conceptual paths:

### Path A: Super Admin creates/onboards a merchant and shop

```text
Super Admin
     ↓
Create Shop
     ↓
Create Merchant
     ↓
Merchant access
```

### Path B: Merchant applies for onboarding

```text
Merchant
     ↓
Application
     ↓
Super Admin review
     ↓
Approve / Reject
     ↓
Merchant access
```

These are business-level concepts, not finalized state machines or implementation flows. Do not define invitation tokens, email verification, OTP, forms, APIs, notifications, or activation mechanics here. Detailed onboarding behavior belongs in the Shop domain specification and remains subject to approval.

## 9. Relationship With the Shops Domain

Users & Merchant Accounts describes **who has access**. The Shops domain describes **what the shop is**, including its shop profile and tenant/business context.

Keep shop profile and other shop business data in the Shops domain. Access and identity concepts must not duplicate that data. This conceptual boundary does not prescribe database relationships.

## 10. Multi-Tenancy Implications

Follow `.ai/skills/multi-tenancy/SKILL.md` as the governing engineering standard.

- Merchant access must never permit unauthorized cross-shop access.
- Tenant context must come from trusted server-side context.
- A client must not choose arbitrary tenant scope as proof of access.
- IDs alone do not establish authorization.
- Every merchant operation involving shop-owned data must be evaluated against the actor's authorized shop access.

This specification does not define the technical tenant-context or authorization implementation.

## 11. Authentication and Authorization Boundary

Keep these concerns separate:

```text
Authentication: Who is this user?
Authorization: What is this user allowed to access?
Tenant access: Which shop(s) may this user operate?
```

This domain defines business concepts only; it does not select an authentication technology or final authorization mechanism. Do not assume JWT, sessions, OAuth, social login, password authentication, or OTP without separate approval.

## 12. Security Requirements

- Users must not access a merchant's shop without authorization.
- Merchant users may operate only within shops they are authorized to access.
- Super Admin access is platform-level only according to approved permissions.
- Account/shop lifecycle decisions must be respected when access rules are finalized; the exact behavior is unresolved.
- Authorization must be enforced server-side.
- Client-provided shop identifiers are never proof of access.
- Credentials and secrets must not be stored in source code.

See `.ai/skills/security/SKILL.md` and `.ai/skills/multi-tenancy/SKILL.md` for engineering standards. This section does not define a permission matrix or implementation.

## 13. Business Invariants

The following approved requirements must remain true:

- Merchant access is limited to the shop context(s) the merchant is authorized to operate.
- A merchant must not access another merchant's shop-owned data.
- Super Admin may operate across the platform only according to approved authorization.
- Customer identity is separate from merchant-account identity and is shop-specific.
- A customer identity or WhatsApp number must not expose customer history from another shop.
- The user/merchant/shop concepts must not be collapsed into an assumed one-to-one relationship.

Lifecycle behavior is not yet an approved invariant. If states such as inactive or suspended are later approved, whether they prevent active access must be explicitly decided and documented.

## 14. Cross-Domain Relationships

The following diagram represents conceptual authorization/access relationships, not database foreign keys:

```text
Users & Merchant Accounts
        |
        ├── controls access to → Shops
        |
        ├── authorizes access to → Catalog
        ├── authorizes access to → Inventory
        ├── authorizes access to → Orders
        ├── authorizes access to → Campaigns
        └── authorizes access to → Analytics
```

Customer identity and customer-owned information belong to the Customers domain and remain shop-specific. Catalog, Inventory, Orders, Campaigns, and Analytics retain ownership of their respective business behavior and data. Exact access policies remain subject to approved domain and authorization decisions.

## 15. Historical Data and Deactivation

The effect of user, merchant, or shop deactivation on existing shop access is unresolved. Historical orders and other records may need to remain available according to future domain rules, but this specification does not establish retention or access behavior.

The following require decisions: what happens to existing orders when a merchant user is deactivated, what happens to shop access, whether historical records remain and who may access them, whether a user can be reactivated, whether merchant/shop access can be transferred, and what happens if the only merchant-side user loses access.

## 16. Audit Requirements

The following actions may require auditability, subject to approved security and domain requirements:

- Merchant creation.
- Merchant application approval or rejection.
- User/account activation or deactivation.
- Shop access being granted or revoked.
- Role or permission changes, if introduced.
- Merchant ownership or access changes, if allowed.

These are audit requirements to evaluate, not a design for an audit log or schema. Exact events, retention, and access to audit information are unresolved.

## 17. Unresolved Decisions

No decision below is finalized by this specification.

| Decision | Reason | Impact |
|---|---|---|
| **Unresolved:** Authentication mechanism and provider. | Project and architecture documents explicitly leave authentication open. | Sign-in and trusted actor identification cannot be finalized. |
| **Unresolved:** Custom User model versus Django's default User model. | No user schema or model choice is approved. | Identity storage and future migration approach remain open. |
| **Unresolved:** Account recovery and credential management. | Authentication and credential lifecycle are not specified. | Recovery, credential issuance, and related user support behavior cannot be designed. |
| **Unresolved:** Exact merchant entity and its ownership/administration semantics. | Product documentation names merchants and shops but does not define their final structures. | Merchant identity and its relationship to shop operations remain conceptual. |
| **Unresolved:** Whether one merchant may operate multiple shops and whether one shop may be associated with multiple merchants. | Existing sources do not establish these cardinalities. | Access scope and ownership behavior cannot be finalized. |
| **Unresolved:** Membership/access model between users, merchants, and shops. | Shared merchant-side access is only an MVP concept; future individual users are anticipated, but no membership design is approved. | Access grants, revocation, and multi-person access behavior remain undefined. |
| **Unresolved:** Merchant roles and role-assignment rules. | Only Super Admin and Merchant are approved actor concepts; detailed roles and permission matrix are not finalized. | No role-specific access behavior can be assumed. |
| **Unresolved:** Account and onboarding lifecycle states, activation/deactivation authority, and access effects. | Pending/review, approved, and rejected are conceptual onboarding outcomes; account states and exact status names are not approved. | Eligibility for merchant functionality and state transitions require product/security decisions. |
| **Unresolved:** Exact onboarding and approval/rejection behavior. | Two onboarding paths are described conceptually, while fields, status names, account activation, and workflow details are deferred. | Onboarding cannot be implemented beyond documented concepts. |
| **Unresolved:** Merchant/shop ownership transfer and behavior if the only merchant-side user loses access. | Transfer and recovery behavior are not documented. | Continuity of shop operations and historical access cannot be determined. |
| **Unresolved:** Customer identity mechanism and any customer authentication behavior. | Customer identity is shop-specific and may use WhatsApp for repeat-order context, but the exact identity key and mechanism are deferred. | Customer identity must not be implemented as a global merchant-account identity or treated as authorization. |
| **Unresolved:** Account deactivation, reactivation, historical access, and related retention behavior. | Product/business documentation does not define these lifecycle effects. | Access to existing shop data and records after deactivation remains undefined. |
| **Unresolved:** Audit events, retention, and access requirements. | Candidate administrative/access changes may require auditability, but no complete audit requirement is approved. | Audit scope and handling cannot be finalized. |

## 18. Explicit Non-Goals

This document does not define Django models, database schema or columns, migrations, serializers, API endpoints or URL structure, authentication technology, JWT/session implementation, permission classes, frontend screens, password/OTP implementation, notification implementation, shop profile structure, catalog structure, order state machine, or inventory behavior.

These topics require their appropriate domain, architecture, API, security, or implementation documentation after the relevant business decisions are approved.

## 19. Implementation Gate

> The Users & Merchant Accounts domain must not be implemented until the unresolved decisions required for implementation are reviewed and approved.

After approval, implementation must follow `AGENTS.md`, relevant engineering skills, this domain specification, and `.ai/project-context/development-status.md`. An implementation agent must not silently resolve unresolved business decisions.

## 20. Git Workflow

Follow the mandatory repository workflow:

```text
git status
git checkout main
git pull origin main
git checkout -b <task-id>/<short-description>
```

- Never work directly on `main`.
- Inspect existing changes first; do not discard them automatically.
- Destructive Git commands require explicit approval.
- Ask for a task ID if one is not provided before creating a branch.
- Keep commits small and task-related; never commit secrets.
- Push the task branch and create a PR against `main`.
- Do not force-push or rewrite history without authorization.

Follow `AGENTS.md` for the complete workflow.

## Final Requirement

Create only `.ai/project-context/domains/users-and-merchant-accounts.md`. Do not modify application code, create models, migrations, APIs, authentication, authorization, or any other file. Do not resolve unresolved business decisions.
# Shops Domain Specification

## 1. Domain Purpose

The Shops domain owns the business concept of a shop/store on the Grocery Platform. Its conceptual scope includes shop identity and profile, shop lifecycle and onboarding-related state, the shop's role as tenant context, public shop visibility and QR/public URL relationship, the merchant/shop relationship, and shop-level operational configuration when approved.

This domain does not own platform user or merchant-account identity, catalog/products/variants, inventory, customer identity, carts, orders, campaigns, analytics, WhatsApp implementation, or payment implementation. Those belong to their respective domains.

## 2. Shop Concept

A **Shop** is a tenant/store on the platform through which merchant-owned catalog data exists, inventory is maintained, customers browse products, customers create carts and place orders, and shop-specific customer identity is maintained.

The Shop is the primary tenant boundary. The product describes grocery shops and shop-based ordering, but does not establish that every shop must be a physical retail location. Do not assume that requirement.

## 3. Shop vs Merchant

```text
Merchant
=
business/operator identity

Shop
=
store/tenant operated by the merchant
```

A User is the platform identity/person accessing the system; a Merchant is the business/operator identity; a Shop is the tenant/store being operated. See `.ai/project-context/domains/users-and-merchant-accounts.md` for identity and access concepts.

The relationship among User, Merchant, Shop, and merchant membership/access is conceptual only. Do not assume one user equals one merchant equals one shop, or finalize cardinality here.

## 4. Tenant Boundary

Follow `.ai/skills/multi-tenancy/SKILL.md` as the governing engineering rule.

- Shop is the primary tenant boundary.
- Merchant-owned operational data is scoped to a shop.
- One shop's tenant-owned data must never be exposed to another shop.
- A client-supplied shop identifier does not establish authorization.
- Server-side authorization must determine whether an actor may access a shop.
- Super Admin's platform-level access is separate from merchant tenant access and follows the approved authorization design.

The following domains may contain shop-scoped data:

- Catalog
- Inventory
- Customers
- Cart
- Orders
- Campaigns where applicable
- Notifications where applicable
- Analytics where applicable

This specification does not define the technical tenant-context implementation.

## 5. Shop Identity

Conceptually, a shop has an internal identity and a public-facing identity used by customers. Each shop has a shop-specific QR entry point that leads to that shop's public catalog/ordering experience.

The exact public shop name, internal identifier, URL/slug, QR destination format, and relationship among these identifiers are not finalized. Do not prescribe UUIDs, integer IDs, slugs, or other identity formats.

## 6. Shop Profile

### Approved

- A shop has a public-facing identity used in the customer-facing experience.
- A merchant can view and manage shop profile information.
- Shop profile information may support the customer-facing experience.

### Potential / Needs Decision

The product and business sources do not approve a specific profile field list. Names, descriptions, contact information, addresses, city/state/pincode, location details, logos, images, and branding are possible categories to evaluate, not confirmed fields. Pickup/delivery capabilities and operating status may also need shop-level configuration, but their exact behavior is not approved.

### Not in Scope Here

Do not define profile fields, schema, formats, validation, or field-level permissions in this specification.

## 7. Shop Status / Lifecycle

The product describes merchant/shop onboarding and review. The business-rules source recognizes conceptual pending/review, approved, and rejected outcomes, but exact status names and the complete shop lifecycle are not finalized.

An unapproved merchant/shop must not receive normal approved-shop functionality. Beyond this approved boundary, do not assume lifecycle states such as active, suspended, closed, or deactivated, or define their transitions.

Who may change shop status, how status affects public visibility and merchant operations, and what happens to existing customer and order data are **Not Finalized / Require Decision**.

## 8. Merchant Onboarding

The product requirements describe two business-level onboarding paths.

### Super Admin Initiated

```text
Super Admin
    ↓
Create/onboard merchant
    ↓
Create shop
    ↓
Merchant access
```

### Merchant Application

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

These flows describe product concepts only. Do not define API endpoints, forms, invitation tokens, OTP, email verification, authentication, notification mechanics, or exact database states. Approval and account activation details remain unresolved and belong in this domain's later decisions/specification.

## 9. QR Code

The product requires a permanent, shop-specific QR entry point. Conceptually:

- Each shop has a QR destination.
- Scanning it opens that shop's public web/catalog experience.
- The QR identifies the intended shop context.
- A shop's QR must not expose another shop's catalog or private data.
- The QR should remain stable if internal implementation details change, unless a future approved requirement changes this behavior.

QR encoding, library, image storage, generation, redirect service, and exact URL structure are **Not Finalized / Require Decision**.

## 10. Public Shop URL

The conceptual relationship is:

```text
Shop
   ↓
Permanent public URL
   ↓
Customer-facing shop/catalog
```

The URL must identify the intended shop context. Domain name, URL format, slug generation, routing, and SEO behavior are **Not Finalized / Require Decision**.

## 11. Public Shop Visibility

### Merchant/Admin Access

Merchant-side operation requires authorized access to the relevant shop. Super Admin access is platform-level according to the approved authorization design.

### Customer Public Access

Customers reach a shop's public catalog through its QR/public shop URL. The current product concept allows customers to browse and order without a traditional password account. Public catalog access does not grant merchant or administrative access and must not reveal private merchant information.

The visibility and customer-access behavior for pending, rejected, deactivated, or otherwise unavailable shops is **Not Finalized / Require Decision**.

## 12. Shop Availability

Product requirements say customers browse products available for the selected shop and can choose pickup or home delivery. They do not define shop opening hours, holidays, temporary closures, scheduled orders, or automatic order blocking based on operating hours.

These behaviors and the relationship between shop operational availability and browsing, ordering, pickup, or delivery are **Not Finalized / Require Decision**.

## 13. Pickup and Delivery

The MVP customer flow supports pickup, where a customer collects the order from the shop, and home delivery, where the customer provides a delivery address. The product does not include centralized delivery-partner management.

The product requirements do not confirm whether each shop has configurable pickup/delivery enablement or how a shop's capabilities affect customer choices. Per-shop capability settings are **Not Finalized / Require Decision**. Delivery zones, pricing, distance calculations, delivery partners, and tracking are not defined here.

## 14. Shop Configuration

| Configuration concept | Status | Current basis |
|---|---|---|
| Public-facing shop identity | Approved concept | A shop has an identity used in the customer-facing experience; exact fields are open. |
| Public catalog access through shop QR/URL | Approved concept | QR access leads to the intended shop's public catalog/ordering experience. |
| Shop visibility controls | Not finalized | Visibility for different shop lifecycle states is undefined. |
| Pickup enabled/disabled per shop | Not finalized | Pickup is an MVP customer choice; per-shop configuration is not specified. |
| Delivery enabled/disabled per shop | Not finalized | Home delivery is an MVP customer choice; per-shop configuration is not specified. |
| Customer ordering enabled/disabled | Not finalized | Rules for shop closure or order blocking are not specified. |
| Contact, location, and branding details | Not finalized | Exact profile fields have not been approved. |
| Operating status and hours | Not finalized | Hours, holidays, closures, and their effects are unspecified. |

These concepts are not a field list or schema.

## 15. Shop Ownership and Access

The Users & Merchant Accounts domain defines identity and access concepts; the Shops domain defines the shop itself and its shop business context.

The product supports Super Admin shop creation/onboarding and merchant applications reviewed by Super Admin. A merchant manages the shop(s) they are authorized to operate. The exact authority to create, update, activate, deactivate, or access shop settings is **Not Finalized / Require Decision**. Super Admin capabilities are subject to the final authorization design. Do not create a detailed permission matrix here.

## 16. Data Isolation

Shop isolation is mandatory:

```text
Shop A                 Shop B
  ├── Catalog A          ├── Catalog B
  ├── Inventory A        ├── Inventory B
  ├── Customers A        ├── Customers B
  ├── Carts A            ├── Carts B
  ├── Orders A           ├── Orders B
  └── Analytics A        └── Analytics B
```

Shop A must not access Shop B's tenant-owned data. IDs are not authorization; tenant scope must be trusted; related-object access must respect shop boundaries; and cross-tenant references must be prevented. Follow `.ai/skills/multi-tenancy/SKILL.md`. These are business/security requirements, not a database-constraint design.

## 17. Shop Deletion / Deactivation

Deletion and deactivation behavior is not finalized. Do not assume hard deletion, soft deletion, or that deactivation is equivalent to deletion.

Decisions are required for what happens to products, inventory, customers, carts, historical orders, analytics, and the permanent QR destination; whether a shop can be restored; and what public and merchant access remains. See [Unresolved Decisions](#24-unresolved-decisions).

## 18. Historical Data

Historical shop-related records may need to remain available when a shop becomes inactive. Retention period, archival, deletion policy, and access after deactivation are **Not Finalized / Require Decision**. Domain specifications must establish historical behavior before implementation.

## 19. Audit Requirements

The following shop-related actions may require auditability:

- Shop creation and onboarding.
- Shop approval or rejection.
- Shop activation or deactivation, if those states are approved.
- Shop profile changes.
- Merchant/shop access changes.
- Pickup/delivery configuration changes, if introduced.
- Public visibility changes, if introduced.

These are domain-level audit considerations, not an audit-log schema. Exact events, retention, and access rules are unresolved.

## 20. Cross-Domain Relationships

These are conceptual domain relationships, not necessarily database foreign keys:

### Users & Merchant Accounts

Defines who may access or manage a shop. The merchant identity and membership/access concepts are covered in `.ai/project-context/domains/users-and-merchant-accounts.md`.

### Catalog

Contains the platform master catalog and shop-specific catalog configuration as defined by the Catalog domain.

### Inventory

Contains shop-specific inventory and availability behavior.

### Customers

Contains shop-specific customer identity and customer information.

### Cart

Contains customer carts in the intended shop context.

### Orders

Contains orders created for the intended shop.

### Campaigns

May contain shop-related campaigns where applicable and approved.

### Notifications

May support shop-related notifications while preserving shop boundaries.

### Analytics

Aggregates shop-level operational metrics, subject to authorization for platform-wide aggregation.

## 21. Business Invariants

- Every merchant operation involving shop-owned data must be associated with an authorized shop context.
- Shop-owned data must remain isolated between shops.
- A shop-specific customer identity must not cross into another shop.
- A shop's QR/public destination resolves to the intended shop.
- Customer browsing through a shop entry point uses that intended shop context.
- Public shop access does not grant merchant administrative access.
- Shop identity remains distinct from merchant identity.

These invariants are supported by the product context and business-rules source. They do not determine schema or enforcement mechanisms.

## 22. Security Requirements

- Prevent cross-shop access server-side.
- Do not treat client-provided `shop_id` as authorization.
- Public catalog access must not expose merchant/admin functionality.
- Merchant operations require authorized access to the relevant shop.
- Super Admin operations require appropriate platform authorization.
- Shop-specific customer information remains isolated.
- QR/public URLs must not bypass tenant authorization or reveal another shop's private data.

Follow `.ai/skills/security/SKILL.md` and `.ai/skills/multi-tenancy/SKILL.md`. Do not select authentication or authorization technology here.

## 23. Unresolved Decisions

No decision below is finalized by this specification.

| Decision | Why unresolved | Impact |
|---|---|---|
| Exact shop identifier and public identity representation. | No identifier type or public identity fields are approved. | URLs, QR references, and shop identification cannot be specified. |
| Public URL format, domain, slug generation, routing, and SEO behavior. | Product requires a shop-specific public destination but does not define its structure. | Public access and URL stability details remain open. |
| QR encoding, generation, storage, and redirect behavior. | Only the permanent shop-specific QR concept is approved. | QR production and lifecycle behavior cannot be implemented. |
| Shop profile fields, including name/description/contact details. | A public identity and profile concept exist, but exact fields are not approved. | Data collection and customer display cannot be finalized. |
| Address/location and branding requirements. | These are possible profile categories, not confirmed requirements. | Location and brand data behavior remain open. |
| Shop lifecycle state names, transitions, and status authority. | Onboarding has conceptual pending/review, approved, and rejected outcomes; a complete shop lifecycle is not finalized. | Status changes and access/visibility behavior cannot be determined. |
| Who may create shops and the detailed approval/rejection behavior. | Two conceptual onboarding paths exist, but exact responsibilities and workflow are deferred. | Onboarding cannot be implemented beyond the approved concepts. |
| Merchant/shop cardinality and multiple-shop support. | Users & Merchant Accounts documents these relationships as unresolved. | Ownership, membership, and tenant-access scope remain open. |
| Shop visibility rules by lifecycle state. | Public access is required for the shop catalog, but pending/rejected/deactivated behavior is unspecified. | Customer access and public visibility cannot be finalized for those states. |
| Per-shop pickup and delivery configuration. | Customers may choose pickup or delivery; per-shop enablement is not stated. | Shop-specific fulfillment choices remain undefined. |
| Operating hours, holidays, temporary closures, and their effect on orders. | Product requirements do not define these behaviors. | Availability, browsing, and order blocking cannot be specified. |
| Shop deletion, deactivation, and the fate of related domain data. | Deletion and deactivation rules are explicitly unresolved. | Products, inventory, customers, carts, orders, and analytics behavior is unknown. |
| Historical-data retention, archival, and post-deactivation access. | No retention period or access policy is approved. | Historical records and customer/merchant access cannot be finalized. |
| QR behavior after shop deactivation or restoration. | Shop lifecycle and QR behavior in those states are unspecified. | Whether a permanent QR remains accessible or redirects cannot be decided. |
| Shop restoration and ownership transfer. | Neither restoration nor transfer behavior is documented. | Recovery and business continuity behavior remain open. |
| Audit events, retention, and audit access. | Potential audit actions are identified, but no complete requirement is approved. | Audit scope and handling cannot be designed. |

## 24. Explicit Non-Goals

This specification does not define Django models, database schema, migrations, serializers, API endpoints, URL routing implementation, authentication, authorization implementation, merchant user model, catalog/product schema, inventory behavior, customer identity implementation, cart implementation, order state machine, payment gateway, WhatsApp provider, delivery-partner architecture, analytics implementation, frontend implementation, or QR library.

## 25. Implementation Gate

> The Shops domain must not be implemented until the unresolved decisions required for implementation are reviewed and approved.

After approval, implementation must follow `AGENTS.md`, `.ai/project-context/product.md`, `.ai/project-context/architecture.md`, `.ai/project-context/business-rules.md`, `.ai/project-context/development-status.md`, this domain specification, and relevant engineering skills. An implementation agent must not silently resolve unresolved business decisions.

## 26. Git Workflow

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
- Ask for a task ID if none is provided before creating a branch.
- Keep commits small and task-related; never commit secrets.
- Push the task branch and create a PR against `main`.
- Do not force-push or rewrite history without authorization.

Follow `AGENTS.md` for the complete workflow.

## Final Requirement

Create only `.ai/project-context/domains/shops.md`. Do not modify any other file. Do not create models, migrations, APIs, authentication, authorization, or frontend behavior. Do not resolve unresolved business decisions.
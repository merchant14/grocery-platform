# Inventory Domain Specification

## 1. Domain Purpose

The Inventory domain owns the shop-specific stock state of products or variants offered by a shop. Its conceptual scope includes stock quantities and availability, inventory status concepts, stock adjustments and movement concepts, low-stock concepts, and the relationship of stock to Catalog and Orders.

Inventory does not own product definitions, product names/categories/variant definitions, shop identity, customer identity, carts, orders, payments, campaigns, analytics, or authentication. Those belong to their respective domains.

## 2. Catalog vs Inventory

Keep the domain responsibilities distinct:

```text
Catalog
=
What the shop sells

Inventory
=
How much of it is available
```

For explanation only, a Catalog may define a rice product, a 5 kg variant, and a shop-specific price; Inventory concerns the shop's stock state for the sellable item. This example does not approve a specific product, variant structure, unit, or price.

Catalog owns product and variant definitions. Inventory owns stock state. The exact inventory granularity (product-level, variant-level, or another approved scope) is unresolved.

## 3. Inventory Tenant Boundary

Follow `.ai/skills/multi-tenancy/SKILL.md` as the governing engineering rule.

- Inventory is shop-scoped.
- Every inventory state belongs to a shop context.
- Inventory must remain isolated between shops; Shop A must never read or modify Shop B inventory.
- Product or variant identifiers alone do not establish authorization.
- Merchant inventory operations require authorized access to the relevant shop.
- Super Admin platform-level operations follow the approved authorization design.

This specification does not define the technical tenant implementation.

## 4. Inventory Identity

Conceptually, inventory represents the stock state of a shop's sellable product or variant in the context of:

```text
Shop
  + Catalog Product
  + Catalog Variant, where applicable
  + Inventory state
```

Whether stock is tracked at product level, variant level, both, or another level is **Not Finalized / Requires Decision**. This specification does not choose identifiers, keys, or constraints.

## 5. Quantity

Inventory quantity concepts may include current quantity, available quantity, quantity added, quantity removed, and quantity adjusted. The quantity and any unit must respect the sellable unit defined by the Catalog domain.

Do not assume integer or decimal storage semantics, pieces, kilograms, liters, packs, or any other unit. Quantity type, fractional quantities, weighted products, and variable-weight products are unresolved; see [Unresolved Decisions](#24-unresolved-decisions).

## 6. Stock Availability

The terms **in stock**, **out of stock**, **low stock**, and **unavailable** describe useful concepts, but no final Inventory status model or definitions are approved.

It is unresolved whether availability is derived from quantity, explicitly controlled by a merchant, or determined by both. Do not introduce status names or assume that a quantity alone determines whether a product may be offered.

## 7. Low Stock

Low stock is a product requirement concept; merchant analytics may include low-stock information. A threshold could conceptually be associated with a quantity, but no formula such as `current quantity <= threshold` is finalized.

It is unresolved whether a threshold is per product, per variant, or per shop; whether it is optional; who configures it; and whether low stock affects customer visibility or only merchant analytics/alerts. Do not choose these behaviors.

## 8. Inventory Updates

Inventory may need to change through conceptual sources such as:

- Merchant stock adjustment, for example to reflect a physical count.
- Order-related activity, depending on the approved order and stock rules.
- Corrections or other explicitly approved adjustments.

Positive adjustments add quantity; negative adjustments remove quantity; corrections address an inaccurate recorded quantity. The exact adjustment authority, reasons, validation, and audit requirements are unresolved. Do not select when an order reserves or deducts stock.

## 9. Inventory and Orders

The conceptual relationship is:

```text
Customer submits an order
        ↓
Order contains product/variant and quantity
        ↓
Inventory is evaluated
        ↓
Inventory may be reserved or deducted
        ↓
Order progresses
```

This is not a finalized transaction flow. The Order domain owns order lifecycle and the Inventory domain owns stock behavior. The complete order state machine is not finalized; stock implications must be decided in coordination with the Order domain before implementation.

## 10. Stock Reservation

Whether the platform needs stock reservation, deduction, available quantity, reserved quantity, or committed quantity is **Not Finalized / Requires Decision**. These are concepts to evaluate, not approved inventory states or required fields.

Do not automatically implement reservations. If a future approved design distinguishes physical, reserved, and available stock, document its business meaning before implementation.

## 11. Overselling

The required behavior when a customer requests more quantity than a shop has available is **Not Finalized / Requires Decision**. Alternatives that require business approval may include rejecting the requested quantity, allowing the merchant to decide during order review, allowing temporary overselling, allowing partial fulfillment, or another documented behavior.

Do not select an alternative. Final overselling behavior must be explicitly approved.

## 12. Order Rejection / Cancellation

Inventory behavior may depend on order rejection, customer cancellation, merchant cancellation, order failure, and completion. The Order domain must define the order state machine first. This specification does not decide whether or when stock is reserved, deducted, released, or restored for these outcomes.

The Inventory/Order dependency and each outcome require explicit decisions before implementation.

## 13. Manual Stock Adjustments

Merchant stock adjustment is a conceptual operation for changing shop stock, including positive adjustments, negative adjustments, and correcting an inaccurate count. Product requirements say merchants manage stock/inventory for their own shop.

The exact users permitted to adjust stock, any role distinctions, reasons required, limits, approval, and auditability are not finalized. Do not define API behavior, schema, or detailed permission roles here.

## 14. Inventory History

Potential inventory events include stock added or removed, manual adjustments, order-related deductions, and order-related restoration. It is unresolved whether the business requires a persistent inventory history/ledger, which events it includes, or how long such history remains available.

Do not assume an inventory ledger is required or define its implementation.

## 15. Concurrency

The business requirement is that simultaneous order operations must not produce inventory outcomes that violate the approved reservation, deduction, or overselling rules.

For example, if available stock is five and two customers request four and three, the outcome must follow the explicitly approved overselling/reservation behavior. This document does not select locking, transactions, SQL, or another implementation technique.

## 16. Product Availability Interaction

Distinguish:

- **Catalog visibility:** whether customers can see a product.
- **Catalog availability:** whether the shop offers the product.
- **Inventory availability:** whether sufficient stock exists under approved Inventory rules.

Do not automatically make one control the others. Whether an out-of-stock product is hidden, shown as out of stock, addable to a cart, blocked at checkout, or handled according to merchant configuration is **Not Finalized / Requires Decision**.

## 17. Units of Measure

Catalog variants may eventually represent units such as pieces, kilograms, grams, liters, milliliters, or packs. These are illustrative possibilities, not a finalized unit list. Inventory must respect the sellable unit represented by the approved Catalog variant.

Do not create a separate unit-of-measure system without an approved requirement. Fractional, decimal, weighted, and variable-weight quantity semantics remain unresolved.

## 18. Low Stock and Merchant Visibility

Merchant-facing operations or analytics may eventually need to show current stock, low-stock products, out-of-stock products, inventory changes, and stock-related order impact. The business rules and exact presentation belong in relevant domain specifications; this document does not define an analytics dashboard.

## 19. Customer Visibility

The product does not define the amount of stock detail customers can see. It is unresolved whether customers see an exact quantity, availability only, an "Out of Stock" indication, a hidden listing, or another approved behavior. Whether stock changes are reflected immediately is also unresolved.

Do not expose detailed customer-facing inventory information by assumption.

## 20. Inventory Deletion / Product Removal

When a Catalog product or variant becomes inactive or is removed, inventory behavior is not finalized. Decisions are required for inventory records/history, existing carts, existing orders, restoration, and historical order integrity.

Do not assume hard deletion or soft deletion. Historical order behavior must follow approved Order rules.

## 21. Business Invariants

The following invariants are supported by the current requirements:

- Inventory is shop-scoped and isolated between shops.
- Inventory represents stock in the context of a shop and its offered Catalog product/variant, with exact granularity unresolved.
- One shop cannot modify another shop's inventory.
- Inventory changes must follow approved business rules.
- Customer ordering cannot bypass approved inventory rules.
- Catalog information changes alone do not constitute inventory quantity changes.

Historical order meaning and concurrency outcomes depend on unresolved Order and Inventory decisions. Do not state a specific snapshot, reservation, deduction, or overselling rule as finalized.

## 22. Security Requirements

- Merchant inventory operations require authorized shop access.
- Cross-shop inventory access must be prevented.
- Client-provided product, variant, or shop identifiers cannot bypass tenant authorization.
- Inventory adjustments must be server-authorized.
- Super Admin inventory access follows platform-level authorization.
- Credentials and secrets must never be stored in source code.

Follow `.ai/skills/security/SKILL.md` and `.ai/skills/multi-tenancy/SKILL.md`. Do not define authentication technology or authorization implementation here.

## 23. Cross-Domain Relationships

These are conceptual domain relationships, not necessarily database foreign keys:

### Shops

Provides the shop/tenant context for inventory.

### Users & Merchant Accounts

Determines who may manage inventory for an authorized shop.

### Catalog

Defines products, variants, and shop listings. Inventory represents their stock state; exact inventory granularity and availability interaction remain unresolved.

### Cart

May consume product availability information. Cart behavior and final stock validation points are not defined here.

### Orders

Order activity may cause stock evaluation or changes according to approved Order and Inventory rules. Timing and restoration behavior remain unresolved.

### Notifications

May eventually consume low-stock or stock-related events where approved.

### Analytics

Consumes inventory metrics, including potential low-stock information, subject to approved definitions and tenant scope.

## 24. Unresolved Decisions

No decision below is finalized by this specification.

| Decision | Why unresolved | Impact |
|---|---|---|
| Product-level versus variant-level inventory. | Catalog defines variants conceptually but not inventory granularity. | Stock identity and availability evaluation cannot be finalized. |
| Quantity type and representation. | No integer, decimal, weight, or other quantity semantics are approved. | Quantity entry, validation, and calculation behavior remain open. |
| Units of measure and fractional/weighted quantities. | Catalog unit semantics are not finalized. | Stock quantities cannot be interpreted consistently. |
| Low-stock threshold and formula. | Low-stock visibility is mentioned, but no threshold or calculation is approved. | Low-stock detection and reporting remain undefined. |
| Low-stock threshold ownership/configuration. | It is unknown whether thresholds vary by product, variant, shop, or actor. | Configuration and responsibility cannot be assigned. |
| Inventory status model. | In-stock, out-of-stock, low-stock, and unavailable are concepts without final definitions/states. | Status transitions and availability meaning remain open. |
| Stock reservation and reserved/committed quantity concepts. | No reservation requirement or state model is approved. | Concurrent customer requests and available quantity cannot be specified. |
| Stock deduction timing. | Order lifecycle and inventory behavior are not finalized. | Order submission and fulfillment cannot determine when stock changes. |
| Stock restoration timing. | Rejection, cancellation, failure, and completion behavior depend on unresolved order rules. | Reversals and available quantity remain undefined. |
| Overselling behavior. | No approved behavior exists for requests above available stock. | Checkout/order acceptance outcomes remain open. |
| Order rejection and cancellation effects on stock. | The complete order state machine and cancellation rules are unresolved. | Reservation, deduction, and restoration behavior cannot be chosen. |
| Manual adjustment permissions and audit expectations. | Merchant stock management is required, but exact authority and audit rules are not defined. | Adjustment access and records remain unspecified. |
| Inventory history/ledger requirement. | Historical movement records are not approved as a business requirement. | Audit, reconciliation, and historical stock reporting remain open. |
| Concurrency outcomes. | Outcomes depend on reservation and overselling decisions. | Simultaneous requests cannot be assigned final business behavior. |
| Customer-facing stock visibility. | Product requirements do not specify exact quantity versus availability-only information. | Customer display remains open. |
| Out-of-stock catalog behavior. | Hide/show/cart/checkout behavior is not defined. | Customer browsing and ordering outcomes remain open. |
| Product/variant deactivation and inventory handling. | Catalog lifecycle and Inventory relationship are unresolved. | Existing stock, carts, orders, and restoration behavior are unknown. |
| Inventory deletion and retention. | No hard/soft delete or historical inventory policy is approved. | Historical records and references cannot be resolved. |
| Initial stock when a product is created. | No stock initialization rule is documented. | New listing availability cannot be inferred. |
| Stock when a new variant is added. | No initialization or default quantity rule is documented. | Variant availability cannot be inferred. |

## 25. Explicit Non-Goals

This specification does not define Django models, database schema, migrations, serializers, API endpoints, authentication, authorization implementation, product definitions or variants, catalog categories, cart implementation, order state machine, payment processing, WhatsApp implementation, delivery management, analytics implementation, frontend implementation, or database locking/transaction implementation.

## 26. Implementation Gate

> The Inventory domain must not be implemented until the unresolved inventory decisions and its dependencies on the Order and Catalog domains are reviewed and approved.

After approval, implementation must follow `AGENTS.md`, `.ai/project-context/product.md`, `.ai/project-context/architecture.md`, `.ai/project-context/business-rules.md`, `.ai/project-context/development-status.md`, `.ai/project-context/domains/catalog.md`, `.ai/project-context/domains/shops.md`, `.ai/project-context/domains/users-and-merchant-accounts.md`, this domain specification, and relevant engineering skills. The implementation agent must not silently resolve business decisions.

## 27. Git Workflow

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

Create only `.ai/project-context/domains/inventory.md`. Do not modify any other file. Do not create models, migrations, APIs, authentication, authorization, or inventory functionality. Do not resolve unresolved business decisions.
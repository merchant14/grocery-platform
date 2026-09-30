# Grocery Platform Business Rules

## 1. Purpose

This document captures approved business rules and invariants that application code, APIs, database constraints, tests, and future domain documentation must respect. Business rules describe what the system must do, not how it is implemented. Do not infer rules solely from current implementation.

```text
Product Requirement
        ↓
Business Rule
        ↓
Technical Implementation
```

## 2. Actors

### Super Admin

The Super Admin is a platform-level actor responsible for approved administrative operations, including merchant/shop onboarding and review, platform master-catalog management, merchant-created product review, campaigns/advertisements, and platform analytics. This document does not define the final permissions.

### Merchant / Shopkeeper

A Merchant / Shopkeeper operates a shop and is responsible for shop management, the merchant catalog, products and variants, pricing, inventory and availability, incoming orders and order processing, merchant-side analytics, and merchant-provided payment instructions. This document does not define the final user or account architecture.

### Customer

A Customer interacts with a specific shop through its QR/public shop URL, shop catalog, product selection, cart, checkout, pickup or delivery selection, order information, and a WhatsApp number. The current MVP concept does not require a traditional customer username/password account.

## 3. Shop / Tenant Rules

- A shop is the primary tenant boundary.
- Merchant-owned data belongs to a shop and must remain isolated from other shops.
- Merchants must not access another shop's tenant-owned data.
- Super Admin may operate across shops according to the final authorization design.
- Customer identity is shop-specific; the same WhatsApp number does not automatically create a globally shared customer identity.
- A customer ordering from Shop A must not gain access to Shop B's customer history.

Follow `.ai/skills/multi-tenancy/SKILL.md` for the engineering requirements. This document does not define technical tenant-context implementation.

## 4. Merchant / Shop Onboarding Rules

A shop may be created/onboarded by a Super Admin or submitted by a merchant for review and approval. The conceptual lifecycle must distinguish pending/review, approved, and rejected outcomes, but the exact status names are not finalized.

An unapproved merchant/shop must not receive normal approved-shop functionality. The exact onboarding process, approval behavior, account activation, and authorization details require domain decisions; do not define them here.

## 5. Shop Profile Rules

A shop has a public-facing identity used in the customer-facing experience. Its profile may contain information necessary for that experience. The exact profile fields are **Not Finalized / Requires Decision**; do not invent them.

## 6. QR / Public Shop Access Rules

- Each shop can have a permanent, shop-specific QR entry point.
- Scanning it should lead to that shop's public catalog and ordering experience without requiring manual shop search.
- QR access identifies the intended shop context.
- Public access must not expose private merchant information.
- Changing a QR target must not accidentally expose another shop's private data.

The QR format and URL structure are **Not Finalized / Requires Decision**.

## 7. Master Catalog Rules

The platform maintains master-catalog information under Super Admin management. Merchant catalog configuration is separate from the platform master catalog. A merchant may create products not present in the master catalog; these initially belong to the merchant's catalog and may enter Super Admin review.

Not every merchant product must originate from the master catalog. The product-review, approval, rejection, and catalog-merging workflow is **Not Finalized / Requires Decision**.

## 8. Merchant Catalog Rules

Each merchant has a shop-specific catalog. Catalog behavior may include products, categories, variants, pricing, availability, and inventory-related information, subject to domain specifications.

Merchant-specific configuration must not modify another merchant's catalog or accidentally modify platform-global master-catalog data.

## 9. Product Rules

Approved conceptual rules:

- Products belong to a catalog/domain context and may have variants.
- Merchants may have shop-specific product configuration.
- Merchant-created products may exist in a merchant catalog independently of master-catalog approval.
- Product visibility and availability follow the relevant merchant/shop configuration.
- One merchant's product configuration must not change another merchant's configuration.

SKU format, exact product fields, variant structure, tax and unit models, and the product-approval algorithm are **Not Finalized / Require Decision** unless approved in future domain documentation.

## 10. Pricing Rules

- Merchant/shop-specific pricing is independent.
- A master-catalog product does not automatically dictate a merchant's selling price.
- Changing one merchant's price must not change another merchant's price.
- Customer checkout uses the applicable shop-specific price.

Tax and discount calculation, currency architecture, price history, and promotional pricing algorithms are **Not Finalized / Require Decision**.

## 11. Inventory and Availability Rules

- Product availability and inventory are merchant/shop-specific.
- One merchant's stock must not affect another merchant's stock.
- Customer-facing availability reflects the shop's configured availability.
- Inventory-related updates preserve tenant isolation.

Reservation logic, stock-deduction timing, low-stock thresholds, overselling behavior, warehouse concepts, and reconciliation algorithms are **Not Finalized / Require Decision**.

## 12. Customer Identity Rules

- Customer identity is shop-specific, not globally shared across merchants by assumption.
- Within a Shop, the customer's WhatsApp number is the primary identifier for recognizing a returning Customer.
- A permanent Shop-specific Customer record is created when the customer first provides their WhatsApp number for that Shop, even before an Order is successfully created.
- Customer information may be reused or pre-filled for future orders at the same shop when the customer provides the same WhatsApp number.
- A WhatsApp number must not expose another shop's customer history.
- Traditional customer username/password accounts are not required by the current MVP concept.

Phone-number normalization and formatting, detailed recognition behavior, privacy handling, and authentication mechanism are **Not Finalized / Require Decision**. The Shop-scoped WhatsApp identity rule and pre-order Customer creation are approved.

## 13. Cart Rules

- A cart is associated with a specific shop context.
- Products added to a cart belong to its intended shop/catalog context.
- A cart must not mix unrelated shops unless a future approved requirement introduces multi-shop carts.
- An initially anonymous cart may become associated with the Shop-specific Customer when the customer first provides their WhatsApp number.
- Customer creation may therefore occur before checkout and before Order creation.
- Prices and availability are validated appropriately before order creation.

Cart persistence, guest-session mechanism, expiration, quantity limits, and price-snapshot behavior are **Not Finalized / Require Decision**.

## 14. Checkout Rules

The current checkout concept requires customer name and WhatsApp number, selected products/variants, quantities, and a pickup or home-delivery choice. Home delivery requires an address. Pickup does not require a delivery address unless another approved requirement says otherwise.

Do not invent additional mandatory checkout fields. Address validation and delivery-zone rules remain subject to domain decisions.

## 15. Delivery / Pickup Rules

The MVP supports:

- **Pickup:** the customer collects the order from the shop.
- **Home delivery:** the customer provides a delivery address.

The MVP does not include centralized delivery-partner management. Delivery pricing, delivery zones, distance calculations, delivery-partner assignment, and ETA algorithms are **Not Finalized / Require Decision**.

## 16. Order Rules

The product requirements describe this conceptual order lifecycle:

```text
PENDING
   ↓
ACCEPTED
   ↓
PREPARING
   ↓
READY
   ↓
COMPLETED
```

They also describe the alternative:

```text
PENDING → REJECTED
```

This is not a finalized, complete state machine. Do not infer additional transitions or cancellation, refund, timeout, return, or partial-fulfillment states. The merchant operates order acceptance, rejection, and status updates through the merchant ERP/web interface.

## 17. Merchant Order Operations

- Incoming orders are visible to the appropriate merchant/shop.
- The merchant reviews an order and may accept or reject it according to the approved workflow.
- The merchant may progress an accepted order through the approved fulfillment lifecycle.
- A merchant must not operate on another shop's orders.
- WhatsApp is not the primary order-operation interface; merchant operations occur through the ERP/web interface.

Do not define exact UI behavior or API endpoints here.

## 18. Customer Order Rules

Customers should be able to review their cart, submit an order, provide required checkout information, select pickup or delivery, and receive appropriate order communication. The exact customer order-history experience is **Not Finalized / Requires Decision**.

## 19. Payment Rules

For the MVP, payment is merchant-handled. A merchant may share UPI, UPI QR, or other payment instructions. The platform does not process centralized online payments in the MVP, and no payment gateway is approved.

Payment gateway, automatic payment verification, refunds, settlements, and commission/monetization are **Not Finalized / Require Decision**.

## 20. WhatsApp Rules

WhatsApp is primarily a communication and notification channel. It may be used for order notifications, acknowledgements, and merchant/customer communication when explicitly approved.

It is not the primary merchant interface for accepting or rejecting orders, changing order status, or managing inventory. The merchant ERP/web interface remains the operational interface. Do not select a WhatsApp provider or integration architecture here.

## 21. Merchant Accounts

The MVP concept allows merchant-side access to potentially be shared by a small number of people. The architecture should not prevent future individual merchant accounts and role-based access.

The number of users per shop, membership model, roles, invitation flow, and authentication mechanism are **Not Finalized / Require Decision**.

## 22. Campaign / Advertising Rules

Super Admin can manage platform campaigns/advertisements according to the approved product concept. Campaigns may be platform-level or shop-related, subject to the finalized domain design.

Advertising pricing, targeting algorithms, campaign bidding, monetization, and ad ranking are **Not Finalized / Require Decision** unless explicitly approved.

## 23. Analytics Rules

Merchant analytics must be shop-scoped. Conceptual merchant metrics may include orders, sales/revenue-related metrics, top products, low stock, rejected/completed orders, average order value, and customers.

Platform analytics may include shops, orders, sales, shop performance, product performance, customers, and campaigns. Do not define exact metric formulas unless they have been finalized.

## 24. Cross-Domain Business Invariants

The following invariants must hold across domains:

- An order belongs to one shop context.
- Merchant-specific pricing belongs to the appropriate shop.
- Shop-specific customer identity remains within that shop.
- Inventory belongs to the appropriate shop/product context.
- Merchant operations cannot cross shop boundaries.
- Customer-facing catalog access is tied to the intended shop.
- Tenant-specific operations must not accidentally mutate platform-global master data.

These are business invariants, not a definition of database constraints or schema.

## 25. Historical Data

When a business operation changes current information, consider whether historical records must preserve the state that existed when an event occurred. Relevant examples may include order information, the pricing used for an order, the customer/order relationship, and merchant/shop state.

The exact snapshot strategy and historical-data requirements are **Not Finalized / Require Decision**.

## 26. Deactivation / Deletion

Deletion behavior is not fully defined. The following are **Not Finalized / Require Decision**:

- Shop deletion.
- Merchant deletion.
- Customer deletion.
- Product deletion.
- Order deletion.
- Historical-data retention.
- Customer/order access for a deactivated shop.

Do not invent soft-delete rules.

## 27. Business Rules vs Implementation

A business rule states required behavior:

```text
Business rule:
"Merchant A cannot access Shop B orders."
```

Implementation is a separate technical decision:

```text
Implementation:
"The application may enforce this through tenant-scoped querysets,
authorization checks, database constraints, or another approved design."
```

This document defines the business rule, not a premature implementation choice.

## 28. Unresolved Business Decisions

The following require product/business approval and must not be answered by assumption:

- Final merchant/shop onboarding statuses.
- Merchant account and membership model.
- Customer phone-number normalization and formatting.
- Exact catalog/master-catalog approval workflow.
- Product and variant structure.
- Inventory deduction behavior.
- Overselling behavior.
- Low-stock rules.
- Complete order state machine.
- Cancellation behavior.
- Refund behavior.
- Delivery pricing.
- Delivery zones.
- Customer order-history behavior.
- Payment verification.
- Campaign rules.
- Analytics formulas.
- Deletion and retention policies.
- Historical-data requirements.

## 29. AI Agent Business-Rule Workflow

Before implementing business behavior, an AI agent MUST:

1. Read `AGENTS.md`.
2. Read `.ai/project-context/product.md`.
3. Read `.ai/project-context/architecture.md`.
4. Read this business-rules file.
5. Read the relevant domain documentation.
6. Read relevant engineering skills.
7. Identify the applicable business rule.
8. Verify whether it is finalized.
9. Ask for clarification if it is not finalized.
10. Never invent business behavior to complete implementation.
11. Add or update tests for approved business rules.
12. Update documentation when an approved business-rule decision changes.

## 30. Documentation Change Rule

When a business decision changes:

1. Update the canonical business-rule documentation.
2. Update affected domain documentation.
3. Update architecture or ADR documentation if the decision has architectural impact.
4. Update tests and implementation.
5. Ensure all sources remain consistent.

Do not silently encode business decisions only in application code.

## 31. Git Workflow

Follow the mandatory repository workflow:

```text
git status
git checkout main
git pull origin main
git checkout -b <task-id>/<short-description>
```

Never work directly on `main`. Inspect existing working-tree changes first and do not discard them automatically. Destructive Git commands require explicit approval. Ask for a task ID before creating a new task branch when none is provided. Keep commits small and logical, never commit secrets, push task branches, and create PRs against `main`. Do not force-push or rewrite history without authorization. Follow `AGENTS.md` for the complete workflow.

## 32. What This File Does Not Define

This document does not define database schema, Django models, API endpoints, serializers, authentication, permission classes, infrastructure, implementation architecture, specific third-party providers, or unresolved business decisions. Those must be defined in the appropriate specifications and approved before implementation.

## Final Requirement

Create only `.ai/project-context/business-rules.md`. Do not modify application code, models, migrations, APIs, authentication, permissions, or infrastructure. Do not invent or silently finalize a business rule not supported by approved product requirements.
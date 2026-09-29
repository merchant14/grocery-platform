# Orders Domain Specification

## 1. Domain Purpose

The Orders domain owns the purchase transaction after checkout. Its business scope includes order identity and shop context, customer/order context, ordered items, historical purchase pricing, fulfillment choice, order lifecycle, merchant order handling, rejection/cancellation decisions, order history, payment context, and notification-triggering events.

Orders does not own shop identity, merchant authentication, product definitions, current catalog pricing, inventory master state, cart state, WhatsApp provider implementation, payment gateway implementation, analytics implementation, or delivery-partner management. Those belong to their respective domains.

## 2. Order Identity

An order conceptually belongs to:

```text
One Shop
+
One Customer context
+
One Purchase Transaction
```

An order belongs to exactly one shop and must not belong to multiple shops. The exact order ID type, order-number format, and public tracking identifier are not finalized. Do not assume integer IDs, UUIDs, or a specific reference format.

## 3. Shop / Tenant Boundary

Shop isolation is mandatory. Every order belongs to one shop context; merchants may access orders only for shops they are authorized to manage; customer order history is shop-specific; and a shop must not expose another shop's orders. Customer-facing order access must not bypass shop isolation. Client-provided identifiers do not establish authorization.

Follow `.ai/skills/multi-tenancy/SKILL.md`. This is the business/security boundary, not a technical tenant implementation.

## 4. Order Creation

The current conceptual flow is:

```text
Customer
   ↓
Cart
   ↓
Checkout
   ↓
Validate cart
   ↓
Create Order
   ↓
Order becomes PENDING
```

The exact order-creation transaction, validation implementation, duplicate-submission handling, and persistence behavior are not defined here. Order creation depends on Catalog, Inventory, Customers, and Cart domain rules.

## 5. Order Snapshot / Historical Meaning

An order represents what the customer actually ordered at the time it was created. Later changes to product name or information, variant information, catalog price, shop catalog, inventory, or customer profile must not silently rewrite the historical meaning of an already-created order.

The exact snapshot implementation is unresolved. Do not choose whether to copy fields, reference immutable records, store snapshots, or use another approach. The required historical meaning is a business boundary; its representation belongs in later design.

## 6. Order Items

An order item conceptually represents a product, a selected variant where applicable, the ordered quantity, the price relevant when the order was created, and an item-level total.

Do not define exact fields or database structure. Not every product is assumed to require a variant. Item meaning must remain consistent with the Catalog domain and preserve the approved historical purchase meaning.

## 7. Pricing

Distinguish:

- **Catalog:** current shop-specific selling price.
- **Cart:** price associated with current shopping state, subject to Cart rules.
- **Order:** historical purchase price for the created transaction.

Once an order exists, later catalog price changes must not alter its historical price. This does not define how the historical price is represented.

## 8. Order Total

Conceptually, an order total may be derived from item totals plus delivery or other approved charges, less approved discounts. These are possible components only, not a claim that each exists:

```text
Item totals
+
Delivery charges, if applicable
+
Other approved charges
-
Approved discounts
=
Order total
```

Do not assume taxes, fees, discounts, delivery charges, or a calculation formula unless approved. The MVP has no centralized online payment gateway; do not introduce gateway calculations here.

## 9. Customer Information

An order is associated with a shop-specific customer context. The Customers domain owns current customer identity; Orders owns the historical transaction. The order should retain information necessary to understand the transaction historically, but the exact copied, referenced, or snapshot representation is unresolved.

## 10. Customer Contact Information

The current checkout concept includes customer name and WhatsApp number. The WhatsApp number may be used for order communication. It is contact information, not authentication, and must not grant access to order history by itself.

Home delivery also requires a delivery address. Additional contact fields are not defined here.

## 11. Fulfillment

The product supports:

- **Pickup:** the customer collects the order from the shop.
- **Home delivery:** the shop delivers the order to the customer's address.

Fulfillment choice is part of the order context. The MVP does not include centralized delivery-partner management. Do not define delivery-partner assignment, pricing, tracking, or detailed delivery operations here.

## 12. Delivery Address

For home-delivery orders, an appropriate delivery address is required under the approved checkout concept. Pickup does not require a delivery address unless another approved requirement says otherwise.

The address may need to remain meaningful for the order, but its exact structure and snapshot behavior are unresolved. Free-form versus structured address, pincode, landmark, coordinates, and saved customer addresses are not decided here.

## 13. Order Lifecycle

The product requirements describe this conceptual lifecycle:

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

An order may alternatively follow:

```text
PENDING
   ↓
REJECTED
```

This is the current conceptual lifecycle, not a complete or finalized state machine. Do not infer states such as CANCELLED, FAILED, REFUNDED, EXPIRED, or DELIVERED unless approved in the source of truth.

## 14. PENDING

Conceptually, the customer has submitted the order and it is awaiting merchant action. The merchant has not yet accepted or rejected it. Timeout behavior and automatic state changes are not defined.

## 15. ACCEPTED

Conceptually, the merchant has accepted the order for fulfillment by the shop. Exact acceptance conditions and inventory deduction timing are not defined here and depend on approved Order and Inventory decisions.

## 16. PREPARING

Conceptually, the shop is preparing the accepted order. The exact entry conditions and whether the transition is manual or automatic are not finalized.

## 17. READY

Conceptually, the order is ready for customer pickup or applicable fulfillment completion. Additional delivery-specific state or behavior is not defined here.

## 18. COMPLETED

Conceptually, the order's fulfillment is complete. The exact meaning for pickup versus delivery and who records completion are unresolved.

## 19. REJECTED

The merchant may reject a pending order; a rejected order is not fulfilled. Whether a rejection reason is required, whether the customer is notified, inventory consequences, and whether reopening is possible are unresolved. Do not infer additional rejection transitions.

## 20. Merchant Order Operations

The product requires merchant order operations through the merchant ERP/web interface. Conceptually, the merchant can view incoming orders, accept or reject according to the approved workflow, update fulfillment status, and complete orders according to the approved lifecycle.

Operations are scoped to shops the merchant is authorized to manage. Merchants do not accept or reject orders through WhatsApp in the current product scope. Exact UI behavior and API endpoints are not defined here.

## 21. Customer Order Visibility

Customers need appropriate visibility into their orders, but the product does not define how they identify or access an order after checkout. Possible concepts include an order reference, browser/session context, WhatsApp link, or public status page; none is selected.

Do not assume a customer account/login or expose private order/customer information through a public access mechanism.

## 22. Order Cancellation

Cancellation is unresolved. Decisions are required on whether a customer or merchant may cancel, permitted states/timing, inventory effects, payment consequences, notifications, and cancellation during or after preparation or readiness. Do not implement or imply a cancellation model without explicit approval.

## 23. Refunds

The MVP has no centralized online payment gateway. Do not introduce an online refund workflow. If payment has already occurred outside the platform and an order is rejected or cancelled, the merchant's and platform's responsibilities are **Not Finalized / Require Decision**.

## 24. Payment Context

For the MVP, payment is handled by the merchant. The merchant may provide UPI, UPI QR, or physical payment instructions. Centralized gateway processing is not approved.

The order may eventually need payment-related context, but this does not define a payment system. Whether payment status is recorded, who records it, whether proof is stored, whether an unpaid order may be accepted, and how payment relates to the order lifecycle are unresolved.

## 25. Inventory Interaction

Orders interact with Inventory. A conceptual flow may include order creation, inventory validation, merchant acceptance or rejection, and an inventory update, but the sequence and timing are not finalized.

Inventory has unresolved decisions about reservation, deduction, restoration, and overselling. Orders must follow those decisions after approval. See `.ai/project-context/domains/inventory.md`; do not choose inventory behavior here.

## 26. Order and Cart Boundary

```text
Cart
=
temporary shopping state

Order
=
historical purchase transaction
```

After successful order creation, the order is independent of future cart changes. Cart-clearing behavior after order creation is not defined here; follow approved Cart rules.

## 27. Notifications

Orders may produce conceptual notification events for order creation, acceptance, rejection, preparation, readiness, completion, and cancellation if later approved. The product explicitly includes customer order-received and order-accepted communications, and a merchant new-order notification. The exact event set, recipients, and timing remain subject to domain decisions.

The Notifications domain defines delivery behavior. Do not implement notifications here.

## 28. WhatsApp Boundary

The conceptual flow is:

```text
Orders
   ↓
Notification event
   ↓
Notifications
   ↓
WhatsApp
```

WhatsApp is a notification/acknowledgement channel. Merchant order operations remain in the ERP/web interface. Do not define or imply WhatsApp commands for accepting, rejecting, preparing, marking ready, or completing orders unless a future product decision explicitly changes scope.

## 29. Order History

Orders are historical business records. Merchants see orders belonging to shops they are authorized to manage. Customers may need access to their own order history within the relevant shop-specific customer context. Super Admin may have platform-level operational or reporting visibility according to approved authorization.

The exact retention, history access mechanism, and visibility policies are unresolved. Do not assume a final permission matrix.

## 30. Order Data Visibility

Distinguish conceptually among:

- **Customer-visible information:** what a customer needs to understand their order.
- **Merchant-visible information:** what an authorized merchant needs to review and fulfill the order.
- **Super Admin-visible information:** what is permitted by platform-level authorization.

Minimize exposed customer data. Exact fields and permissions remain for approved API, privacy, and authorization decisions.

## 31. Historical Data

Orders represent historical business transactions. Consider preservation of product/variant meaning, order-time pricing, customer/order context, fulfillment choice, and relevant order status history. This specification requires that later Catalog or Cart changes do not silently rewrite an existing order's historical meaning or purchase price.

The exact snapshot representation, retention period, archival, deletion, and access rules remain unresolved. See the business-rules source and the Catalog, Customers, and Inventory specifications.

## 32. Concurrency and Idempotency

Conceptual scenarios include duplicate customer checkout submissions, repeated merchant acceptance, and concurrent attempts to update the same order. The system must not create unintended duplicate purchases or allow invalid state transitions once those business rules are approved.

Do not design idempotency keys, database locks, or transaction code here. Exact duplicate-submission and concurrent-transition behavior is unresolved.

## 33. Order State Transition Rules

The currently described transitions are:

| Current state | Conceptual next state | Actor / notes |
|---|---|---|
| `PENDING` | `ACCEPTED` | Merchant reviews and accepts through the ERP/web interface. |
| `PENDING` | `REJECTED` | Merchant rejects through the ERP/web interface. |
| `ACCEPTED` | `PREPARING` | Merchant may progress the accepted order through fulfillment; exact transition authority is not finalized. |
| `PREPARING` | `READY` | Conceptual fulfillment progression; exact transition authority is not finalized. |
| `READY` | `COMPLETED` | Conceptual completion; exact pickup/delivery meaning and who records it are unresolved. |

This table is conceptual and does not finalize a complete state machine or permission rules. Do not add transitions absent approval. Invalid transitions must eventually be prevented by implementation according to the approved state machine.

## 34. Business Invariants

The following requirements are supported by current product and business documentation:

- An order belongs to exactly one shop.
- An order must not expose another shop's data.
- An order represents the purchase made at creation time; later catalog price changes must not change its historical purchase price.
- Merchant order operations are limited to authorized shops.
- Customer identity and history remain shop-specific.
- Merchant order operations happen through the ERP/web interface; WhatsApp does not replace order management.
- Order state changes follow the approved lifecycle and transition rules.
- Inventory consequences follow finalized Inventory rules; timing and behavior are not yet defined.

## 35. Security Requirements

- Order access is shop-scoped.
- Merchants cannot access another shop's orders.
- Customer order access must not expose another customer's orders.
- Client-provided order IDs do not establish authorization.
- State transitions require server-side authorization.
- Merchant order operations verify access to the relevant shop.
- Public order/status access must not expose unnecessary customer data.
- Sensitive information must not be exposed through unauthorized access.

Follow `.ai/skills/security/SKILL.md` and `.ai/skills/multi-tenancy/SKILL.md`. Do not select authentication technology here.

## 36. Cross-Domain Relationships

These are conceptual domain relationships, not automatically database foreign keys:

### Shops

Provides the tenant context for an order.

### Users & Merchant Accounts

Determines which merchant actors may manage orders for authorized shops.

### Customers

Provides the shop-specific customer context for the purchase.

### Catalog

Provides products, variants, and the applicable shop-specific price at order creation.

### Inventory

Provides stock validation and stock-change interactions according to finalized rules.

### Cart

Provides checkout input; cart state remains separate from the created order.

### Notifications

Receives order-related notification events and defines their delivery.

### Analytics

Consumes order data for shop-level or authorized platform-level reporting.

### Campaigns

May affect product or order pricing only if a future approved rule defines that interaction.

## 37. Unresolved Decisions

No decision below is finalized by this specification.

| Decision | Why unresolved | Impact |
|---|---|---|
| Exact order identifier, order number, and public reference. | No identifier or reference format is approved. | Order identification and customer access cannot be finalized. |
| Order creation validation and transaction boundary. | Checkout dependencies exist, but exact validation and transaction behavior is not specified. | Order creation readiness and failure behavior remain open. |
| Historical snapshot representation and order item structure. | Historical meaning is required, but exact item fields and snapshot approach are unresolved. | Data representation cannot be chosen. |
| Order-time price, item total, and order total calculation. | Shop-specific pricing is approved; full calculation rules are not. | Totals, taxes, fees, and adjustments remain open. |
| Taxes, fees, discounts, and delivery charges. | No formulas or applicable components are finalized. | Final payable total cannot be specified. |
| Customer information and delivery-address snapshot. | Checkout requirements exist, but what Orders preserves historically is unresolved. | Historical customer/order context cannot be finalized. |
| Exact lifecycle state definitions and transition permissions. | The lifecycle is conceptual and incomplete. | State behavior and authorized actors require approval. |
| Acceptance conditions and merchant review details. | Merchant review is required, but exact rules are not documented. | Acceptance behavior cannot be completed by assumption. |
| Preparation, readiness, and completion criteria. | State meanings are conceptual; fulfillment specifics are deferred. | Progression and completion criteria remain open. |
| Rejection reasons and customer notification. | Rejection is supported; reason and notification rules are unspecified. | Rejection records and communications cannot be finalized. |
| Cancellation actors, allowed states, and effects. | Cancellation is not defined. | Customer/merchant cancellation behavior is blocked. |
| Refund behavior. | MVP payment is merchant-handled and no gateway/refund process is approved. | Refund responsibilities and records remain open. |
| Payment status, who records it, proof, and lifecycle effects. | Payment is merchant-handled; status behavior is not defined. | Payment/order coupling cannot be determined. |
| Inventory reservation, deduction timing, restoration, and overselling. | Inventory rules and complete order lifecycle are unresolved. | Stock effects and order acceptance behavior cannot be finalized. |
| Duplicate checkout and repeated state-transition behavior. | No idempotency/concurrency business behavior is approved. | Duplicate orders or operations cannot be handled by an assumed rule. |
| Customer order access and history. | Customer identity is shop-specific, but order access mechanism is unresolved. | Customer visibility cannot be finalized. |
| Merchant and Super Admin order visibility. | Final authorization matrix is not approved. | Access scope and privileged visibility remain open. |
| Order retention, deletion, archival, and behavior after shop deactivation. | Historical-data and deletion policies are unresolved. | Order history and access duration remain open. |
| Pickup versus delivery completion semantics. | Fulfillment choices exist, but completion behavior differs potentially and is unspecified. | `COMPLETED` meaning cannot be fully defined. |

## 38. Explicit Non-Goals

This specification does not define Django models, database schema, migrations, serializers, API endpoints, authentication, authorization implementation, Catalog implementation, Inventory implementation, Cart implementation, payment or refund gateway, WhatsApp provider, delivery-partner management, notification implementation, analytics implementation, or frontend implementation.

## 39. Implementation Gate

> The Orders domain must not be implemented until the unresolved order-lifecycle, inventory, pricing, fulfillment, customer-access, and payment-context decisions are reviewed and approved.

After approval, implementation must follow `AGENTS.md`, `.ai/project-context/product.md`, `.ai/project-context/architecture.md`, `.ai/project-context/business-rules.md`, `.ai/project-context/development-status.md`, `.ai/project-context/domains/users-and-merchant-accounts.md`, `.ai/project-context/domains/shops.md`, `.ai/project-context/domains/catalog.md`, `.ai/project-context/domains/inventory.md`, `.ai/project-context/domains/customers.md`, `.ai/project-context/domains/cart.md`, this domain specification, and relevant engineering skills. The implementation agent must not silently resolve unresolved business decisions.

## 40. Git Workflow

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

Create only `.ai/project-context/domains/orders.md`. Do not modify any other file. Do not create models, migrations, APIs, authentication, authorization, order functionality, payment functionality, or WhatsApp functionality. Do not resolve unresolved business decisions.
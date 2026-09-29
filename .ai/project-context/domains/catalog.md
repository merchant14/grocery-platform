# Catalog Domain Specification

## 1. Domain Purpose

The Catalog domain owns the business concepts for the platform master catalog, shop/merchant catalogs, product definitions and variants, shop product listings, merchant-specific pricing, product availability/visibility, merchant-created products, product review, the relationship between master and merchant catalogs, and customer-facing catalog representation.

The Catalog domain does not own inventory quantities or stock movements, customer identity, carts, orders, payment, WhatsApp, analytics implementation, merchant authentication, or shop identity. Those belong to their respective domains.

## 2. Master Catalog vs Merchant Catalog

Keep these catalog concepts distinct:

```text
Platform Master Catalog
        ↓
Reusable/common product knowledge
        ↓
Merchant/Shop Catalog
        ↓
Shop-specific product listing
        ↓
Customer-facing catalog
```

The platform maintains a master catalog of standardized product knowledge. A shop may use products from it in a shop-specific catalog. The master catalog is not itself a shop's sellable listing, and a master product does not imply that every shop sells it.

Not every merchant product must originate in the master catalog. Merchants may create products for their own catalog even when those products are not in the master catalog. This conceptual distinction does not define the final identity or data relationship between the two catalogs.

## 3. Platform Master Catalog

The Super Admin maintains platform-wide master-catalog information. Approved concepts include product identity, product name, category, product information, variants, and potentially reusable product metadata.

This is platform-global catalog knowledge, not shop-owned data. Exact fields and metadata are not defined here. Do not infer a final master-product schema.

## 4. Merchant / Shop Catalog

Each merchant controls a shop-specific catalog. A shop catalog may present products, categories, variants, shop-specific prices, availability, and customer-facing visibility according to approved requirements.

Distinguish a **Master Product** from a **Shop Product Listing**. A master product does not automatically mean a shop offers it. Shop-specific changes must not modify another shop's catalog or accidentally mutate platform-global master-catalog data.

Do not assume automatic synchronization between master and shop catalogs.

## 5. Merchant-Created Products

A merchant may create a product that is not currently present in the master catalog. It initially belongs to that merchant's shop catalog and may be submitted for Super Admin review.

Conceptually:

```text
Merchant
   ↓
Create product
   ↓
Shop catalog
   ↓
Product may be submitted for review
   ↓
Super Admin review
   ↓
Potential master-catalog inclusion
```

The product may exist for use in its shop independently of master-catalog approval. Do not assume every merchant-created product must originate in or be approved into the master catalog.

## 6. Product Review / Approval

Keep these concerns separate:

### Merchant product existence

A merchant may need to use a product in their own shop catalog even when it is absent from the master catalog.

### Master catalog review

The Super Admin may review a merchant-created product for potential inclusion in the platform master catalog.

Rejection is not known to remove the merchant's shop product, and approval is not known to change product ownership or automatically merge listings. Those outcomes are **Not Finalized / Require Decision**. The exact review states, approval workflow, matching, merging, and post-review behavior belong in future Catalog business rules.

## 7. Product Identity

Distinguish conceptually among a platform master product, a shop-specific product/listing, and a product variant. Do not assume they always share an identity or that a shop product must have a master product.

Whether a merchant product can reference a master product, be completely independent, or later become linked to a master product is unresolved. Do not prescribe an identifier strategy.

## 8. Product Variants

Products may have variants. Examples such as 500 g, 1 kg, 250 ml, 1 L, a pack of 6, or a pack of 12 are illustrative only, not finalized product requirements.

Variants may affect what a customer selects, the applicable price, inventory interaction, and ordering. Exact variant structure, identity, and which properties belong to the master product versus a shop listing are unresolved. Do not define a database structure here.

## 9. Pricing

Merchants configure shop-specific selling prices. A master catalog product does not establish a universal selling price. One merchant's price changes must not change another merchant's price, and customer checkout uses the applicable shop-specific price.

Do not assume platform-wide prices, dynamic pricing, discounts, tax calculations, currency conversion, or price history. If price history or discounts are needed, they require explicit business decisions.

## 10. Availability and Visibility

Keep these concepts distinct:

- **Product availability:** whether the shop currently offers the product.
- **Catalog visibility:** whether the product is displayed to customers.
- **Inventory availability:** whether stock exists; actual stock quantities are owned by Inventory.

Customers scanning a shop's QR should see products available for that shop. Product visibility and availability follow the relevant merchant/shop configuration. The exact relationship between listing availability, catalog visibility, inventory quantity, and customer ordering is **Not Finalized / Require Decision**. Do not collapse these concepts or define stock behavior here.

## 11. Categories

The platform master catalog contains standardized category concepts, and customers can browse categories. The following are unresolved: whether shops may create their own categories, whether merchant categories can differ from master categories, whether categories are shared across shops, and whether or how a shop category relates to a master category.

Do not invent a category hierarchy or category ownership model.

## 12. Customer-Facing Catalog

The customer-facing catalog flow is conceptually:

```text
Shop QR
   ↓
Shop public page
   ↓
Categories
   ↓
Products
   ↓
Variants
   ↓
Quantity selection
   ↓
Cart
```

The Catalog domain supplies product and catalog information; it does not own the Cart. Customers should only see products belonging to the selected shop's catalog. Results must not expose another shop's products or private catalog data.

## 13. Shop Isolation

Follow `.ai/skills/multi-tenancy/SKILL.md` as the governing engineering rule.

- Merchant catalogs and product listings are shop-scoped.
- Merchant product data must never cross shop boundaries.
- Customer catalog requests resolve within the intended shop context.
- A product identifier alone does not bypass shop isolation.
- Related variants must remain within the proper product/shop context.
- Platform master-catalog data is global/shared data, distinct from tenant-owned listings.

This describes the required business/security boundary, not its technical enforcement mechanism.

## 14. Master Catalog Governance

The Super Admin maintains platform master-catalog information and may review merchant-created products for possible inclusion. These are the approved governance concepts.

Additional administrative powers, exact approval states, decision criteria, matching/merge behavior, and post-approval changes are not defined. Do not invent them.

## 15. Product Lifecycle

### Master Product

The platform maintains master-catalog information. Its complete lifecycle and permitted state changes are not defined.

### Shop Product

A merchant can have a product listing in the shop catalog, including a product created outside the master catalog. Its full lifecycle and state changes are not defined.

### Product Variant

A product may have variants. Variant lifecycle, availability, and relationship to master versus shop products are not defined.

Do not introduce states such as `DRAFT`, `ACTIVE`, `INACTIVE`, `ARCHIVED`, or `REJECTED` as finalized Catalog states. If states are needed, define them in approved domain requirements, including who can change them and what customers see.

## 16. Product Editing

The Super Admin maintains master-catalog information; merchants manage shop-specific catalog configuration. The following are unresolved: which master-product attributes Super Admin may edit, which listing attributes merchants may edit, whether merchants can propose or modify master information, and whether master changes propagate to shop listings.

Do not assume propagation or that a merchant's listing update modifies a master product or another shop's listing.

## 17. Product Deletion / Deactivation

Deletion and deactivation behavior is not finalized. Decisions are required about whether merchants can delete or only hide a shop product, the effects on existing carts and orders, historical order items, inventory, restoration, and deleting a master product referenced by shops.

Do not assume hard deletion or soft deletion.

## 18. Inventory Boundary

### Catalog owns conceptually

- Product and variant definitions.
- Shop product listings.
- Shop-specific price.
- Catalog visibility and listing availability, subject to decisions.

### Inventory owns

- Stock quantity.
- Stock movements.
- Stock deductions.
- Low-stock behavior.
- Inventory state and algorithms.

Catalog may consume inventory-provided availability information according to an approved interaction. Do not specify inventory algorithms or stock-deduction behavior here.

## 19. Cart and Order Boundary

Catalog describes what product a shop offers and the applicable shop-specific price. Cart describes what a customer intends to buy. Order records what the customer actually ordered.

Catalog does not define cart or order schemas. The relationship between catalog edits and existing cart contents or orders is unresolved and must be specified by the relevant domain decisions.

## 20. Historical Pricing / Order Snapshot

The business rules say to consider whether historical records preserve the information that existed when an event occurred, including order information and the price used for an order. They also mark the exact snapshot strategy and historical-data requirements as unresolved.

Therefore, whether an order must preserve a historical product description, variant information, price, or other catalog details is **Not Finalized / Require Decision**. No snapshot implementation or schema is defined here.

## 21. Business Invariants

The following invariants are supported by the product and business-rule sources:

- A shop exposes only products belonging to its catalog/context.
- A merchant cannot modify another shop's product listing.
- Master catalog data is platform-wide and distinct from shop-owned data.
- Merchant-specific prices belong to the applicable shop context.
- Customer-facing catalog results respect the intended shop context.
- Product variants remain associated with the correct product/shop context.
- Inventory quantity is owned by Inventory, not Catalog.

Whether existing orders preserve a historical catalog/price snapshot is unresolved. Do not treat that candidate requirement as a finalized invariant until the business decision is approved.

## 22. Security Requirements

- Shop-scoped merchant catalog operations require authorized access to that shop.
- Public catalog requests resolve to the intended shop.
- Client-provided identifiers cannot bypass tenant isolation.
- Merchants cannot modify master-catalog data unless explicitly authorized.
- One merchant's product listing cannot be modified through another shop's context.
- Super Admin platform-level actions require appropriate authorization.
- Public customer access exposes only intended customer-facing information.

Follow `.ai/skills/security/SKILL.md` and `.ai/skills/multi-tenancy/SKILL.md`. Do not select authentication technology or authorization implementation here.

## 23. Cross-Domain Relationships

These are conceptual domain relationships, not automatically database foreign keys:

### Shops

Provides the intended shop/tenant context.

### Users & Merchant Accounts

Determines who may manage a shop catalog.

### Inventory

Provides the stock information/availability interaction; inventory owns quantities and movements.

### Customers

Consumes customer-facing catalog information; customer identity remains shop-specific.

### Cart

Consumes products, variants, and shop-specific prices.

### Orders

References purchased products/variants. Historical order meaning and pricing behavior require the decision described above.

### Campaigns

May reference products or catalog items if later approved.

### Analytics

Consumes catalog/product information for reporting while respecting tenant scope.

## 24. Unresolved Decisions

No decision below is finalized by this specification.

| Decision | Why unresolved | Impact |
|---|---|---|
| Exact product identity model. | Primary-key strategy and product identity details are not approved. | Product references and identity cannot be finalized. |
| Master product versus shop product relationship. | The product supports both master products and merchant-created products but defines no final linkage. | Reuse, independence, and cross-catalog references remain open. |
| Whether merchant products can remain independent from the master catalog. | They may exist in merchant catalogs before review; long-term relationship is unspecified. | Merchant product lifecycle and master-catalog handling remain open. |
| Master-catalog approval, rejection, and inclusion workflow. | Review is required conceptually; exact outcomes are deferred. | Product review behavior cannot be implemented beyond the concept. |
| Whether rejection affects a merchant's existing listing. | Existing requirements do not define the effect. | Shop listing availability after rejection is unknown. |
| Whether approval changes ownership, links products, or merges catalog entries. | Catalog merge/link behavior is explicitly deferred. | Cross-catalog product identity remains undefined. |
| Master-product editing permissions. | Super Admin maintains the master catalog, but exact editing authority and fields are unspecified. | Administrative changes cannot be scoped. |
| Merchant product/listing editing permissions. | Shop-specific management is required, but exact editable properties and rules are not finalized. | Merchant catalog operations remain underspecified. |
| Whether master-catalog changes propagate to shops. | No synchronization behavior is approved. | Existing shop listings must not be assumed to update automatically. |
| Variant identity and structure. | Variants are required conceptually, but their representation and ownership are open. | Product selection and downstream inventory/order relationships remain open. |
| Category ownership and merchant-created categories. | Standardized master categories exist; shop category behavior is unspecified. | Category organization and mapping remain open. |
| Product lifecycle states and transitions. | No Catalog state machine is finalized. | Visibility and review transitions cannot be fully specified. |
| Product visibility rules. | Customers see products available to a shop, but exact visibility controls are not defined. | Customer-facing display behavior remains partly open. |
| Product availability and its relationship to inventory. | Catalog listing availability and Inventory stock are distinct; their interaction is undefined. | A product's orderability cannot be determined from Catalog rules alone. |
| Pricing model, price history, discounts, taxes, and currency. | Only independent shop-specific prices are approved; these details are not. | Price calculation and historical price behavior remain open. |
| Merchant product deletion/deactivation and restoration. | Deletion semantics are unresolved. | Effects on carts, orders, and listings cannot be determined. |
| Master product deletion when shops reference it. | Master-product reference behavior is unresolved. | Reference integrity and shop behavior after removal are unknown. |
| Historical order product/variant/price snapshot requirements. | Historical state should be considered, but exact snapshot requirements are unresolved. | Catalog changes may affect historical interpretation until decided. |
| Catalog ordering/sorting. | Customer category/product browsing exists, but ordering rules are unspecified. | Display order cannot be treated as an approved business rule. |

## 25. Explicit Non-Goals

This specification does not define Django models, database schema, migrations, serializers, API endpoints, URL routing, authentication, authorization implementation, inventory schema or deductions, cart schema, order schema, payment processing, WhatsApp integration, campaign implementation, analytics implementation, frontend implementation, or image/file storage implementation.

## 26. Implementation Gate

> The Catalog domain must not be implemented until the unresolved decisions required for implementation are reviewed and approved.

After approval, implementation must follow `AGENTS.md`, `.ai/project-context/product.md`, `.ai/project-context/architecture.md`, `.ai/project-context/business-rules.md`, `.ai/project-context/development-status.md`, `.ai/project-context/domains/users-and-merchant-accounts.md`, `.ai/project-context/domains/shops.md`, this domain specification, and relevant engineering skills. The implementation agent must not silently resolve unresolved business decisions.

## 27. Git Workflow

Follow the mandatory repository workflow:

```text
git status
git checkout main
git pull origin main
git checkout -b <task-id>/<short-description>
```

- Never work directly on `main`.
- Inspect existing changes first; never automatically discard them.
- Destructive Git commands require explicit approval.
- Ask for a task ID if none is provided before creating a branch.
- Keep commits small and task-related; never commit secrets.
- Push the task branch and create a PR against `main`.
- Do not force-push or rewrite history without authorization.

Follow `AGENTS.md` for the complete workflow.

## Final Requirement

Create only `.ai/project-context/domains/catalog.md`. Do not modify any other file. Do not create models, migrations, APIs, authentication, authorization, or catalog functionality. Do not resolve unresolved business decisions.
# FreshTrack – Inbound Fruit & Vegetable Receiving System

## 1. Document Overview & Objective

The purpose of this document is to outline the business and technical requirements for FreshTrack, an internal logistics application designed to streamline and digitize the receiving of fresh produce (fruits and vegetables) at regional fulfillment Hubs.

Currently, manual tracking of vendor deliveries against physical stock causes inventory inaccuracies, delayed updates, and financial leakage. This application will allow Central Operations to upload expected inventory via master invoices, and enable Hub Users to physically scan and verify incoming items directly on the warehouse receiving dock.

## 2. User Roles & Role-Based Access Control (RBAC)

The system requires strict role-based access control to ensure operational boundaries, security, and data isolation.

| Role          | Operational Scope        | Key Permissions                                                                                                                                  |
| ------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Central Admin | Global / Cross-Warehouse | Full system configuration, user-to-hub mapping, master invoice uploads, and global cross-warehouse reporting.                                    |
| Hub User      | Assigned Warehouse Only  | Select and enter assigned warehouse, view expected invoices mapped to that specific location, and execute the physical scan-to-receive workflow. |

## 3. Functional Requirements

### 3.1. User Management & Authentication

- Secure Login: Standard secure login (email/username and password) with session management.
- User-to-Warehouse Mapping: A Central Admin must be able to map individual Hub Users to one or more physical warehouses.
- Data Isolation: A Hub User must only be allowed to view data, access invoices, and perform scanning operations for the warehouse they are currently logged into and authorized to access.

### 3.2. Central Inbound Planning (Invoice Ingestion)

- Invoice Ingestion: Central Admin can upload vendor invoices (supported formats: CSV/Excel) to establish expected delivery schedules.
- Data Fields Required per Invoice Line:
  - Invoice_ID (String, Unique)
  - Vendor_Name (String)
  - Target_Warehouse_ID (String)
  - Item_SKU (String)
  - Item_Name (String)
  - Expected_Quantity (Positive Integer, representing Units/Eaches)
- Validation: The system must validate that the Target_Warehouse_ID exists in the system before committing the upload.

### 3.3. Hub Receiving Workflow (The "Scan & Count" Module)

- Warehouse Entry: Upon logging in, the Hub User enters or selects their active physical Warehouse_ID to unlock and access their dashboard.
- Invoice Selection: The user selects the active Invoice_ID currently being unloaded at their dock.
- Scan-to-Receive:
  - The application interface must be designed to integrate smoothly with a physical hardware barcode scanner or mobile device camera.
  - Scanning a valid barcode containing the Item_SKU automatically increments the Received Quantity by +1 (Each/Unit) for that specific item in the ledger.
  - The UI must display real-time progress of the count relative to what was expected.

### 3.4. Reporting & Analytics

- Reconciliation Report: Central Admin must be able to download a reconciliation report (CSV/Excel) filtered by Date Range, Warehouse, or Vendor.
- Report Schema Requirements: The output must display the performance of each delivery line:
  - Invoice_ID
  - Vendor_Name
  - Warehouse_ID
  - Item_SKU
  - Item_Name
  - Expected_Quantity
  - Received_Quantity
  - Variance (calculated dynamically)
- Variance formula:
  - `{Variance} = {Expected_Quantity} - {Received_Quantity}`

## 4. Technical & Non-Functional Requirements

- Aesthetics & UI/UX: The interface must be optimized for speed, clarity, and ease of use in a fast-paced, rugged, and low-light warehouse environment.
- Audit Trail: Every barcode scan, manual increment, or override must log a detailed record including the system timestamp, the Invoice_ID, the Item_SKU, and the User_ID who performed the action.
- Performance: The receiving ingestion system must handle rapid-fire barcode scan inputs without lagging, skipping counts, or causing UI freeze.

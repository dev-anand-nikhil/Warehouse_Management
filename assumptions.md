# Assumptions

- Barcode format is assumed to be `SKU-{sku}`.
- Invoice upload is primarily supported via CSV format.
- User authentication uses JWT stored in local storage for the frontend.
- Central Admin can create warehouses and assign users, while Hub Users scan and adjust inventory.
- The app is designed for local Docker Compose development without cloud dependencies.

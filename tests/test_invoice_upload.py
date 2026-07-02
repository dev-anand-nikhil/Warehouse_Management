import io


def test_upload_invoice_csv(client):
    csv_content = 'Invoice_ID,Vendor_Name,Warehouse_ID,Item_SKU,Item_Name,Expected_Quantity\nINV-001,Fresh Farms,1,SKU123,Apple,10\n'
    response = client.post(
        '/api/invoices/upload',
        files={'file': ('invoice.csv', csv_content, 'text/csv')},
    )
    assert response.status_code == 201
    assert response.json()['inserted'] == 1

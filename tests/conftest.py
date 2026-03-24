import pytest
from api.products_api import ProductsAPI

@pytest.fixture(scope="function")
def product_api():
    """Fixture to initialize the ProductsAPI object."""
    return ProductsAPI()

@pytest.fixture(scope="function")
def temp_product(product_api):
    """
    PRD-001 & PRD-019 Lifecycle Fixture.
    Creates a temporary product and deletes it after the test.
    """
    payload = {
        "name": "Automated Test Product",
        "type": "simple",
        "regular_price": "29.99",
        "description": "This is a temporary product for automation testing.",
        "short_description": "Auto-generated",
        "categories": [{"id": 9}],
        "sku": f"TEST-SKU-{pytest.importorskip('random').randint(1000, 9999)}"
    }

    response = product_api.create_product(payload)
    product_data = response.json()
    product_id = product_data.get("id")

    yield product_data

    if product_id:
        print(f"\n[Teardown] Cleaning up: Deleting product ID {product_id}")
        product_api.delete_product(product_id, force=True)

@pytest.fixture(scope="function")
def multiple_products(product_api):
    """
    Pagination Fixture.
    Creates 3 products before the test and deletes them after.
    """
    created_ids = []

    for i in range(3):
        payload = {
            "name": f"Pagination Test Product {i+1}",
            "type": "simple",
            "regular_price": f"{10 + i}.00",
            "sku": f"PAGI-SKU-{i+1}-{pytest.importorskip('random').randint(1000, 9999)}"
        }
        response = product_api.create_product(payload)
        product_id = response.json().get("id")
        if product_id:
            created_ids.append(product_id)

    yield created_ids

    for product_id in created_ids:
        print(f"\n[Teardown] Deleting pagination product ID {product_id}")
        product_api.delete_product(product_id, force=True)
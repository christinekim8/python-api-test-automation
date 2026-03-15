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
    1. Setup: Creates a temporary product before the test.
    2. Test: Provides the created product data to the test function.
    3. Teardown: Permanently deletes the product after the test completes.
    """
    # 1. Setup: Define sample product data
    payload = {
        "name": "Automated Test Product",
        "type": "simple",
        "regular_price": "29.99",
        "description": "This is a temporary product for automation testing.",
        "short_description": "Auto-generated",
        "categories": [{"id": 9}], # You can adjust category IDs as needed
        "sku": f"TEST-SKU-{pytest.importorskip('random').randint(1000, 9999)}" 
    }

    # 2. Create the product
    response = product_api.create_product(payload)
    product_data = response.json()
    product_id = product_data.get("id")

    # Yield the product data to the test
    yield product_data

    # 3. Teardown: Hard Delete the product to keep DB clean
    if product_id:
        print(f"\n[Teardown] Cleaning up: Deleting product ID {product_id}")
        product_api.delete_product(product_id, force=True)
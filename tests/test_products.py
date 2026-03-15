import pytest
import uuid

class TestProducts:
    """
    Test suite for WooCommerce Products API.
    Focuses on Full Lifecycle and Data Integrity.
    """

    def test_create_and_verify_product_lifecycle(self, product_api, temp_product):
        """
        PRD-001 & PRD-019: Full Lifecycle Test
        1. Create a product (Handled by 'temp_product' fixture)
        2. Verify the product exists and has correct data
        3. Hard delete is performed automatically after this test
        """
        
        # [Step 1] Retrieve the product ID from the fixture
        product_id = temp_product.get("id")
        expected_name = temp_product.get("name")
        expected_price = temp_product.get("regular_price")

        print(f"\n[Test] Verifying product ID: {product_id}")

        # [Step 2] API Call: Get the product details by ID
        response = product_api.get_product(product_id)
        
        # [Step 3] Assertions: Quality Gates
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
        
        actual_data = response.json()
        assert actual_data["name"] == expected_name, "Product name mismatch!"
        assert actual_data["regular_price"] == expected_price, "Product price mismatch!"
        
        print(f"[Test] Success: Product '{expected_name}' verified correctly.")

    def test_list_all_products_status_code(self, product_api):
        """
        PRD-011: Verify that the product list API returns a 200 status code.
        """
        response = product_api.list_all_products()
        assert response.status_code == 200, "Failed to retrieve product list"
        
        products = response.json()
        assert isinstance(products, list), "Response is not a list"
        print(f"[Test] Successfully retrieved {len(products)} products.")

    @pytest.mark.parametrize("invalid_payload, expected_status, test_case_id", [
        # PRD-003: Instead of empty string, try sending a wrong data type for the whole object
        # (Note: WooCommerce is very flexible, so achieving 400 can be tricky!)
        ({"name": ["This should be a string, not a list"]}, 400, "PRD-003: Invalid Name Format"),
    
        # PRD-005: Use a value that absolutely cannot be cast to a number
        ({"name": "Test", "regular_price": True}, 400, "PRD-005: Boolean Price"),
    ])

    def test_create_product_negative_cases(self, product_api, invalid_payload, expected_status, test_case_id):
        """
        Data-Driven Negative Testing
        Ensures the system correctly handles invalid input by returning appropriate error status codes.
        """
        print(f"\n[Running] {test_case_id}")

        # [Step 1] Attempt to create a product with invalid data
        response = product_api.create_product(invalid_payload)

        # [Step 2] Assert that the API responds with the expected error status code
        # Note: WooCommerce might return 400 or other codes based on server-side validation rules.
        assert response.status_code == expected_status, \
            f"{test_case_id} failed: Expected {expected_status} but got {response.status_code}"

        # [Step 3] Log the success of error handling
        error_response = response.json()
        print(f"[Success] {test_case_id} properly handled. Error message: {error_response.get('message')}")

    def test_create_product_duplicate_sku(self, product_api):
        """
        PRD-007: Duplicate SKU Validation
        Verifies that the system prevents creating two products with the same SKU.
        This test checks business logic and state management.
        """
        # [Step 1] Setup: Generate a unique SKU for this test session
        unique_sku = f"TEST-SKU-{uuid.uuid4().hex[:6].upper()}"
        payload = {
            "name": "Original Product",
            "type": "simple",
            "regular_price": "20.00",
            "sku": unique_sku
        }

        print(f"\n[Test] Creating first product with unique SKU: {unique_sku}")
        
        # [Step 2] Action: Create the first product (Expected: 201 Created)
        first_response = product_api.create_product(payload)
        assert first_response.status_code == 201, "Initial product creation failed."
        
        product_id = first_response.json().get("id")

        try:
            # [Step 3] Action: Try to create another product with the SAME SKU
            print(f"[Test] Attempting to create second product with duplicate SKU: {unique_sku}")
            second_response = product_api.create_product(payload)

            # [Step 4] Verification: API must return 400 Bad Request
            assert second_response.status_code == 400, \
                f"Expected 400 for duplicate SKU, but got {second_response.status_code}"

            # [Step 5] Verification: Check the specific error code from WooCommerce
            error_data = second_response.json()
            assert error_data.get('code') == 'product_invalid_sku', "Incorrect error code for duplicate SKU"
            print(f"[Success] Duplicate SKU correctly blocked with message: {error_data.get('message')}")

        finally:
            # [Step 6] Teardown: Cleanup the first product to keep the DB clean
            # Using 'finally' ensures deletion even if the assertions above fail.
            if product_id:
                product_api.delete_product(product_id)
                print(f"[Teardown] Deleted the original test product (ID: {product_id}).")

    def test_product_pagination_integrity(self, product_api):
        """
        PRD-011: Advanced Pagination Logic
        Verifies that there is no data overlap between different pages.
        Demonstrates complex data validation using Python sets.
        """
        per_page = 2
        
        # [Step 1] Fetch Page 1 (2 products)
        print(f"\n[Test] Fetching Page 1 with per_page={per_page}")
        page1_response = product_api.list_all_products(params={"page": 1, "per_page": per_page})
        assert page1_response.status_code == 200
        page1_ids = [item['id'] for item in page1_response.json()]
        
        # [Step 2] Fetch Page 2 (Remaining products)
        print(f"[Test] Fetching Page 2 with per_page={per_page}")
        page2_response = product_api.list_all_products(params={"page": 2, "per_page": per_page})
        assert page2_response.status_code == 200
        page2_ids = [item['id'] for item in page2_response.json()]

        print(f"[Debug] Page 1 IDs: {page1_ids}")
        print(f"[Debug] Page 2 IDs: {page2_ids}")

        # [Step 3] Verification: Check for overlapping IDs using Python Sets
        # intersection() returns elements common to both sets
        overlap = set(page1_ids).intersection(set(page2_ids))
        
        assert len(overlap) == 0, f"Pagination Error: Overlapping product IDs found: {overlap}"
        assert len(page1_ids) > 0, "Page 1 should not be empty for this test."
        
        print("[Success] Pagination integrity verified. No data overlap found between Page 1 and Page 2.")
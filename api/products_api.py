from api.base_api import BaseAPI

class ProductsAPI(BaseAPI):
    """
    API methods related to WooCommerce Products.
    Inherits from BaseAPI to use common auth and request logic.
    """

    def create_product(self, data):
        """
        PRD-001: Create a new product.
        :param data: Dictionary containing product details (name, type, regular_price, etc.)
        :return: Response object
        """
        return self.post("products", data)

    def get_product(self, product_id):
        """
        Retrieve a single product by ID.
        """
        return self.get(f"products/{product_id}")

    def delete_product(self, product_id, force=True):
        """
        PRD-019: Delete a product.
        :param product_id: ID of the product to delete.
        :param force: If True, permanently deletes the product (Hard Delete).
                      If False, moves it to the trash (Soft Delete).
        :return: Response object
        """
        # WooCommerce API uses 'force' parameter for permanent deletion
        params = {"force": force}
        return self.delete(f"products/{product_id}", params=params)

    def list_all_products(self, params=None):
        """
        PRD-011: Get a list of products with optional pagination.
        """
        return self.get("products", params=params)
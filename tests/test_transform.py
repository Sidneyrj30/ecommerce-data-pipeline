import pytest

from src.transform.transform import transform_and_validate


@pytest.mark.parametrize(
    "test_input, expected_valid, expected_discarded",
    [
        pytest.param(
            [
                {
                    "title": "Product test 1",
                    "price": 14.99,
                    "discountPercentage": 9.84,
                    "rating": 2.86,
                    "category": "beauty",
                }
            ], 
            [],  
            1, 
            id="without-id",
        ),
        pytest.param(
            [
                {
                    "id": 2,
                    "title": None,
                    "price": 16.40,
                    "discountPercentage": 9.84,
                    "rating": 4.86,
                    "category": "beauty",
                }
            ], 
            [],  
            1, 
            id="title-none",
        ),
        pytest.param(
            [
                {
                    "id": 3,
                    "title": "Product test 1",
                    "price": 0,
                    "discountPercentage": 10,
                    "rating": 1.78,
                    "category": "beauty",
                }
            ], 
            [
                {
                    "id": 3,
                    "title": "Product test 1",
                    "price": 0,
                    "discount_percentage": 10,
                    "rating": 1.78,
                    "category": "beauty",
                }
            ],  
            0, 
            id="price-zero-valid",
        ),
        pytest.param(
            [
                {
                    "id": 4,
                    "title": "Product test 1",
                    "rating": 3.78,
                    "category": "beauty",
                    "price": 14.99,
                    "discountPercentage": 9.84,
                }
            ], 
            [
                {
                    "id": 4,
                    "title": "Product test 1",
                    "price": 14.99,
                    "discount_percentage": 9.84,
                    "rating": 3.78,
                    "category": "beauty",
                }
            ],  
            0, 
            id="product-valid",
        ),
    ],
)
def test_transform_and_validate(test_input, expected_valid, expected_discarded):
    valid_products, discarded_count = transform_and_validate(test_input)

    assert valid_products == expected_valid
    assert discarded_count == expected_discarded

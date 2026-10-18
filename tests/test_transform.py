from src.transform.transform import transform_and_validate

product_mock = [
    {
        "title": "Product test 1",
        "rating": 2.86,
        "description": "ipsum loren test 1",
        "category": "beauty",
        "price": 14.99,
        "discountPercentage": 9.84,
    },
    {
        "id": 2,
        "title": "Product test 1",
        "rating": 4.86,
        "description": "ipsum loren test 2",
        "category": "beauty",
        "discountPercentage": 9.84,
    },
    {
        "id": 3,
        "title": "Product test 1",
        "rating": 1.86,
        "category": "beauty",
        "price": 14.99,
        "discountPercentage": 9.84,
    },
    {
        "id": 4,
        "title": "Product test 1",
        "rating": 3.78,
        "category": "beauty",
        "price": 14.99,
        "discountPercentage": 9.84,
    },
    {
        "id": 5,
        "title": "Product test 1",
        "rating": 4.45,
        "category": "beauty",
        "price": 14.99,
        "discountPercentage": 9.84,
    },
]


def test_transform_and_validate():
    valid, discarded = transform_and_validate(product_mock)

    assert discarded == 2
    assert valid == [
        {
            "id": 3,
            "title": "Product test 1",
            "rating": 1.86,
            "category": "beauty",
            "price": 14.99,
            "discount_percentage": 9.84,
        },
        {
            "id": 4,
            "title": "Product test 1",
            "rating": 3.78,
            "category": "beauty",
            "price": 14.99,
            "discount_percentage": 9.84,
        },
        {
            "id": 5,
            "title": "Product test 1",
            "rating": 4.45,
            "category": "beauty",
            "price": 14.99,
            "discount_percentage": 9.84,
        },
    ]

import pytest

from src.transform.transform import transform_and_validate

BASE_PRODUCT = {
    "id": 1,
    "title": "Product test 1",
    "price": 14.99,
    "discountPercentage": 9.84,
    "rating": 2.86,
    "category": "beauty",
}


def to_expected(product: dict) -> dict:
    """Retorna uma cópia do produto com a chave camelCase convertida para snake_case."""
    expected = product.copy()
    if "discountPercentage" in expected:
        expected["discount_percentage"] = expected.pop("discountPercentage")
    return expected


def create_payload(remove_keys: list | None = None, **overrides) -> dict:
    """Gera um dicionário derivado do BASE_PRODUCT aplicando remoções e atualizações."""
    payload = BASE_PRODUCT.copy()
    if remove_keys:
        for key in remove_keys:
            payload.pop(key, None)
    payload.update(overrides)
    return payload


@pytest.mark.parametrize(
    "test_input, expected_valid, expected_discarded",
    [
        pytest.param(
            [create_payload(remove_keys=["id"])],
            [],
            1,
            id="without-id-invalid",
        ),
        pytest.param(
            [create_payload(title=None)],
            [],
            1,
            id="title-none-invalid",
        ),
        pytest.param(
            [create_payload(price=0)],
            [to_expected(create_payload(price=0))],
            0,
            id="price-zero-valid",
        ),
        pytest.param(
            [BASE_PRODUCT],
            [to_expected(BASE_PRODUCT)],
            0,
            id="product-valid",
        ),
        pytest.param(
            [create_payload(discountPercentage=0)],
            [to_expected(create_payload(discountPercentage=0))],
            0,
            id="product-zero-discount-valid",
        ),
        pytest.param(
            [create_payload(rating=0)],
            [to_expected(create_payload(rating=0))],
            0,
            id="product-zero-rating-valid",
        ),
        pytest.param(
            [create_payload(remove_keys=["category"])],
            [to_expected(create_payload(remove_keys=["category"], category=None))],
            0,
            id="product-none-category-valid",
        ),
        pytest.param(
            [create_payload(remove_keys=["price"])],
            [],
            1,
            id="product-without-price-invalid",
        ),
    ],
)
def test_transform_and_validate(test_input, expected_valid, expected_discarded):
    valid_products, discarded_count = transform_and_validate(test_input)

    assert valid_products == expected_valid
    assert discarded_count == expected_discarded

import json
import logging
from pathlib import Path


def read_latest_raw_file(raw_path: str) -> list[dict]:
    """Lê o arquivo JSON mais recente gerado pela etapa de extração"""
    path = Path(raw_path)

    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"O diretório especificado não existe: {raw_path}")

    json_files = list(path.glob("*.json"))

    if not json_files:
        raise FileNotFoundError(
            f"Nenhum arquivo .json foi encontrado em '{raw_path}'. "
            "Certifique-se de executar a etapa de extração primeiro."
        )

    last_file = max(json_files)
    logging.info(f"last_file found: {last_file}")

    with open(last_file, "r", encoding="utf-8") as file:
        return json.load(file)


def transform_and_validate(file_data: list[dict]) -> tuple[list[dict], int]:
    """Valida e transforma os produtos; retorna os válidos e a contagem de descartados."""
    required_fields = ("id", "title", "price", "discountPercentage", "rating")
    discarded_count = 0
    valid_products = []
    for item in file_data:
        if any(item.get(field) is None for field in required_fields):
            product_id = item.get("id", "Desconhecido")
            logging.warning(f"Campos obrigatórios ausentes no produto ID: {product_id}")
            discarded_count += 1
            continue
        valid_products.append(
            {
                "id": item["id"],
                "title": item["title"],
                "price": item["price"],
                "discount_percentage": item["discountPercentage"],
                "rating": item["rating"],
                "category": item.get("category"),
            }
        )

    return valid_products, discarded_count

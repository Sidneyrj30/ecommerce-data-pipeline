import json
import logging
from datetime import datetime
from pathlib import Path

import requests


def extract_products(api_url: str) -> list[dict]:
    """Extrai todos os produtos de uma API paginada de forma iterativa."""
    products = []
    skip = 0
    limit = 30
    total = None

    while total is None or skip < total:
        try:
            response = requests.get(f"{api_url}?limit={limit}&skip={skip}", timeout=5)
            response.raise_for_status()

            response_sample = response.json()
            products_sample = response_sample.get("products", [])
            skip = response_sample.get("skip", 0) + limit
            products.extend(products_sample)

            if total is None:
                total = response_sample.get("total", 0)

        except requests.HTTPError as error:
            logging.error(f"Error status: {error}")
            raise

        except requests.exceptions.ConnectionError as error:
            logging.error(f"Erro de conexão: {error}")
            raise

        except requests.exceptions.Timeout as error:
            logging.error(f"Timeout ao consultar a API: {error}")
            raise

    logging.info(f"Busca finalizada com {len(products)} produtos encontrados")
    return products


def save_products_on_raw_file(products: list[dict], raw_path: str) -> Path:
    """Salva a lista de produtos extraídos em um arquivo JSON com carimbo de data/hora."""
    path = Path(raw_path)

    path.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = path / f"{today}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(products, file)

    return file_path

import json
import logging
from datetime import datetime

import requests

from src.config import API_URL, RAW_DATA_PATH


def extract_products() -> list[dict]:
    products = []
    skip = 0
    limit = 30
    total = None

    while total is None or skip < total:
        try:
            response = requests.get(f"{API_URL}?limit={limit}&skip={skip}", timeout=5)
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


def save_products_on_raw_file(products: list[dict]):
    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"{RAW_DATA_PATH}/{today}.json", "w") as file:
        json.dump(products, file)

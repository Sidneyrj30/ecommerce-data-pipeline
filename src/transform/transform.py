import os
import sys
import logging
import json
from src.config import RAW_DATA_PATH
from src.transform.database import create_products_table, get_connection, upsert_products

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

files = os.listdir(RAW_DATA_PATH)
list_files = list(filter(lambda f: f.endswith('.json'), files))

if not list_files:
    sys.exit("Nenhum arquivo .json encontrado em data/raw/. Rode a extração primeiro.")

last_file = max(list_files)
logging.info(f"last_file found: {last_file}")

with open(os.path.join(RAW_DATA_PATH, last_file), "r") as file:
    file_data = json.load(file)

logging.info(f"tipo do arquivo: {type(file_data)}")

count = 0
filter_data = []
for item in file_data:
    if item.get('title') is None or item.get('price') is None or item.get('discountPercentage') is None or item.get('rating') is None:
        logging.warning(f"Tem valores faltando no produto {item['id']}")
        count += 1
        continue;
    filter_data.append(
        {
            'id': item['id'],
            'title': item['title'],
            'price':item['price'],
            'discount_percentage' : item['discountPercentage'],
            'rating': item['rating'],
            'category': item['category']
        }
    )

logging.info(f"Produtos válidos: {len(filter_data)} | Produtos descartados: {count}")

with get_connection() as conn:
    create_products_table(conn)
    upsert_products(conn, filter_data)
conn.close()

import logging

from src.config import API_URL, DATABASE_PATH, RAW_DATA_PATH
from src.extract.extract import extract_products, save_products_on_raw_file
from src.load.load import load_to_db
from src.transform.transform import read_latest_raw_file, transform_and_validate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    # Etapa 1: Extração
    logging.info("Iniciando a busca por produtos...")
    products = extract_products(API_URL)
    save_products_on_raw_file(products, RAW_DATA_PATH)
    logging.info("Arquivo com os dados dos produtos criado")

    # Etapa 2: Transformação e validação
    products = read_latest_raw_file(RAW_DATA_PATH)
    valid, discarded = transform_and_validate(products)
    logging.info(f"Produtos válidos: {len(valid)} | Produtos descartados: {discarded}")

    # Etapa 3: Carga (Load)
    load_to_db(valid, DATABASE_PATH)
    logging.info("Pipeline finalizada com sucesso")


if __name__ == "__main__":
    main()

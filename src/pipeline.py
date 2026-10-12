import logging

from src.config import RAW_DATA_PATH
from src.extract.extract import extract_products, save_products_on_raw_file
from src.load.load import load_to_db
from src.transform.transform import read_latest_raw_file, transform_and_validate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    logging.info("Iniciando a busca por produtos...")
    products = extract_products()
    save_products_on_raw_file(products)
    logging.info("Arquivo com os dados dos produtos criado")

    products = read_latest_raw_file(RAW_DATA_PATH)
    valid, discarded = transform_and_validate(products)
    logging.info(f"Produtos válidos: {len(valid)} | Produtos descartados: {discarded}")
    load_to_db(valid)
    logging.info("Processo finalizado")


if __name__ == "__main__":
    main()

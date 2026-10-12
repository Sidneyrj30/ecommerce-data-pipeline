import json
import logging
from pathlib import Path


def read_latest_raw_file(raw_path: str) -> list[dict]:
    """Lê o arquivo JSON mais recente gerado pela etapa de extração

    Args:
        raw_path (str): Caminho do diretório contendo os arquivos brutos.

    Returns:
        list[dict]: Conteúdo do arquivo JSON carregado (lista de dicionários).

    Raises:
        FileNotFoundError: Se o diretório não existir ou se nenhum arquivo .json for encontrado.
    """
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
    """Valida e transforma a lista de produtos extraídos para o formato de inserção no banco

    Filtra itens que possuem campos obrigatórios ausentes ou nulos e converte
    as chaves do dicionário para padrão snake_case

    Args:
        file_data (list[dict]): Lista de dicionários contendo os dados dos produtos.

    Returns:
        tuple[list[dict], int]: uma tupla contendo:
            - A lista de produtos válidos e formatados
            - A quantidade de produtos descartados devido a campos ausentes
    """
    required_fields = ("id", "title", "price", "discountPercentage", "rating")
    discarted_count = 0
    valid_products = []
    for item in file_data:
        if any(item.get(field) is None for field in required_fields):
            product_id = item.get("id", "Desconhecido")
            logging.warning(f"Campos obrigatórios ausentes no produto ID: {product_id}")
            discarted_count += 1
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

    return valid_products, discarted_count

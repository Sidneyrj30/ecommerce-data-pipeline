import requests
import json
from datetime import datetime
from config import API_URL, RAW_DATA_PATH

try:
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()

    today = datetime.now().strftime("%Y%m%d_%H%M%S")

    with open(f"{RAW_DATA_PATH}/{today}.json", "w") as file:
        json.dump(response.json(), file)

except requests.HTTPError as error:
    print(f"Error status: {error}")

except requests.exceptions.ConnectionError:
    print("Erro de conexão")

except requests.exceptions.Timeout:
    print("Timeout ao consultar a API.")
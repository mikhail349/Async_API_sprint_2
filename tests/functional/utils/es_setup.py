import json
import os

from tests.functional.utils.es_client import get_elastic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def create_index():
    """Метод для создания индексов в elastic search."""
    es = get_elastic()
    for index in ["movies", "persons", "genres"]:
        with open(f"{BASE_DIR}/schema/{index}.json") as f:
            schema = json.load(f)
        es.indices.create(index=index, ignore=400, body=schema)


if __name__ == "__main__":
    create_index()

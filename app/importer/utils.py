from datetime import datetime
import json
from typing import Iterable

from app.baskets.dao import BasketDAO
from app.candles.dao import CandleDAO


TABLE_MODEL_MAP = {
    "candles": CandleDAO,
    "baskets": BasketDAO,
}


def convert_csv_to_postgres_format(csv_iterable: Iterable):
    try:
        data = []
        for row in csv_iterable:
            for k, v in row.items():
                if v.isdigit():
                    row[k] = int(v)
                elif k == "services":
                    row[k] = json.loads(v.replace("'", '"'))
                elif "date" in k:
                    row[k] = datetime.strptime(v, "%Y-%m-%d")
            data.append(row)
        return data
    except Exception:
        pass
from datetime import datetime
from enum import Enum


class Quarter(Enum):
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4


async def get_quarter() -> Quarter:
    current_minute = datetime.now().minute
    if 0 <= current_minute < 15:
        return Quarter.Q1
    elif 15 <= current_minute < 30:
        return Quarter.Q2
    elif 30 <= current_minute < 45:
        return Quarter.Q3
    else:
        return Quarter.Q4

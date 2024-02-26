import datetime
import os
from typing import List, Union

from pydantic import BaseModel
from candfans_client.client import CandFansClient


def collect_sales(email: str, password: str):
    client = CandFansClient(email=email, password=password)
    user_mine = client.get_user_mine()
    mine = user_mine.users[0]
    timeline_month = client.get_timeline_month(user_id=mine.id)

    for timeline in timeline_month:
        month_str = datetime.datetime.strptime(
            timeline.column_name, '%Y年%m月'
        ).strftime('%Y-%m')
        print(f'START collect sales Stats for [{month_str}]')
        base_path = f'./collected_json/{month_str}'
        os.makedirs(base_path, exist_ok=True)
        histories = client.get_sales_history(month_str)
        _dump_json_file(histories, f'{base_path}/histories.json')
        sales = client.get_sales(month_str)
        _dump_json_file(sales, f'{base_path}/sales.json')
        purchase = client.get_sales_purchase_post(month_str)
        _dump_json_file(purchase, f'{base_path}/purchase.json')
        subscribe = client.get_sales_subscribe(month_str)
        _dump_json_file(subscribe, f'{base_path}/subscribe.json')
        chip = client.get_sales_chip(month_str)
        _dump_json_file(chip, f'{base_path}/chip.json')
        backnumber = client.get_sales_backnumber(month_str)
        _dump_json_file(backnumber, f'{base_path}/backnumber.json')
        print(f'END')


def _dump_json_file(data: Union[BaseModel, List[BaseModel]], file_name: str):
    with open(file_name, 'w') as f:
        if isinstance(data, list):
            f.write('[')
            content = ',\n'.join([item.model_dump_json(indent=4) for item in data])
            f.write(content)
            f.write(']')
        else:
            f.write(data.model_dump_json(indent=4))

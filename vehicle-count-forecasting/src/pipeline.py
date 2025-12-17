from .auth import TokenManager
from .api import generate_batch, fetch_with_retry

import os
from datetime import datetime, timedelta, timezone, time as dt_time

def pipeline(config):

    manager = TokenManager(
        server = config['server'],
        token_file = config['token'],
        refresh_file= config['refresh']
    )

    token = manager.get_valid_token()

    headers = {
        "Accept": "application/json",
        "X-Authorization": f"Bearer {token}"
    }

    start_date = datetime.strptime(config['start_collect'], "%m/%d/%Y")
    end_date = datetime.strptime(config['end_collect'], "%m/%d/%Y")

    range_batch = list(
        generate_batch(start_date, end_date, batch=config['batch'])
    )

    fetch_with_retry(
        url=config['api'],
        header=headers,
        base_params=config['base_params'],
        key_list=config['key_list'],
        output_dir=config['output_dir'],
        range_batch=range_batch,
        start_batch=config['start_batch'],
        max_retry=config['max_retry'],
        timeout=config['timeout']        
    )
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import time
import requests
import json

# ----------------------
# Generate Date Ranges
# ----------------------

def generate_batch(start_date, end_date, batch=2):
    ranges = []
    current_start = start_date

    while current_start <= end_date:
        current_end = min(
            current_start + relativedelta(months=1) - timedelta(days=1),
            end_date
        )

        ranges.append((
            current_start.strftime("%m/%d/%Y"),
            current_end.strftime("%m/%d/%Y")
        ))

        current_start += relativedelta(months=1)

    for i in range(0, len(ranges), batch):
        yield ranges[i:i + batch]

# ------------
# Fetch Data
# ------------

def _convert_date_to_ts(date):
    return int(datetime.strptime(date, "%m/%d/%Y").timestamp() * 1000)

def fetch_with_retry(
        url,
        header,
        base_params,
        key_list,
        output_dir,
        range_batch,
        *,
        start_batch=1,
        max_retry=3,
        timeout=30
):
    for batch_to_run in range(start_batch, len(range_batch) + 1):

        current_batch = range_batch[batch_to_run -1]
        all_data = {}

        print(f'Running batch {batch_to_run} with {len(current_batch)} parts')

        for i, (start_date_str,  end_date_str) in enumerate(current_batch, 1):
            print(f'Fetching data for range : {start_date_str} to {end_date_str}')
        
            for key in key_list:
                params = {
                    **base_params,
                    "keys":key,
                    "startTs": _convert_date_to_ts(start_date_str),
                    "endTs": _convert_date_to_ts(end_date_str)
                }
                range_data = None

                for attempt in range(1, max_retry + 1):
                    try:
                        response = requests.get(url, headers=header, params=params, timeout=timeout)

                        if response.status_code == 200:
                            range_data = response.json()
                            break

                        print(
                            f'Attempt{attempt}/{max_retry} failed'
                            f'({response.status_code}): {response.text}' 
                        )

                    except requests.exceptions.RequestException as e:
                        print(f"Attempt {attempt}/{max_retry} exception: {e}")
                        
                    time.sleep(attempt * 2)

                if not range_data:
                    print(
                        f"skipped, key:{key} | "
                        f"range:{start_date_str} to {end_date_str}"
                    )
                continue

            all_data.setdefault(key, []).extend(range_data.get(key, []))
            time.sleep(1)
        
        output_path = output_dir/"data"/"raw"/f"batch_{batch_to_run}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(all_data,f)

        print(f'Batch {batch_to_run} completed')
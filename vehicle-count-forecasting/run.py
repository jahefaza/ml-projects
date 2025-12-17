import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta

from src.pipeline import pipeline

def main():

    base_dir = Path(__file__).resolve().parent
    load_dotenv(base_dir / ".env")

    obj = ['mobil_pribadi','truk','pickup']
    keys = []
    for obj_view in obj:
        keys.append(f'{obj_view}_in2_delta')
        keys.append(f'{obj_view}_out_delta')
        keys.append(f'{obj_view}_turn_delta')

    config = {
        "server": os.getenv("SERVER"),
        "token": str(base_dir/ os.getenv("TOKEN")),
        "refresh": str(base_dir/ os.getenv("REFRESH")),

        "asset_name": "VTC-DEMO-CAM1",
        "asset_id": os.getenv("ASSET_ID"),
        "asset_token": os.getenv("ASSET_TOKEN"),

        "start_collect": "07/05/2025",
        "end_collect": datetime.now().strftime("%m/%d/%Y"),
        
        "batch": 2,
        "start_batch": 1,
        "max_retry": 3,
        "timeout":30,

        "key_list": keys,
        "output_dir": base_dir,
        
        "api": (
            f"{os.getenv('SERVER')}/api/plugins/telemetry/DEVICE/"
            f"{os.getenv('ASSET_ID')}/values/timeseries"
        ),

        "base_params": {
            "interval": 2 * 60 * 60 * 1000,
            "agg": "SUM",
            "useStrictDataTypes": "false"
        },
    }

    pipeline(config)

if __name__ == '__main__':
    main()
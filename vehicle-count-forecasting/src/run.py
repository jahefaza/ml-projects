import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

from pipelines import run_ingest
from services import load_yaml

base_dir = Path(__file__).resolve().parent
project_root = Path(__file__).resolve().parent.parent

def build_ingest_config():
    load_dotenv(base_dir / ".env")
    cfg = load_yaml(base_dir / "config/ingest.yaml")

    keys = []
    for obj_view in cfg['objects']:
        keys.extend([
            f'{obj_view}_in2_delta',
            f'{obj_view}_out_delta',
            f'{obj_view}_turn_delta'
        ])

    return {
        "server": os.getenv("SERVER"),
        "token": str(base_dir/ os.getenv("TOKEN")),
        "refresh": str(base_dir/ os.getenv("REFRESH")),

        "asset_name": cfg['asset']['name'],
        "asset_id": os.getenv("ASSET_ID"),
        "asset_token": os.getenv("ASSET_TOKEN"),

        "start_collect": cfg['collection']['start_date'],
        "end_collect": datetime.now().strftime("%m/%d/%Y"),
        
        "batch": cfg['collection']['batch'],
        "start_batch": cfg['retry']['start_batch'],
        "max_retry": cfg['retry']['max_retry'],
        "timeout": cfg['retry']['timeout'],

        "key_list": keys,
        "output_dir": project_root,
        
        "api": (
            f"{os.getenv('SERVER')}/api/plugins/telemetry/DEVICE/"
            f"{os.getenv('ASSET_ID')}/values/timeseries"
        ),

        "base_params": {
            "interval": cfg['telemetry']['interval_ms'],
            "agg": cfg['telemetry']['aggregation'],
            "useStrictDataTypes": "false"
        },
    }

def main():
    config = build_ingest_config()
    run_ingest(config)
    
if __name__ == '__main__':
    main()

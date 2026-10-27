from dataclasses import dataclass
import pandas as pd

LOAD_COL = 'load_percent'
AMBIENT = 'temp_ambient'

@dataclass(frozen=True)
class MachineConfig:
    regression_features: list[str]
    min_load: float

AIR_COMPRESSOR_1 = MachineConfig(
    regression_features=[
        'load_percent',
        'temp_ambient'
    ],
    min_load=5.0
)

def air_compressor_1(
    df: pd.DataFrame
) -> pd.DataFrame:
    
    data = df.copy()
    req_cols = [LOAD_COL, AMBIENT]
    missing = [col for col in req_cols if col not in data.columns]

    if missing:
        raise ValueError('Missing required telemetry')
    
    if 'press_discharge' in data.columns and 'press_oil' in data.columns:
        data['press_diff'] = data['press_oil'] - data['press_discharge']
    
    data[LOAD_COL] = pd.to_numeric(
        data[LOAD_COL],
        errors='coerce'
    )

    data = data.loc[
        data[LOAD_COL] > AIR_COMPRESSOR_1.min_load
    ].copy()

    return data.dropna(subset=[LOAD_COL, AMBIENT])
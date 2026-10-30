from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class MachineConfig:
    req_features: tuple[str, ...]
    min_load: float = 5.0

AIR_COMPRESSOR_1 = MachineConfig(
    req_features=(
        'load_percent',
        'temp_ambient'
    ),
    min_load=5.0
)

def air_compressor_1(
    df: pd.DataFrame
) -> pd.DataFrame:
    
    data = df.copy()
    req_cols = AIR_COMPRESSOR_1.req_features
    missing = [col for col in req_cols if col not in data.columns]

    if missing:
        raise ValueError('Missing required telemetry')
    
    if 'press_discharge' in data.columns and 'press_oil' in data.columns:
        data['press_diff'] = data['press_oil'] - data['press_discharge']
    
    for col in req_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    
    data = data.loc[data['load_percent'] > AIR_COMPRESSOR_1.min_load].copy()
    if data.empty:
        raise ValueError('No valid air-compressor data')

    return data.dropna(subset=AIR_COMPRESSOR_1.req_features)
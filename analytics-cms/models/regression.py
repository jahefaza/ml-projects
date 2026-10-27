from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd

@dataclass
class RegressionParamConfig:
    col: str
    direction: Literal['upper','lower','both']
    thr_high: float | None = None
    thr_low: float | None = None
    window: str = '1h'
    min_span_frac: float = 0.05
    k_sigma: float | None = None

def design_matrix(
    df: pd.DataFrame,
    feature_cols: list[str]
) -> np.ndarray:
    X = df[feature_cols].to_numpy(dtype=float)

    return np.column_stack([
        np.ones(len(df)),
        X,
    ])

class RegressionModel:
    def __init__(
        self, features_cols: list[str]
    ):
        if not features_cols:
            raise ValueError('At least one regression feature required')
        self.features_cols = list(features_cols)
    
    def fit_baseline(
        self,
        baseline: pd.DataFrame,
        cfg: RegressionParamConfig
    ) -> dict:
        
        req_cols = list(dict.fromkeys(
            [cfg.col] + self.features_cols
        ))
        missing_cols = [col for col in req_cols if col not in baseline.columns]
        if missing_cols:
            raise ValueError('Missing column')
        
        data = baseline.dropna(subset=req_cols).copy().sort_index()
        X = design_matrix(data, self.features_cols)
        y = data[cfg.col].to_numpy(dtype=float)

        coef, *_ = np.linalg.lstsq(X, y, rcond=None)

        residu = pd.Series(y - X @ coef, index=data.index)
        residu_s = residu.rolling(cfg.window).median().dropna()
        return {
            'coef': coef,
            'feature_cols': self.features_cols.copy(),
            'res_lo': float(residu_s.quantile(0.05)),
            'res_hi': float(residu_s.quantile(0.95)),
            'res_std': float(residu.std()),
            'res_std_s': float(residu_s.std())
        }
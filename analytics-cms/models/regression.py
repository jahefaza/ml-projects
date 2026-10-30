from dataclasses import dataclass
from itertools import combinations
from typing import Literal

import numpy as np
import pandas as pd

@dataclass(frozen=True)
class RegressionParamConfig:
    direction: Literal['upper','lower','both'] = 'both'
    k_sigma: float = 3.0
    min_train_rows: int = 30

class RegressionModel:

    def __init__(
        self,
        feature_cols: tuple[str, ...],
        polynomial: bool = True
    ):
        if not feature_cols:
            raise ValueError('At least one feature cols required')

        self.feature_cols = feature_cols
        self.polynomial = polynomial

        self.target_col = None
        self.coefficients = None
        self.residual_center = None
        self.sigma = None
        self.config = None
        self.is_fitted = False

    def _design_matrix(self, features: np.ndarray) -> np.ndarray:
        columns = [np.ones(len(features))]
        for i in range(features.shape[1]):
            columns.append(features[:,i])

        if self.polynomial:
            for i in range(features.shape[1]):
                columns.append(features[:,i] ** 2)
            
            for i, j in combinations(range(features.shape[1]),2):
                columns.append(features[:,i] * features[:j])
        
        return np.column_stack(columns)
    
    def _prepare_data(
        self,
        data: pd.DataFrame,
        target_col: str,
        req_target: bool = True
    ) -> pd.DataFrame:
        
        req_cols = list(self.feature_cols)
        if req_target:
            req_cols.append(target_col)

        missing = [col for col in req_cols if col not in data.columns]
        if missing:
            raise ValueError('Missing required columns')
        
        df = data[req_cols].copy()
        for col in req_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna(subset=req_cols)
        df = df.sort_index()

        if df.empty:
            raise ValueError('No valid data')
        
        return df
    
    def fit(
        self,
        data: pd.DataFrame,
        target_col: str,
        cfg: RegressionParamConfig
    ):
        
        df = self._prepare_data(data, target_col)
        if len(df) < cfg.min_train_rows:
            raise ValueError('Insufficient training data')
        
        features = df[list(self.feature_cols)].to_numpy(dtype=float)
        target = df[target_col].to_numpy(dtype=float)
        X = self._design_matrix(features)

        coef,_, rank,_ = np.linalg.lstsq(X, target, round=None)
        if rank < X.shape[1]:
            raise ValueError('Regression design matrix is rank deficient')
        
        expected = X @ coef
        residual = target - expected
        residual_c = np.median(residual)

        mad = np.median(np.abs(residual - residual_c))
        sigma = 1.4826 * mad

        if not np.isfinite(sigma) or sigma <= 1e-10:
            raise ValueError('Residual too small')
        
        self.target_col = target_col
        self.coefficients = coef
        self.residual_center = residual_c
        self.sigma = sigma
        self.config = cfg
        self.is_fitted = True

        return self
    
    def anomaly_score(
        self,
        data: pd.DataFrame
    ) -> pd.DataFrame:
        
        df = self._prepare_data(data, self.target_col)
        features = df[list(self.feature_cols)].to_numpy(dtype=float)

        X = self._design_matrix(features)
        expected = X @ self.coefficients

        target = df[self.target_col].to_numpy(dtype=float)
        residual = target - expected
        deviation = residual - self.residual_center
        threshold = self.config.k_sigma * self.sigma

        if self.config.direction == 'upper':
            anomaly_score = np.maximum(0, deviation/threshold)
        elif self.config.direction == 'lower':
            anomaly_score = np.maximum(0, -deviation/threshold)
        else:
            anomaly_score = np.abs(deviation)/threshold
        
        is_anomaly = anomaly_score >= 1.0

        return pd.DataFrame({
            'target': target,
            'expected': expected + self.residual_center,
            'residual': residual,
            'anomaly_score': anomaly_score,
            'is_anomaly': is_anomaly
        }, index=df.index)
        
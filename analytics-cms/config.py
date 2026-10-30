from pydantic import BaseModel, Field
from typing import Literal

class AnalyticsConfig(BaseModel):
    telemetry: str = Field(min_length=1)
    training_window: str = Field(min_length=1)
    device_profile: str = Field(min_length=1)

    model_name: Literal[
        'regression',
        'isolation_forest'
    ] = 'regression'

def load_config(payload: dict)-> AnalyticsConfig:
    return AnalyticsConfig.model_validate(payload)
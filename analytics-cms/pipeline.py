from config import AnalyticsConfig

from preprocess import preprocess
from machine_rules.registry import get_machine_rules, get_machine_config
from models.regression import RegressionModel, RegressionParamConfig
from models.factory import create_model

def run_model_pipeline(df, config=AnalyticsConfig) :
    # 1. Clean and preprocess raw telemetry
    data = preprocess(df)
    
    # 2. Machine specific data 
    machine_rules = get_machine_rules(config.device_profile)
    machine_config = get_machine_config(config.device_profile)

    # 3. Apply machine-specific
    data = machine_rules(data)
    req_features = machine_config.req_features
    target_cols = [col for col in config.telemetry if col not in req_features]
    missing = [col for col in target_cols if col not in data.columns]

    if missing:
        raise ValueError('Selected telemetry not found')
    
    # 4. Run the model based on input 
    models = {}
    for target_col in target_cols:
        model = create_model(
            model_name=config.model_name,
            feature_cols=req_features
        )
        model.fit(data=data, target_col=target_col) 
        models[target_col] = model

    return {
        'models': models,
        'feature_cols': req_features,
        'target_cols': target_col,
        'device_profile': config.device_profile,
        'model_name': config.model_name
    }

# 5. Feed the model to the new telemetry
def run_detection_pipeline(df, config, baseline):
    data = preprocess(df)
    machine_rules = get_machine_rules(config.device_profile)
    data = machine_rules(data)
    models = baseline['models']
    
    result = {}
    for target_col, model in models.items():
        result[target_col] = model.anomaly_score(data)
    
    return {
        'result': result,
        'processed_data': data
    }
from preprocess import preprocess
from machine_rules.compressor import air_compressor_1
from machine_rules.registry import get_machine_rules

def run_pipeline(df, config) :
    data = preprocess(df)
    
    machine_rules = get_machine_rules(config.machine_type)
    data = machine_rules(data)

    return data
from machine_rules.compressor import air_compressor_1

machine_rules = {
    'air_compressor_1': air_compressor_1
}

def get_machine_rules(machine_type: str):
    if machine_type not in machine_rules:
        raise ValueError(
            'Please chose supported machine type'
        )
    
    return machine_rules[machine_type]
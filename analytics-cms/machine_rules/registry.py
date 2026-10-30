from machine_rules.compressor import AIR_COMPRESSOR_1, air_compressor_1

# Machine Type
MACHINE_RULES = {
    'air_compressor_1': air_compressor_1
}

MACHINE_CONFIGS = {
    'air_compressor_1': AIR_COMPRESSOR_1
}

DEVICE_PROFILE_MAP = {
    'Air Compressor': 'air_compressor_1'
}

def get_machine_rules(device_profile: str):
    machine_key = DEVICE_PROFILE_MAP.get(device_profile)
    if machine_key is None:
        raise ValueError('Unsupported device profile')
         
    return MACHINE_RULES[machine_key]

def get_machine_config(device_profile: str):
    machine_key = DEVICE_PROFILE_MAP.get(device_profile)
    if machine_key is None:
        raise ValueError('Unsupported device profile')
    
    return MACHINE_CONFIGS[machine_key]
from regression import RegressionModel

def create_model(model_name, feature_cols):
    if model_name == 'regression':
        return RegressionModel(feature_cols=feature_cols)
    else:
        raise ValueError('Unsupported Model')
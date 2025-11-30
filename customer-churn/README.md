# 1. Overview
This projects predicting customer churn (telco dataset) using Machine Learning.
The goal is to identify which customer are likely to leave whether change to another provider or only using Wi-Fi so business can take action before it happens.

# 2. Business Problem
Customer churn impact revenue and SWE (subscription with event) which competitor could take because theh have better package.
This project provides **proactive prediction model** to help reduce churn by focus retention efforts on high-risk users which generate high-revenue  

# 3. Dataset
A Fictional telco company that provided home phone and Internet services
- Total rows: 7043 customer
- Features: 33 variables
- Target: churn (1=churned, 0=stayed)
- Data comes from: latest version "path = kagglehub.dataset_download("yeanzc/telco-customer-churn-ibm-dataset")" 

# 4. Approach & Methods
**Data Processing**
- Handling missing values
- Exploratory Data Analysis (EDA)
- Encoding categorical features
- Feature scaling
- Train and test split

**Models Tried**
- Logistic Regression
- Random Forest
- XGBoost

# 5. Result
- Best Model:
- AUC:
- Recall (churn class):
- Precision:

# 6. Insight

# 7. How to Run

```bash
pip install -requirement.txt
python src/train.py
python src/predict.py
```
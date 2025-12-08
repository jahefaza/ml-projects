# Vehicle Count Forecasting

## 1. Overview
This project predicts the number of vehicles entering and leaving a specific area using **time-series forecasting**.  
The goal is to help operators (e.g., toll gates, parking areas, or traffic management teams) forecast peak hours and allocate the right number of gates/staff efficiently.

---

## 2. Business Problem
Traffic volume is highly variable. Without forecasting, operators either:
- Open too many gates (higher operational cost), or  
- Open too few gates (long queues, bad customer experience)

This project builds a **proactive forecasting model** that predicts vehicle counts for each vehicle type (car, truck, motorcycle) to support:
- capacity planning  
- staffing decisions  
- traffic flow optimization  
- event or holiday preparation  

---

## 3. Dataset
The dataset was generated from **public CCTV feeds**, processed by a custom vehicle-detection model built by my colleague.
- Total rows:  for each vehicle
- Features:  variables
- Target: Forecast
- Data comes from: 

---

## 4. Approach & Methods
### **Data Processing**
- Resampling to 5/15/60-minute intervals  
- Handling missing timestamps  
- Outlier detection (holiday spikes, sudden drops)  
- Time-based feature engineering (hour, day, weekend, holiday flags)  
- Exploratory Data Analysis (trend, seasonality, autocorrelation)

### **Models Tried**
- **Random Forest Regressor** (baseline)  
- **XGBoost Regressor**  
- **ARIMA / SARIMA**  
- **Prophet** (optional)  
- **Naive Seasonal baseline**

### **Model Selection Strategy**
Models evaluated using:
- RMSE  
- MAE  
- MAPE  
- Cross-validation on rolling windows  

## 5. Result
- Best Model:
- AUC:
- Recall (churn class):
- Precision:

---

## 6. Insight

## 7. How to Run

```bash
pip install -requirement.txt
python src/train.py
python src/predict.py
```
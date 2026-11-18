"""
src/model_engine.py
Machine Learning Engine: Random Forest Regressor, Evaluation & Scenario Forecasting.
Preserves 100% of model architecture, hyperparameters, random states, and split logic.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Canonical Feature Vector
FEATURES = [
    "Season_Code", "DayOfWeek", "DayOfMonth", "Month", "UnitPrice",
    "Qty_Lag_1", "Qty_Lag_7", "Qty_Lag_30",
    "Qty_Rolling_Avg_7", "Qty_Rolling_Avg_30"
]

def prepare_model_dataset(daily: pd.DataFrame) -> pd.DataFrame:
    """
    Filters rows where Target_Next_7D exists and fills missing lag values with 0.
    """
    model_df = daily.dropna(subset=["Target_Next_7D"]).copy()
    model_df[FEATURES] = model_df[FEATURES].fillna(0)
    return model_df

def chronological_split(model_df: pd.DataFrame, train_ratio: float = 0.8) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Performs chronological holdout split:
    The last 20% of calendar dates within each season are held out for testing.
    """
    train_parts, test_parts = [], []
    for _, g in model_df.groupby("Season_Type"):
        dates = sorted(g.Date.unique())
        cutoff = dates[max(1, int(len(dates) * train_ratio)) - 1]
        train_parts.append(g[g.Date <= cutoff])
        test_parts.append(g[g.Date > cutoff])
    train = pd.concat(train_parts, ignore_index=True)
    test = pd.concat(test_parts, ignore_index=True)
    return train, test

def train_model(train_df: pd.DataFrame, random_state: int = 42) -> RandomForestRegressor:
    """
    Fits Random Forest Regressor using exact project hyperparameter configuration:
    n_estimators=300, max_depth=10, min_samples_leaf=2, random_state=42, n_jobs=-1.
    """
    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=10,
        min_samples_leaf=2,
        random_state=random_state,
        n_jobs=-1
    )
    model.fit(train_df[FEATURES], train_df["Target_Next_7D"])
    return model

def evaluate_model(model: RandomForestRegressor, test_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Evaluates model on holdout set and returns MAE, RMSE, R² and prediction vector.
    """
    pred_test = model.predict(test_df[FEATURES])
    mae = mean_absolute_error(test_df["Target_Next_7D"], pred_test)
    rmse = mean_squared_error(test_df["Target_Next_7D"], pred_test) ** 0.5
    r2 = r2_score(test_df["Target_Next_7D"], pred_test) if len(test_df) > 1 else float("nan")
    
    test_results = test_df.copy()
    test_results["Predicted_Next_7D"] = pred_test
    test_results["Abs_Error"] = np.abs(test_results["Target_Next_7D"] - pred_test)
    
    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "predictions": test_results
    }

def get_feature_importances(model: RandomForestRegressor) -> pd.DataFrame:
    """
    Returns feature importance rankings for Model Explainability.
    """
    fi = pd.DataFrame({
        "Feature": FEATURES,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False).reset_index(drop=True)
    
    friendly_names = {
        "Qty_Rolling_Avg_7": "7-Day Rolling Avg Quantity",
        "Qty_Lag_7": "Quantity (7 Days Ago)",
        "Qty_Rolling_Avg_30": "30-Day Rolling Avg Quantity",
        "Qty_Lag_1": "Quantity (Yesterday)",
        "UnitPrice": "Unit Price ($)",
        "DayOfWeek": "Day of Week (0-6)",
        "DayOfMonth": "Day of Month (1-31)",
        "Qty_Lag_30": "Quantity (30 Days Ago)",
        "Season_Code": "Season Indicator (Normal/Festive)",
        "Month": "Calendar Month"
    }
    fi["Feature_Label"] = fi["Feature"].map(friendly_names).fillna(fi["Feature"])
    return fi

def generate_scenario_forecast(daily: pd.DataFrame, model: RandomForestRegressor) -> pd.DataFrame:
    """
    Computes scenario predictions for each product:
    - Normal Scenario: Season_Code = 0, Month = 5 (using Normal season's latest features)
    - Festive Scenario: Season_Code = 1, Month = 11 (using Festive season's latest features)
    Computes absolute difference and percentage variation.
    """
    normal_latest = (
        daily[daily.Season_Type == "Normal"]
        .sort_values("Date")
        .groupby("StockCode")
        .tail(1)
        .copy()
    )
    festive_latest = (
        daily[daily.Season_Type == "Festive"]
        .sort_values("Date")
        .groupby("StockCode")
        .tail(1)
        .copy()
    )

    def _predict(frame: pd.DataFrame, season_code: int, month: int) -> pd.DataFrame:
        x = frame.copy()
        x["Season_Code"] = season_code
        x["Month"] = month
        next_dates = x["Date"] + pd.Timedelta(days=1)
        x["DayOfWeek"] = next_dates.dt.dayofweek
        x["DayOfMonth"] = next_dates.dt.day
        x[FEATURES] = x[FEATURES].fillna(0)
        x["Predicted_7D_Quantity"] = np.maximum(0, model.predict(x[FEATURES]))
        cols = ["StockCode", "Description", "Predicted_7D_Quantity"]
        if "Category" in x.columns:
            cols.append("Category")
        return x[cols]

    normal_pred = _predict(normal_latest, 0, 5).rename(
        columns={"Predicted_7D_Quantity": "Normal_Predicted_7D"}
    )
    festive_pred = _predict(festive_latest, 1, 11).rename(
        columns={"Predicted_7D_Quantity": "Festive_Predicted_7D"}
    )

    merge_cols = ["StockCode", "Description"]
    if "Category" in normal_pred.columns and "Category" in festive_pred.columns:
        merge_cols.append("Category")

    comparison = normal_pred.merge(festive_pred, on=merge_cols, how="inner")
    comparison["Difference_Units"] = comparison["Festive_Predicted_7D"] - comparison["Normal_Predicted_7D"]
    comparison["Variation_%"] = np.where(
        comparison["Normal_Predicted_7D"] > 0,
        comparison["Difference_Units"] / comparison["Normal_Predicted_7D"] * 100,
        np.nan
    )
    comparison = comparison.sort_values("Festive_Predicted_7D", ascending=False).reset_index(drop=True)
    return comparison

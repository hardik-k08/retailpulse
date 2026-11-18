"""
src/data_engine.py
Data Ingestion, Cleaning, Feature Engineering & Business Taxonomy Mapping.
Preserves 100% of the original feature calculations and data transformations.
"""

from typing import List, Optional, Tuple, Union
from pathlib import Path
import pandas as pd
import numpy as np

# Dynamically resolve project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "combined_transactions.csv"

# Enterprise Business Categorization for the 10 catalog SKUs
CATEGORY_MAP = {
    "84029G": "Seasonal Warmth",
    "22633": "Seasonal Warmth",
    "84029E": "Seasonal Warmth",
    "22726": "Clocks & Decor",
    "22728": "Clocks & Decor",
    "22727": "Clocks & Decor",
    "21730": "Candles & Lighting",
    "85123A": "Candles & Lighting",
    "71053": "Candles & Lighting",
    "84406B": "Home & Storage"
}

def load_data(data_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Loads raw transaction data with parsed dates and numeric coercion.
    Enriches with enterprise Category mapping while keeping original fields intact.
    Automatically resolves relative paths against the project root directory.
    """
    if data_path is None:
        target_path = DATA_PATH
    else:
        p = Path(data_path)
        target_path = p if p.is_absolute() else (BASE_DIR / p)

    df = pd.read_csv(target_path, parse_dates=["InvoiceDate", "Date"])
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["Total Sales"] = pd.to_numeric(df["Total Sales"], errors="coerce")
    df["StockCode"] = df["StockCode"].astype(str).str.strip()
    df["Category"] = df["StockCode"].map(CATEGORY_MAP).fillna("General Merchandise")
    return df

def prepare_daily(raw: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms raw transaction stream into regular calendar-day product panel.
    Recalculates lag features (1, 7, 30), rolling averages (7, 30), and 7-day target.
    
    EXACT PRESERVATION GUARANTEE:
    - Same grouping keys (Season_Type, StockCode, Description, Date)
    - Reindexed to daily frequency per product-season window
    - Forward-fill/backward-fill for UnitPrice
    - Zero-fill for missing date quantities and revenues
    - Shift and rolling windows computed per season/product partition
    """
    raw_clean = raw.dropna(subset=["InvoiceDate", "StockCode", "Quantity", "UnitPrice"]).copy()
    raw_clean = raw_clean[raw_clean["Quantity"] > 0]
    raw_clean["Date"] = raw_clean["InvoiceDate"].dt.normalize()
    
    # Aggregate to product-season-date level
    d = (
        raw_clean.groupby(["Season_Type", "StockCode", "Description", "Date"], as_index=False)
        .agg(
            Quantity=("Quantity", "sum"),
            UnitPrice=("UnitPrice", "mean"),
            Revenue=("Total Sales", "sum")
        )
    )
    
    blocks = []
    for (season, code, desc), g in d.groupby(["Season_Type", "StockCode", "Description"]):
        idx = pd.date_range(g.Date.min(), g.Date.max(), freq="D")
        z = g.set_index("Date").reindex(idx)
        z.index.name = "Date"
        z["Quantity"] = z["Quantity"].fillna(0)
        z["Revenue"] = z["Revenue"].fillna(0)
        z["UnitPrice"] = z["UnitPrice"].ffill().bfill()
        z["Season_Type"] = season
        z["StockCode"] = code
        z["Description"] = desc
        blocks.append(z.reset_index())
        
    daily = pd.concat(blocks, ignore_index=True).sort_values(["Season_Type", "StockCode", "Date"])
    daily["Season_Code"] = (daily.Season_Type == "Festive").astype(int)
    daily["DayOfWeek"] = daily.Date.dt.dayofweek
    daily["DayOfMonth"] = daily.Date.dt.day
    daily["Month"] = daily.Date.dt.month
    
    # Feature engineering: Lags and rolling stats partitioned by season and product
    grp = daily.groupby(["Season_Type", "StockCode"])
    for lag in [1, 7, 30]:
        daily[f"Qty_Lag_{lag}"] = grp["Quantity"].shift(lag)
        
    for win in [7, 30]:
        daily[f"Qty_Rolling_Avg_{win}"] = daily.groupby(["Season_Type", "StockCode"])["Quantity"].transform(
            lambda s: s.shift(1).rolling(win, min_periods=1).mean()
        )
        
    daily["Target_Next_7D"] = daily.groupby(["Season_Type", "StockCode"])["Quantity"].transform(
        lambda s: s.shift(-1).rolling(7, min_periods=7).sum().shift(-6)
    )
    
    # Map category to daily panel
    daily["Category"] = daily["StockCode"].map(CATEGORY_MAP).fillna("General Merchandise")
    
    return daily

def filter_transactions(
    df: pd.DataFrame,
    date_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None,
    categories: Optional[List[str]] = None,
    products: Optional[List[str]] = None,
    seasons: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Filters transactions dataset dynamically for dashboard slice-and-dice analytics.
    """
    filtered = df.copy()
    if date_range and len(date_range) == 2 and date_range[0] and date_range[1]:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered = filtered[(filtered["Date"] >= start_date) & (filtered["Date"] <= end_date)]
    if categories:
        filtered = filtered[filtered["Category"].isin(categories)]
    if products:
        filtered = filtered[filtered["Description"].isin(products)]
    if seasons:
        filtered = filtered[filtered["Season_Type"].isin(seasons)]
    return filtered

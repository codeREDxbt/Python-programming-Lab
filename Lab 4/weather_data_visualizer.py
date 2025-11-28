"""
Project: Weather Data Visualizer (Single File)
Author: Vinayak [2501730150]
Course: Programming for Problem Solving using Python

Assignment Summary:
- Load a real-world weather CSV (user-provided path)
- Clean and process data (dates, NaNs)
- Compute daily/monthly/yearly statistics with NumPy/Pandas
- Visualize: daily temperature (line), monthly rainfall (bar), humidity vs temperature (scatter)
- Combine at least two plots in one figure
- Export cleaned CSV, PNG plots, and a Markdown report

Usage:
    python weather_data_visualizer.py --csv path/to/weather.csv --outdir ./Lab_4_outputs
If --csv is omitted, you'll be prompted for a path.
"""

from __future__ import annotations
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for saving figures
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -----------------------------------------------------------------------------
# Column inference helpers
# -----------------------------------------------------------------------------
DATE_CANDIDATES = [
    "date", "datetime", "time", "timestamp", "day"
]
TEMP_CANDIDATES = [
    "temperature", "temp", "tavg", "tmean", "avg_temp", "tmax",
]
RAIN_CANDIDATES = [
    "rainfall", "rain", "precip", "precipitation", "prcp"
]
HUMIDITY_CANDIDATES = [
    "humidity", "hum", "rh"
]


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    return df


def _find_first_column(df: pd.DataFrame, candidates) -> Optional[str]:
    for c in candidates:
        if c in df.columns:
            return c
    return None


# -----------------------------------------------------------------------------
# Data loading and cleaning
# -----------------------------------------------------------------------------

def load_and_clean(csv_path: Path) -> Tuple[pd.DataFrame, Dict[str, Optional[str]]]:
    """Load CSV, normalize columns, infer key columns, parse dates, coerce numerics.
    Returns cleaned DataFrame and the mapping for key columns.
    """
    logging.info("Loading CSV: %s", csv_path)
    df = pd.read_csv(csv_path)
    df = _normalize_columns(df)

    # Infer key columns
    date_col = _find_first_column(df, DATE_CANDIDATES)
    temp_col = _find_first_column(df, TEMP_CANDIDATES)
    rain_col = _find_first_column(df, RAIN_CANDIDATES)
    hum_col = _find_first_column(df, HUMIDITY_CANDIDATES)

    if date_col is None:
        # Try auto-detect any datetime-like column by attempting to parse
        for col in df.columns:
            try:
                parsed = pd.to_datetime(df[col], errors="raise")
                date_col = col
                df[col] = parsed
                break
            except Exception:
                continue
    else:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    # Coerce numerics for known columns
    for col in [temp_col, rain_col, hum_col]:
        if col is not None and col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Basic cleaning
    if date_col is None:
        raise ValueError("Could not infer a date/datetime column from the CSV.")

    # Drop rows with invalid dates
    df = df.dropna(subset=[date_col])

    # Sort by date and set index
    df = df.sort_values(by=date_col)
    df = df.set_index(date_col)

    # Fill rainfall NaNs with 0 (common practice) if present
    if rain_col and rain_col in df.columns:
        df[rain_col] = df[rain_col].fillna(0)

    # Remove rows where all of the target numeric columns are NaN (if any exist)
    numeric_cols = [c for c in [temp_col, rain_col, hum_col] if c is not None]
    if numeric_cols:
        df = df.dropna(axis=0, how="all", subset=numeric_cols)

    logging.info(
        "Data loaded. Rows: %d, Columns: %d. Date range: %s to %s",
        len(df), df.shape[1], df.index.min(), df.index.max()
    )

    mapping = {
        "date": date_col,
        "temperature": temp_col,
        "rainfall": rain_col,
        "humidity": hum_col,
    }
    return df, mapping


# -----------------------------------------------------------------------------
# Analysis
# -----------------------------------------------------------------------------

def compute_statistics(df: pd.DataFrame, mapping: Dict[str, Optional[str]]) -> Dict[str, pd.DataFrame]:
    """Compute daily, monthly, and yearly statistics for available metrics."""
    stats = {}
    temp = mapping.get("temperature")
    rain = mapping.get("rainfall")
    hum = mapping.get("humidity")

    def _agg(df_group: pd.Series) -> pd.Series:
        arr = df_group.to_numpy(dtype=float)
        return pd.Series({
            "mean": np.nanmean(arr),
            "min": np.nanmin(arr),
            "max": np.nanmax(arr),
            "std": np.nanstd(arr),
            "count": np.count_nonzero(~np.isnan(arr)),
        })

    # Daily (as-is)
    daily = {}
    if temp and temp in df.columns:
        daily["temperature"] = df[[temp]].groupby(df.index.date).agg(_agg)
    if rain and rain in df.columns:
        daily["rainfall"] = df[[rain]].groupby(df.index.date).agg(_agg)
    if hum and hum in df.columns:
        daily["humidity"] = df[[hum]].groupby(df.index.date).agg(_agg)
    if daily:
        stats["daily"] = {k: v for k, v in daily.items()}

    # Monthly
    monthly = {}
    if temp and temp in df.columns:
        monthly["temperature"] = df[temp].resample("M").apply(_agg)
    if rain and rain in df.columns:
        # For rainfall, monthly total is useful; still provide stats
        monthly["rainfall"] = df[rain].resample("M").apply(_agg)
    if hum and hum in df.columns:
        monthly["humidity"] = df[hum].resample("M").apply(_agg)
    if monthly:
        stats["monthly"] = {k: v for k, v in monthly.items()}

    # Yearly
    yearly = {}
    if temp and temp in df.columns:
        yearly["temperature"] = df[temp].resample("Y").apply(_agg)
    if rain and rain in df.columns:
        yearly["rainfall"] = df[rain].resample("Y").apply(_agg)
    if hum and hum in df.columns:
        yearly["humidity"] = df[hum].resample("Y").apply(_agg)
    if yearly:
        stats["yearly"] = {k: v for k, v in yearly.items()}

    return stats


# -----------------------------------------------------------------------------
# Visualization
# -----------------------------------------------------------------------------

def plot_daily_temperature(df: pd.DataFrame, temp_col: Optional[str], outdir: Path) -> Optional[Path]:
    if not temp_col or temp_col not in df.columns:
        logging.warning("Temperature column not found; skipping daily temperature plot.")
        return None
    fig, ax = plt.subplots(figsize=(10, 4))
    df[temp_col].plot(ax=ax, color="tab:red", linewidth=1)
    ax.set_title("Daily Temperature")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature")
    ax.grid(True, alpha=0.3)
    out = outdir / "daily_temperature.png"
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_monthly_rainfall(df: pd.DataFrame, rain_col: Optional[str], outdir: Path) -> Optional[Path]:
    if not rain_col or rain_col not in df.columns:
        logging.warning("Rainfall column not found; skipping monthly rainfall plot.")
        return None
    monthly = df[rain_col].resample("M").sum(min_count=1)
    fig, ax = plt.subplots(figsize=(10, 4))
    monthly.plot(kind="bar", ax=ax, color="tab:blue")
    ax.set_title("Monthly Rainfall Totals")
    ax.set_xlabel("Month")
    ax.set_ylabel("Rainfall (Total)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.autofmt_xdate(rotation=45)
    out = outdir / "monthly_rainfall.png"
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_humidity_vs_temperature(df: pd.DataFrame, hum_col: Optional[str], temp_col: Optional[str], outdir: Path) -> Optional[Path]:
    if not hum_col or hum_col not in df.columns or not temp_col or temp_col not in df.columns:
        logging.warning("Humidity or Temperature column not found; skipping scatter plot.")
        return None
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(df[temp_col], df[hum_col], alpha=0.5, c=df[temp_col], cmap="coolwarm", edgecolors="none")
    ax.set_title("Humidity vs Temperature")
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Humidity")
    ax.grid(True, alpha=0.3)
    out = outdir / "humidity_vs_temperature.png"
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_combo(df: pd.DataFrame, temp_col: Optional[str], rain_col: Optional[str], outdir: Path) -> Optional[Path]:
    if not temp_col or temp_col not in df.columns or not rain_col or rain_col not in df.columns:
        logging.warning("Temperature or Rainfall column not found; skipping combo figure.")
        return None
    monthly_rain = df[rain_col].resample("M").sum(min_count=1)
    monthly_temp = df[temp_col].resample("M").mean()

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    monthly_temp.plot(ax=axes[0], color="tab:red")
    axes[0].set_title("Monthly Average Temperature")
    axes[0].set_ylabel("Temperature")
    axes[0].grid(True, alpha=0.3)

    monthly_rain.plot(kind="bar", ax=axes[1], color="tab:blue")
    axes[1].set_title("Monthly Rainfall Totals")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Rainfall (Total)")
    axes[1].grid(True, axis="y", alpha=0.3)

    fig.autofmt_xdate(rotation=45)
    out = outdir / "combo_temp_rain.png"
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


# -----------------------------------------------------------------------------
# Exporting
# -----------------------------------------------------------------------------

def export_cleaned_csv(df: pd.DataFrame, outdir: Path) -> Path:
    out = outdir / "cleaned_weather.csv"
    df.to_csv(out)
    return out


def write_report(df: pd.DataFrame, mapping: Dict[str, Optional[str]], outputs: Dict[str, Optional[Path]], outdir: Path) -> Path:
    lines = []
    lines.append("# Weather Data Visualizer Report")
    lines.append("")
    lines.append("Author: Vinayak [2501730150]")
    lines.append("")
    lines.append("## Dataset Overview")
    lines.append(f"Rows: {len(df)} | Columns: {df.shape[1]}")
    lines.append(f"Date Range: {df.index.min()} to {df.index.max()}")
    lines.append("")

    t = mapping.get("temperature")
    r = mapping.get("rainfall")
    h = mapping.get("humidity")

    if t and t in df.columns:
        lines.append("### Temperature Summary")
        lines.append(f"Mean: {df[t].mean():.2f}, Min: {df[t].min():.2f}, Max: {df[t].max():.2f}, Std: {df[t].std():.2f}")
        lines.append("")
    else:
        lines.append("### Temperature Summary\nNot available in this dataset.")
        lines.append("")

    if r and r in df.columns:
        lines.append("### Rainfall Summary")
        lines.append(f"Total: {df[r].sum():.2f}, Mean: {df[r].mean():.2f}")
        lines.append("")
    else:
        lines.append("### Rainfall Summary\nNot available in this dataset.")
        lines.append("")

    if h and h in df.columns:
        lines.append("### Humidity Summary")
        lines.append(f"Mean: {df[h].mean():.2f}, Min: {df[h].min():.2f}, Max: {df[h].max():.2f}")
        lines.append("")
    else:
        lines.append("### Humidity Summary\nNot available in this dataset.")
        lines.append("")

    lines.append("## Visualizations")
    for label, path in outputs.items():
        if path is not None:
            lines.append(f"- {label}: {path.name}")
    lines.append("")

    lines.append("## Interpretation & Insights (Example)")
    lines.append("- Identify periods of high temperature variability using the line plot.")
    lines.append("- Observe wet months from the rainfall bar chart; check seasonal patterns.")
    lines.append("- Explore correlation between humidity and temperature in the scatter plot.")
    lines.append("")

    out = outdir / "weather_report.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Weather Data Visualizer")
    p.add_argument("--csv", type=str, help="Path to the input weather CSV")
    p.add_argument("--outdir", type=str, default=str(Path(__file__).parent), help="Output directory for files")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    csv_path = args.csv
    if not csv_path:
        csv_path = input("Enter path to weather CSV: ").strip().strip('"')
    csv_file = Path(csv_path).expanduser().resolve()

    if not csv_file.exists():
        logging.error("CSV file does not exist: %s", csv_file)
        return 2

    try:
        df, mapping = load_and_clean(csv_file)
    except Exception as e:
        logging.error("Failed to load/clean data: %s", e)
        return 3

    # Compute stats (not saved but could be extended to CSV)
    stats = compute_statistics(df, mapping)
    logging.info("Computed statistics sections: %s", ", ".join(stats.keys()) or "none")

    # Visualizations
    outputs: Dict[str, Optional[Path]] = {}
    outputs["Daily Temperature"] = plot_daily_temperature(df, mapping.get("temperature"), outdir)
    outputs["Monthly Rainfall"] = plot_monthly_rainfall(df, mapping.get("rainfall"), outdir)
    outputs["Humidity vs Temperature"] = plot_humidity_vs_temperature(df, mapping.get("humidity"), mapping.get("temperature"), outdir)
    outputs["Combo Figure (Temp + Rain)"] = plot_combo(df, mapping.get("temperature"), mapping.get("rainfall"), outdir)

    # Exports
    cleaned_csv = export_cleaned_csv(df, outdir)
    report = write_report(df, mapping, outputs, outdir)

    logging.info("Saved cleaned CSV: %s", cleaned_csv)
    logging.info("Saved report: %s", report)
    for label, path in outputs.items():
        if path is not None:
            logging.info("Saved %s: %s", label, path)

    print("\nAnalysis complete. Outputs saved to:")
    print(f"- {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

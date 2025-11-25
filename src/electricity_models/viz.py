 
import polars as pl
import matplotlib.pyplot as plt
from pathlib import Path

def plot_spot(df: pl.DataFrame, save_path: str|None=None):
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df["date"], df["spot"], color="steelblue", lw=1)
    ax.set_title("Spot electricity price")
    ax.set_xlabel("Date"); ax.set_ylabel("Price")
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight")
    return fig, ax

def plot_deseasonalized(df: pl.DataFrame, save_path: str|None=None):
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df["date"], (df["log_spot"] - df["s_t"]), color="darkorange", lw=1)
    ax.set_title("Deseasonalized log spot")
    ax.set_xlabel("Date"); ax.set_ylabel("Log price (minus seasonality)")
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight")
    return fig, ax

def plot_forward_fit(df: pl.DataFrame, forward_col: str, model_col: str, save_path: str|None=None):
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df["date"], df[forward_col], color="black", lw=1, label="Observed")
    ax.plot(df["date"], df[model_col], color="crimson", lw=1, label="Model")
    ax.set_title(f"Forward fit: {forward_col}")
    ax.legend()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight")
    return fig, ax

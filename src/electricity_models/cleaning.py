import polars as pl

def clip_outliers(df: pl.DataFrame, col: str, p_low: float=0.01, p_high: float=0.99) -> pl.DataFrame:
    q = df.select([
        pl.col(col).quantile(p_low).alias("q_low"),
        pl.col(col).quantile(p_high).alias("q_high")
    ]).to_dicts()[0]
    return df.with_columns(
        pl.when(pl.col(col) < q["q_low"]).then(q["q_low"])
          .when(pl.col(col) > q["q_high"]).then(q["q_high"])
          .otherwise(pl.col(col)).alias(col)
    )

def add_log_spot(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(pl.col("spot").log().alias("log_spot"))

def add_returns(df: pl.DataFrame, col: str) -> pl.DataFrame:
    return df.with_columns(
        pl.col(col).diff().alias(f"{col}_diff"),
        (pl.col(col) - pl.col(col).shift(1)).alias(f"{col}_ret")
    )

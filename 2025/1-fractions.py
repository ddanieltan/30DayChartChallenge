# %%
import polars as pl
from plotnine import *

git_pushes = pl.read_csv("../data/github/git_pushes.csv")
git_pushes

# %%
git_pushes.describe()


# %%
# First get your original sorted DataFrame
df = (
    git_pushes.filter(pl.col("year") == 2024)
    .group_by("iso2_code")
    .agg(pl.sum("git_pushes"))
    .with_columns(
        percentage=pl.col("git_pushes") / pl.sum("git_pushes"),
        blocks=(pl.col("git_pushes") / pl.sum("git_pushes") * 100)
        .round()
        .cast(pl.Int32),
    )
    .sort("git_pushes", descending=True)
)

# Get the top 5 rows
top5 = df.head(5)

# Get all other rows, sum them, and create a single "Others" row
others = df.slice(5).select(
    pl.lit("Others").alias("iso2_code"), pl.sum("git_pushes").alias("git_pushes")
)

# Calculate the percentage and blocks for the "Others" row
others = others.with_columns(
    percentage=pl.col("git_pushes") / df["git_pushes"].sum(),
    blocks=(pl.col("git_pushes") / df["git_pushes"].sum() * 100).round().cast(pl.Int32),
)

# Combine the top 5 with the "Others" row
result = pl.concat([top5, others])

# %%

# %%
import numpy as np
import polars as pl
from plotnine import *


git_pushes = pl.read_csv("../data/github/git_pushes.csv")
git_pushes

# %%
git_pushes.describe()

# %%
df = (
    git_pushes.group_by("iso2_code")
    .agg(pl.sum("git_pushes"))
    .with_columns(
        percentage=pl.col("git_pushes") / pl.sum("git_pushes"),
        blocks=(pl.col("git_pushes") / pl.sum("git_pushes") * 100)
        .round()
        .cast(pl.Int32),
    )
    .sort("git_pushes", descending=True)
)

# Focus on top 5 countries and squash rest into Others
top5 = df.head(10)

others = df.slice(10).select(
    pl.lit("Others").alias("iso2_code"), pl.sum("git_pushes").alias("git_pushes")
)

others = others.with_columns(
    percentage=pl.col("git_pushes") / df["git_pushes"].sum(),
    blocks=(pl.col("git_pushes") / df["git_pushes"].sum() * 100).round().cast(pl.Int32),
)

# Combine the top 5 with the "Others" row
result = pl.concat([top5, others])

# Manual workaround rounding not equal to total of 100
result[10, "blocks"] += 1
result


# %%
x = 10
y = 10

Xlin = np.linspace(0, 5, x)
Ylin = np.linspace(0, 5, y)
X, Y = np.meshgrid(Xlin, Ylin)


status = []
for country, blocks in result.select("iso2_code", "blocks").iter_rows():
    status += blocks * [country]

df = pl.DataFrame({"x": X.flatten(), "y": Y.flatten(), "Status": status})

p = ggplot(df, aes(x="x", y="y")) + geom_tile(
    aes(fill="Status"), width=0.8, height=0.8, color="white", size=0.5
)

p.show()

# %%
df
# %%

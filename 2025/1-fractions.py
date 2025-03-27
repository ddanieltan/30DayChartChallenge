# %%
import numpy as np
import polars as pl
from pywaffle import Waffle
import matplotlib.pyplot as plt
from plotnine import *

# %%
git_lang = pl.read_csv("./data/github/languages.csv")
gl = (
    git_lang.filter(pl.col("iso2_code") == "SG")
    .group_by("language")
    .agg(pl.sum("num_pushers").alias("git_pushes"))
    .sort("git_pushes", descending=True)
)

n = 5
top = gl.head(n)
others = gl.slice(n).select(
    pl.lit("Others").alias("language"), pl.sum("git_pushes").alias("git_pushes")
)

df = pl.concat([top, others])
df = df.with_columns(
    percentage=pl.col("git_pushes") / df["git_pushes"].sum(),
    blocks=(pl.col("git_pushes") / df["git_pushes"].sum() * 100).round().cast(pl.Int32),
)


fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=20,  # Either rows or columns could be omitted
    values=df.select("blocks").to_series(),  # Pass a list of integers to values
    title={
        "label": "Top git pushes to Github by Programming Language",
        "loc": "left",
        "fontdict": {"fontsize": 15},
    },
    colors=["#004d00", "#00b300", "#419873", "#008000", "#52bf90", "#808080"],
)

fig.show()

# %%
git_pushes = pl.read_csv("./data/github/git_pushes.csv")
(
    git_pushes.group_by("iso2_code")
    .agg(pl.sum("git_pushes"))
    .filter(pl.col("iso2_code").is_in(["US", "SG"]))
)
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

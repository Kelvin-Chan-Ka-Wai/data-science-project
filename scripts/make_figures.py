"""Recreate the three interactive figures of the project as standalone HTML pages.

Run:  python scripts/make_figures.py
Output: figures/html/*.html  (open in any browser)
The PNG versions committed in figures/ were exported from exactly these plots.
"""
import os

import numpy as np
import pandas as pd
from bokeh.io import output_file, save
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "figures", "html")


def population():
    df = pd.read_csv(os.path.join(DATA, "world_population.csv"), index_col=0)
    years = [y for y in df.columns if not y[0].isalpha()]
    de = [df.loc["Germany", y] for y in years]
    ch = [df.loc["Switzerland", y] for y in years]
    plot = figure(title="Population density, Germany vs Switzerland (1961-2015)",
                  x_axis_label="Year", y_axis_label="People per km2",
                  width=900, height=460)
    plot.line([int(y) for y in years], de, line_width=2.5, color="#2678b2",
              legend_label="Germany")
    plot.line([int(y) for y in years], ch, line_width=2.5, color="#f2a33c",
              legend_label="Switzerland")
    plot.legend.location = "top_left"
    output_file(os.path.join(OUT, "population_density.html"))
    save(plot)


def car_prices():
    df = pd.read_csv(os.path.join(DATA, "automobiles.csv"))
    grouped = df.groupby("make", as_index=False).mean(numeric_only=True)
    mapper = LinearColorMapper(palette="Magma256", low=grouped["price"].min(),
                               high=grouped["price"].max())
    source = ColumnDataSource(grouped)
    plot = figure(title="Mean car price by manufacturer (1985 automobile market)",
                  x_axis_label="Manufacturer", y_axis_label="Mean price (USD)",
                  x_range=list(grouped["make"]), width=900, height=460)
    plot.scatter("make", "price", source=source, size=16, marker="circle",
                 color=linear_cmap("price", "Magma256", grouped["price"].min(),
                                   grouped["price"].max()), line_color="white")
    plot.xaxis.major_label_orientation = "vertical"
    plot.add_tools(HoverTool(tooltips=[("Manufacturer", "@make"),
                                       ("Mean price", "@price{0,0}")]))
    output_file(os.path.join(OUT, "car_prices.html"))
    save(plot)


def olympics():
    df = pd.read_csv(os.path.join(DATA, "olympia2016_athletes.csv"))
    countries = (df.groupby("nationality")
                 .agg(athletes=("id", "count"), gold=("gold", "sum"),
                      silver=("silver", "sum"), bronze=("bronze", "sum"))
                 .reset_index())
    countries["medals"] = countries[["gold", "silver", "bronze"]].sum(axis=1)
    source = ColumnDataSource(countries)
    plot = figure(title="Rio 2016: medals vs delegation size",
                  x_axis_label="Number of medals", y_axis_label="Number of athletes",
                  width=900, height=460)
    plot.scatter("medals", "athletes", source=source, size=9, marker="circle",
                 fill_color="#2678b2", line_color="white", alpha=0.85)
    plot.add_tools(HoverTool(tooltips=[("Country", "@nationality"),
                                       ("Athletes", "@athletes"),
                                       ("Medals", "@medals")]))
    output_file(os.path.join(OUT, "olympics.html"))
    save(plot)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    population()
    car_prices()
    olympics()
    print("wrote interactive figures to", OUT)

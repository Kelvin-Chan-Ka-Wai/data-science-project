"""Regenerate the three figures of the project as PNG (for the README) and HTML (interactive).

Run:  python scripts/make_figures.py
Output:
    figures/*.png          static images used by README.md and the portfolio page
    figures/html/*.html    the same figures, interactive

Every figure states its unit on the axis, carries a title that names the comparison, and
annotates the number the finding depends on, so the picture can be read without the prose.

The PNG export needs a browser driver (Bokeh uses Selenium):
    pip install selenium
    # Chrome/Chromium is auto-detected; Selenium Manager fetches a matching driver.
If no driver is available the script fails clearly; use --html-only when intentionally
producing just the interactive HTML.
"""
import os
import sys

import numpy as np
import pandas as pd
from bokeh.io import output_file, save
from bokeh.models import ColumnDataSource, HoverTool, Label, LabelSet, Span
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "figures")
OUT_HTML = os.path.join(OUT, "html")

# One palette/geometry set, so the three figures look like one report.
BLUE = "#1f5fa9"
ORANGE = "#e08a1e"
GREY = "#5b6770"
W, H = 1000, 520


#: set by --html-only; PNG export is skipped rather than attempted and failed
SKIP_PNG = False


def _export_png(plot, name):
    """Write the static PNG; return True on success (or when intentionally skipped)."""
    if SKIP_PNG:
        print("  - skipped %s (--html-only)" % name)
        return True
    try:
        from bokeh.io import export_png
        export_png(plot, filename=os.path.join(OUT, name))
        return True
    except Exception as exc:                       # no driver installed
        print("  ! could not export %s (%s)" % (name, str(exc).splitlines()[0][:110]))
        return False


def _finish(plot, html_name, png_name):
    output_file(os.path.join(OUT_HTML, html_name), title=html_name)
    save(plot)
    return _export_png(plot, png_name)


# --------------------------------------------------------------------------- 1. population
def population():
    df = pd.read_csv(os.path.join(DATA, "world_population.csv"), index_col=0)
    years = [y for y in df.columns if not y[0].isalpha()]
    pairs = [(int(y), df.loc["Germany", y], df.loc["Switzerland", y]) for y in years]
    pairs = [(y, de, ch) for y, de, ch in pairs if pd.notna(de) and pd.notna(ch)]
    xs = [p[0] for p in pairs]
    de = [p[1] for p in pairs]
    ch = [p[2] for p in pairs]

    plot = figure(
        title="Population density converged: Germany and Switzerland, 1961-2015",
        x_axis_label="Year",
        y_axis_label="Population density (people per km\u00b2)",
        width=W, height=H, tools="xpan,xwheel_zoom,reset,save",
        toolbar_location="above")
    plot.line(xs, de, line_width=2.5, color=BLUE, legend_label="Germany")
    plot.line(xs, ch, line_width=2.5, color=ORANGE, legend_label="Switzerland")
    plot.legend.location = "top_left"
    plot.legend.label_text_font_size = "11pt"

    # mark the two years the finding is computed from
    for year, a, b in ((1961, de[0], ch[0]), (2015, de[-1], ch[-1])):
        plot.segment(x0=year, y0=b, x1=year, y1=a, line_color=GREY,
                     line_width=1.6, line_dash="dashed")
        plot.scatter([year, year], [a, b], size=9, color=[BLUE, ORANGE],
                     line_color="white")

    gap_1961 = de[0] - ch[0]
    gap_2015 = de[-1] - ch[-1]
    plot.add_layout(Label(
        x=1975, y=168,
        text="gap %0.1f \u2192 %0.1f people/km\u00b2 (\u2212%d%%)"
             % (gap_1961, gap_2015, round((1 - gap_2015 / gap_1961) * 100)),
        text_font_size="12pt", text_color=GREY, text_font_style="italic"))
    plot.y_range.start = 120
    return _finish(plot, "population_density.html",
                   "population_density_germany_switzerland.png")


# ------------------------------------------------------------------------------ 2. car prices
def car_prices():
    df = pd.read_csv(os.path.join(DATA, "automobiles.csv"))
    grouped = df.groupby("make", as_index=False).mean(numeric_only=True)
    grouped = grouped.sort_values("price", ascending=False)
    source = ColumnDataSource(grouped)
    low, high = float(grouped["price"].min()), float(grouped["price"].max())
    median = float(df["price"].median())

    plot = figure(
        title="Mean price per manufacturer is skewed 5.8x (1985 US market, 201 cars)",
        x_axis_label="Manufacturer",
        y_axis_label="Mean price (USD, 1985 - not inflation adjusted)",
        x_range=list(grouped["make"]), width=W, height=H,
        tools="xpan,reset,save", toolbar_location="above")
    plot.scatter("make", "price", source=source, size=15, marker="circle",
                 color=linear_cmap("price", "Magma256", low, high),
                 line_color="white", legend_label="Mean price per manufacturer")
    plot.xaxis.major_label_orientation = 1.2
    plot.add_tools(HoverTool(tooltips=[("Manufacturer", "@make"),
                                       ("Mean price", "@price{$0,0}")]))
    # the median car is the honest comparator for a skewed distribution
    plot.add_layout(Span(location=median, dimension="width", line_color=GREY,
                         line_dash="dashed", line_width=1.4))
    plot.add_layout(Label(x=len(grouped) - 1, y=median + 900,
                          text="median car $%s" % format(int(median), ","),
                          text_font_size="11pt", text_color=GREY,
                          text_align="right", text_font_style="italic"))
    plot.y_range.start = 0
    plot.legend.location = "top_right"
    return _finish(plot, "car_prices.html", "car_mean_price_by_make.png")


# -------------------------------------------------------------------------------- 3. olympics
def olympics():
    df = pd.read_csv(os.path.join(DATA, "olympia2016_athletes.csv"))
    countries = (df.groupby("nationality")
                 .agg(athletes=("id", "count"), gold=("gold", "sum"),
                      silver=("silver", "sum"), bronze=("bronze", "sum"))
                 .reset_index())
    countries["medals"] = countries[["gold", "silver", "bronze"]].sum(axis=1)
    r = float(np.corrcoef(countries["athletes"], countries["medals"])[0, 1])

    # The dataset uses IOC three-letter codes, not country names ("JAM", not "Jamaica");
    # matching on the full name silently found nothing and the three named points were never
    # highlighted.
    labels = ["USA", "JAM", "SRB"]
    source = ColumnDataSource(countries)
    plot = figure(
        title="Medals track delegation size at Rio 2016 (Pearson r = %.2f, n = %d countries)"
              % (r, len(countries)),
        x_axis_label="Athletes sent by the country (delegation size)",
        y_axis_label="Total medals won (gold + silver + bronze)",
        width=W, height=H, tools="xpan,xwheel_zoom,reset,save",
        toolbar_location="above")
    plot.scatter("athletes", "medals", source=source, size=9, marker="circle",
                 fill_color=BLUE, line_color="white", alpha=0.8,
                 legend_label="One country")
    plot.add_tools(HoverTool(tooltips=[("Country", "@nationality"),
                                       ("Athletes", "@athletes"),
                                       ("Medals", "@medals")]))
    picked = countries[countries["nationality"].isin(labels)].copy()
    plot.scatter("athletes", "medals", source=ColumnDataSource(picked), size=15,
                 marker="circle", fill_color=ORANGE, line_color="white",
                 legend_label="Named in the findings")
    # label placement per point, so nothing runs off the canvas or over a neighbour
    offsets = {"USA": (-10, 10), "JAM": (12, -4), "SRB": (12, -4)}
    picked["x_off"] = [offsets.get(n, (8, 4))[0] for n in picked["nationality"]]
    picked["y_off"] = [offsets.get(n, (8, 4))[1] for n in picked["nationality"]]
    picked["align"] = ["right" if offsets.get(n, (8, 4))[0] < 0 else "left"
                       for n in picked["nationality"]]
    for name, x_off, y_off, align in zip(picked["nationality"], picked["x_off"],
                                         picked["y_off"], picked["align"]):
        row = picked[picked["nationality"] == name].iloc[0]
        plot.add_layout(Label(x=int(row["athletes"]), y=int(row["medals"]),
                              text=name, x_offset=int(x_off), y_offset=int(y_off),
                              text_font_size="10pt", text_color=GREY,
                              text_align=align))
    plot.x_range.start = -25
    plot.x_range.end = 610
    plot.y_range.start = -10
    plot.legend.location = "top_left"
    return _finish(plot, "olympics.html", "olympics_medals_vs_athletes.png")


if __name__ == "__main__":
    os.makedirs(OUT_HTML, exist_ok=True)
    SKIP_PNG = "--html-only" in sys.argv
    ok = [population(), car_prices(), olympics()]
    print("wrote interactive figures to", OUT_HTML)
    if SKIP_PNG:
        print("PNG figures: skipped (--html-only)")
    else:
        print("PNG figures:", "3/3" if all(ok) else "%d/3" % sum(ok))
    if not all(ok) and not SKIP_PNG:
        raise SystemExit("PNG export failed. Install Chrome/Chromium and a matching "
                         "ChromeDriver, or explicitly pass --html-only.")

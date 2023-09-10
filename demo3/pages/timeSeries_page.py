import panel as pn
from pages.sidebar import selected_stocks

pn.extension("tabulator", design="material", template="material", loading_indicator=True)


# ===============
#  Plot stock prices
timeseries = selected_stocks.hvplot.line(
    "Date",
    group_label="Stock",
    value_label="Stock Price ($)",
    title="Daily Stock Price",
    min_height=300,
    responsive=True,
    grid=True,
    legend="top_left",
).dmap()
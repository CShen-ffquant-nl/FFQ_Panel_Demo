import numpy as np
import pandas as pd
import holoviews as hv
import panel as pn
import hvplot.pandas
from demo2.load import get_stocks
from demo2.logic import compute_frontier,compute_random_allocations,find_best_allocation

pn.extension("tabulator", design="material", template="material", loading_indicator=True)

# ===============
# load data from csv or default data
file_input = pn.widgets.FileInput(sizing_mode="stretch_width")

stocks = hvplot.bind(get_stocks, file_input).interactive()

selector = pn.widgets.MultiSelect(
    name="Select stocks", sizing_mode="stretch_width", options=stocks.columns.to_list()
)

selected_stocks = stocks.pipe(lambda df, cols: df[cols] if cols else df, selector)

# =================
# declare UI components
n_samples = pn.widgets.IntSlider(
    name="Random samples",
    value=10_000,
    start=1000,
    end=20_000,
    step=1000,
    sizing_mode="stretch_width",
)
button = pn.widgets.Button(name="Run Analysis", sizing_mode="stretch_width")
posxy = hv.streams.Tap(x=None, y=None)

text = """
#  Portfolio optimization

This application performs portfolio optimization given a set of stock time series.

To optimize your portfolio:

1. Upload a CSV of the daily stock time series for the stocks you are considering
2. Select the stocks to be included.
3. Run the Analysis
4. Click on the Return/Volatility plot to select the desired risk/reward profile

Upload a CSV containing stock data:
"""

explanation = """
The code for this app was taken from [this excellent introduction to Python for Finance](https://github.com/PrateekKumarSingh/Python/tree/master/Python%20for%20Finance/Python-for-Finance-Repo-master).
To learn some of the background and theory about portfolio optimization see [this notebook](https://github.com/PrateekKumarSingh/Python/blob/master/Python%20for%20Finance/Python-for-Finance-Repo-master/09-Python-Finance-Fundamentals/02-Portfolio-Optimization.ipynb).
"""

sidebar = pn.layout.WidgetBox(
    pn.pane.Markdown(text, margin=(0, 10)),
    file_input,
    selector,
    n_samples,
    explanation,
    max_width=350,
    sizing_mode="stretch_width",
).servable(area="sidebar")

# =================
# plot Portfolio optimization plot

# Set up data pipelines
log_return = np.log(selected_stocks / selected_stocks.shift(1))
random_allocations = log_return.pipe(compute_random_allocations, n_samples)
closest_allocation = log_return.pipe(find_best_allocation, posxy.param.x, posxy.param.y)
efficient_frontier = random_allocations.pipe(compute_frontier)
max_sharpe = random_allocations.pipe(lambda df: df[df.Sharpe == df.Sharpe.max()])

# Generate plots
opts = {"x": "Volatility", "y": "Return", "responsive": True}

allocations_scatter = (
    random_allocations.hvplot.scatter(alpha=0.1, color="Sharpe", cmap="plasma", **opts)
    .dmap()
    .opts(tools=[])
)

frontier_curve = efficient_frontier.hvplot(
    line_dash="dashed", color="green", **opts
).dmap()

max_sharpe_point = max_sharpe.hvplot.scatter(line_color="black", size=50, **opts).dmap()

closest_point = (
    closest_allocation.to_frame()
    .T.hvplot.scatter(color="green", line_color="black", size=50, **opts)
    .dmap()
)

posxy.source = allocations_scatter

summary = pn.pane.Markdown(
    pn.bind(
        lambda p: f"""
    The selected portfolio has a volatility of {p.Volatility:.2f}, a return of {p.Return:.2f}
    and Sharpe ratio of {p.Return/p.Volatility:.2f}.""",
        closest_allocation,
    ),
    width=250,
)

table = pn.widgets.Tabulator(closest_allocation.to_frame().iloc[:-2])

plot = (allocations_scatter * frontier_curve * max_sharpe_point * closest_point).opts(
    min_height=400, show_grid=True
)

pn.Row(plot, pn.Column(summary, table), sizing_mode="stretch_both")


# ==================
# plot Portfolio Performance plot

investment = pn.widgets.Spinner(
    name="Investment Value in $", value=5000, step=1000, start=1000, end=100000
)
year = pn.widgets.DateRangeSlider(
    name="Year",
    value=(stocks.index.min().eval(), stocks.index.max().eval()),
    start=stocks.index.min(),
    end=stocks.index.max(),
)

stocks_between_dates = selected_stocks[year.param.value_start : year.param.value_end]
price_on_start_date = selected_stocks[year.param.value_start :].iloc[0]
allocation = closest_allocation.iloc[:-2] * investment

performance_plot = (
    (stocks_between_dates * allocation / price_on_start_date)
    .sum(axis=1)
    .rename()
    .hvplot.line(
        ylabel="Total Value ($)",
        title="Portfolio performance",
        responsive=True,
        min_height=400,
    )
    .dmap()
)

performance = pn.Column(
    pn.Row(year, investment), performance_plot, sizing_mode="stretch_both"
)

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

# ================
# Log return plots
log_ret_hists = (
    log_return.hvplot.hist(
        min_height=300,
        min_width=400,
        responsive=True,
        bins=100,
        subplots=True,
        group_label="Stock",
    )
    .cols(2)
    .opts(sizing_mode="stretch_both")
    .panel()
)

# ==================
# Overall layout
main_plot = pn.Tabs(
    (
        "Analysis",
        pn.Column(
            pn.Row(plot, pn.Column(summary, table), sizing_mode="stretch_both"),
            performance,
            sizing_mode="stretch_both",
        ),
    ),
    ("Timeseries", timeseries),
    (
        "Log Return",
        pn.Column(
            "## Daily normalized log returns",
            "Width of distribution indicates volatility and center of distribution the mean daily return.",
            log_ret_hists,
            sizing_mode="stretch_both",
        ),
    ),
    sizing_mode="stretch_both",
    min_height=1000,
).servable(title="Portfolio Optimizer")

page=pn.Row(sidebar, main_plot)
#local run:
page.show()
#Azure:
# page.show(port=8000,websocket_origin='ffq-panel-test.azurewebsites.net',address='0.0.0.0')

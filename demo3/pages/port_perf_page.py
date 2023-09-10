import panel as pn
from pages.sidebar import stocks,selected_stocks
from logic.port_opt_logic import closest_allocation

pn.extension("tabulator", design="material", template="material", loading_indicator=True)


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

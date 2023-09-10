import holoviews as hv
import panel as pn
import hvplot.pandas
from data.data import get_stocks

pn.extension(
    "tabulator", design="material", template="material", loading_indicator=True
)

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

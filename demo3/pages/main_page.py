import panel as pn
from pages.sidebar import sidebar
from pages.port_opt_page import plot,summary,table
from pages.port_perf_page import performance
from pages.timeSeries_page import timeseries
from pages.log_ret_hist_page import log_ret_hists

pn.extension("tabulator", design="material", template="material", loading_indicator=True)

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
# page.show(port=8000,websocket_origin='ffq-panel-test.azurewebsites.net,paneltest.ffquants.nl',address='0.0.0.0')

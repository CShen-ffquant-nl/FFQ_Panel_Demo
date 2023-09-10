import panel as pn
from logic.port_opt_logic import log_return

pn.extension("tabulator", design="material", template="material", loading_indicator=True)

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

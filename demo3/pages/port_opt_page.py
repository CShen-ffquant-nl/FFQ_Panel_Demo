import panel as pn
from pages.sidebar import posxy
from logic.port_opt_logic import max_sharpe,random_allocations,efficient_frontier,closest_allocation

pn.extension("tabulator", design="material", template="material", loading_indicator=True)

# # =================
# # plot Portfolio optimization plot

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



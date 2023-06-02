'''
https://panel.holoviz.org/getting_started/build_app.html
with small modification to run in VS code
'''


import panel as pn
import pandas as pd
import numpy as np
import hvplot.pandas #TODO: if remove this one will fail. 

def view_hvplot(avg, highlight):
    # this function display a plot
    return avg.hvplot(height=300, width=400, legend=False) * highlight.hvplot.scatter(
        color="orange", padding=0.1, legend=False
    )

def find_outliers(data,variable="Temperature", window=30, sigma=10, view_fn=view_hvplot):
    
    # some logic here
    avg = data[variable].rolling(window=window).mean()
    residual = data[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = np.abs(residual) > std * sigma

    #call view_hvplot to display avg line, highlight avg[outliers]
    return view_fn(avg, avg[outliers])

if __name__=="__main__":

    #init template    
    pn.extension(design='material')

    #load data
    csv_file = ("./demo_data/datatest.txt")
    data = pd.read_csv(csv_file, parse_dates=["date"], index_col="date")

    # create widget : 
    # Select widget allows to select from pull down list 
    variable_widget = pn.widgets.Select(name="variable", value="Temperature", options=list(data.columns))
    # window widget allows to slide to choose a value for window
    window_widget = pn.widgets.IntSlider(name="window", value=30, start=1, end=60)
    # sigma widget allows to slide to choose a value for sigma
    sigma_widget = pn.widgets.IntSlider(name="sigma", value=10, start=0, end=20)

    #feed result from widget to function find_outlier() (and create a plot by find_outlier)
    bound_plot_1 = pn.bind(find_outliers,data=data, variable=variable_widget, window=window_widget, sigma=sigma_widget)

    #create a page that covers 3 widget and 1 plot in a column style. servable() allows it to display
    #https://panel.holoviz.org/how_to/editor/editor.html
    first_app=pn.Column(variable_widget, window_widget, sigma_widget, bound_plot_1)

    # with this line, run the demo.py will start a server
    first_app.show(port=5007)



# Pandas for data management
import pandas as pd
import numpy as np

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script
from scripts.hist import histogram_tab

# Read data into dataframes
#flights = pd.read_csv(join(dirname(__file__), 'data', 'flights.csv'), index_col=0).dropna()

file = 'http://mlr.cs.umass.edu/ml/machine-learning-databases/adult/adult.data'

census = pd.read_csv(file, sep=", ", header=None, index_col=False,
                  names=['age', 'workclass', 'fnlwgt', 'education', 'education-num',
                         'marital-status', 'occupation', 'relationship', 'race',
                         'sex', 'capital-gain', 'capital-loss', 'hours-per-week',
                         'native-country'])

census = census.replace('?', np.NaN)
census = census.dropna()

# Formatted Flight Delay Data for map
#map_data = pd.read_csv(join(dirname(__file__), 'data', 'flights_map.csv'),
#                            header=[0,1], index_col=0)

# Create each of the tabs
tab1 = histogram_tab(census)
#tab2 = density_tab(flights)
#tab3 = table_tab(flights)
#tab4 = map_tab(map_data, states)
#tab5 = route_tab(flights)

# Put all the tabs into one application
#tabs = Tabs(tabs = [tab1, tab2, tab3, tab4, tab5])
tabs = Tabs(tabs = [tab1])

# Put the tabs in the current document for display
curdoc().add_root(tabs)



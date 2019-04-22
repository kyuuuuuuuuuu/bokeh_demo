# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 21:00:37 2019

@author: Jin
"""
import numpy as np
import pandas as pd

#from bokeh.io import show, output_notebook, push_notebook
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
#from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

#from bokeh.application.handlers import FunctionHandler
#from bokeh.application import Application

from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
								  Tabs, CheckboxButtonGroup, 
								  TableColumn, DataTable, Select)

def histogram_tab(census):
  
  def make_dataset(work_list, range_start = 0, range_end = 100, bin_width = 5):
    
    # check start and end
    assert range_start < range_end, "Start must be less than end!"

    by_class = pd.DataFrame(columns=['proportion', 'left', 'right', 
                                         'f_proportion', 'f_interval',
                                         'workclass', 'color'])
    range_extent = range_end - range_start

    # Iterate through all the classes
    for i, work in enumerate(work_list):

      # Subset to the carrier
      subset = census[census['workclass'] == work]

      # Create a histogram with specified bins and range
      hour_hist, edges = np.histogram(subset['hours-per-week'], 
                                     bins = int(range_extent / bin_width), 
                                     range = [range_start, range_end])

      # Divide the counts by the total to get a proportion and create df
      hour_df = pd.DataFrame({'proportion': hour_hist / np.sum(hour_hist),
                              'left': edges[:-1], 
                              'right': edges[1:] })

      # Format the proportion 
      hour_df['f_proportion'] = ['%0.5f' % proportion for proportion in hour_df['proportion']]

      # Format the interval
      hour_df['f_interval'] = ['%d to %d hrs' % (left, right) for left, right in zip(hour_df['left'], hour_df['right'])]

      # Assign the carrier for labels
      hour_df['workclass'] = work

      # Color each carrier differently
      hour_df['color'] = Category20_16[i]

      # Add to the overall dataframe
      by_class = by_class.append(hour_df)

    # Overall dataframe
    by_class = by_class.sort_values(['workclass', 'left'])

    return ColumnDataSource(by_class)
  
  
  def style(p):
    
    # Title 
    p.title.align = 'center'
    p.title.text_font_size = '20pt'
    p.title.text_font = 'serif'

    # Axis titles
    p.xaxis.axis_label_text_font_size = '14pt'
    p.xaxis.axis_label_text_font_style = 'bold'
    p.yaxis.axis_label_text_font_size = '14pt'
    p.yaxis.axis_label_text_font_style = 'bold'

    # Tick labels
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font_size = '12pt'

    return p

  def make_plot(src):
    
    # Blank plot with correct labels
    p = figure(plot_width = 700, plot_height = 700, 
            title = 'Histogram of Weekly Hours by Work Class',
            x_axis_label = 'Weekly Work (hr)', y_axis_label = 'Proportion')

    # Quad glyphs to create a histogram
    p.quad(source = src, bottom = 0, top = 'proportion', left = 'left', right = 'right',
         color = 'color', fill_alpha = 0.7, hover_fill_color = 'color', legend = 'workclass',
         hover_fill_alpha = 1.0, line_color = 'black')

    # Hover tool with vline mode
    hover = HoverTool(tooltips=[('Work Class', '@workclass'), 
                              ('Weekly Work', '@f_interval'),
                              ('Proportion', '@f_proportion')],
                      mode='vline')

    p.add_tools(hover)

    # Styling
    p = style(p)

    return p
  
  # Update function takes three default parameters
  def update(attr, old, new):
    
    # Get the list of carriers for the graph
    class_to_plot = [class_selection.labels[i] for i in class_selection.active]

    # Make a new dataset based on the selected carriers and the 
    # make_dataset function defined earlier
    new_src = make_dataset(class_to_plot,
                           range_start = range_select.value[0],
							    range_end = range_select.value[1],
							    bin_width = binwidth_select.value)

    # Convert dataframe to column data source
#    new_src = ColumnDataSource(new_src)

    # Update the source used the quad glpyhs
    src.data.update(new_src.data)

  # Available workclass list
  available_workclass = list(census['workclass'].unique())
  available_workclass.sort()

  # controls
  class_selection = CheckboxGroup(labels=available_workclass, active = [0, 1, 2])
  class_selection.on_change('active', update)

  binwidth_select = Slider(start = 0, end = 30, 
                     step = 5, value = 5,
                     title = 'Weekly Work (hr)')
  binwidth_select.on_change('value', update)
 
  range_select = RangeSlider(start = 1, end = 99, value = (1, 99),
                           step = 1, title = 'Work Range (hr)')
  range_select.on_change('value', update)

  initial_class = [class_selection.labels[i] for i in class_selection.active]

  src = make_dataset(initial_class,
                    range_start = 5,
                    range_end = 95,
                    bin_width = 5)
    
  p = make_plot(src)
  
  
  # Put controls in a single element
  controls = WidgetBox(class_selection, binwidth_select, range_select)
  layout = row(controls, p)
  
  # Make a tab with the layout 
  tab = Panel(child=layout, title = 'Histogram')

  return tab


#  doc.add_root(layout)
    
# Set up an application
#handler = FunctionHandler(modify_doc)
#app = Application(handler)
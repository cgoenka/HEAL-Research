import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from UliEngineering.EngineerIO import format_value
import csv

# Helper functions

# helper function for formatting axis units
def axes_units(x_unit: str, y_unit: str, ax = None):

    def format_x(value, pos=None):
        return format_value(value, x_unit)
    def format_y(value, pos=None):
        return format_value(value, y_unit)

    # Set our formatters as X and Y axis formatters
    if ax:
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(format_x))
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(format_y))
    else:
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(format_x))
        plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(format_y))

# one-liner for simplifying axes code
def axes_labels(x_label: str, x_unit: str, y_label: str, y_unit: str, title = None, ax = None):
    if ax:
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        axes_units(x_unit, y_unit, ax)
        if title:
            ax.set_title(title)
    else:
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        axes_units(x_unit, y_unit)
        if title:
            plt.title(title)

# helper function for simplifying column names
def strip_labels(label: str):
    if label == "Time":
        return "t"
    idx = label.find(":")
    if idx < 0:
        return label
    return label[:idx]

# read funky Rigol CSV format
def read_rigol_csv(csv_file_name, ch1 = "CH1", ch2 = "CH2", ch3 = "CH3", ch4 = "CH4", smooth = 10, shift = 0):
    # print("running helper")
    with open(csv_file_name) as f:
        rows = list(csv.reader(f))
        i = 0
        while rows[0][i] != "":
            i = i+1
        numcols = i-2
        t0 = float(rows[1][numcols])
        dt = float(rows[1][numcols+1])
    data = pd.read_csv(csv_file_name, usecols=range(0,numcols), skiprows=[1])

    data['X'] = t0 + data['X'] * dt + shift
    data['X'] = (data['X'] // dt) * dt # make sure the result is an integer multiple of dt so that joins still work

    data.rename(columns = {"X": "t"}, inplace = True)

    default_channel_names = ["CH1", "CH2", "CH3", "CH4"]
    new_channel_names = [ch1, ch2, ch3, ch4]

    for default_name, new_name in zip(default_channel_names, new_channel_names):
        if default_name in data.columns:
            data.rename(columns = {default_name: new_name}, inplace = True)
            if smooth > 0:
                data[new_name] = data[new_name].rolling(smooth).mean()

    return data, t0, dt
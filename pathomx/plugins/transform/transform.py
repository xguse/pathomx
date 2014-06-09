# -*- coding: utf-8 -*-

import csv
import xml.etree.cElementTree as et
from collections import defaultdict

import numpy as np

import pathomx.ui as ui
import pathomx.db as db
import pathomx.threads as threads
import pathomx.utils as utils

from pathomx.plugins import ProcessingPlugin
from pathomx.data import DataSet, DataDefinition
from pathomx.views import MplSpectraView, IPyMplView


class TransformApp(ui.IPythonApp):

    legacy_inputs = {'input': 'input_data'}
    legacy_outputs = {'output': 'output_data'}

    def __init__(self, **kwargs):
        super(TransformApp, self).__init__(**kwargs)

        self.addDataToolBar()
        self.addFigureToolBar()

        self.data.add_input('input_data')  # Add input slot
        self.data.add_output('output_data')  # Add output slot
        #self.table.setModel(self.data.o['output'].as_table)

        # Setup data consumer options
        self.data.consumer_defs.append(
            DataDefinition('input_data', {  # Accept anything!
            })
        )

        self.finalise()


class TransformMeanCenter(TransformApp):
    name = "Mean Center"
    notebook = 'mean_center.ipynb'

class TransformLog2(TransformApp):
    name = "Log2"
    notebook = 'log2.ipynb'

class TransformLog10(TransformApp):
    name = "Log10"
    notebook = 'log10.ipynb'

class TransformZeroBaseline(TransformApp):
    name = "Zero baseline"
    notebook = 'zero_baseline.ipynb'

class TransformGlobalMinima(TransformApp):
    name = "Global minima"
    notebook = 'global_minima.ipynb'

class TransformLocalMinima(TransformApp):
    name = "Local minima"
    notebook = 'local_minima.ipynb'

    # Minima on column by column basis (should have optional axis here)
    def fn(self, dso):
        #dso.data[dso.data==0] = np.nan
        dmin = np.ma.masked_less_equal(dso.data, 0).min(0) / 2
        inds = np.where(np.logical_and(dso.data == 0, np.logical_not(np.ma.getmask(dmin))))
        dso.data[inds] = np.take(dmin, inds[1])
        return dso


class TransformRemoveInvalid(TransformApp):
    name = "Remove invalid data"
    notebook = 'remove_invalid.ipynb'


class Transform(ProcessingPlugin):

    def __init__(self, **kwargs):
        super(Transform, self).__init__(**kwargs)
        self.register_app_launcher(TransformMeanCenter)
        self.register_app_launcher(TransformLog2)
        self.register_app_launcher(TransformLog10)
        self.register_app_launcher(TransformZeroBaseline)
        self.register_app_launcher(TransformGlobalMinima)
        self.register_app_launcher(TransformLocalMinima)
        self.register_app_launcher(TransformRemoveInvalid)

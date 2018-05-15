import os
import math
import logging
import argparse
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(message)s')

def prepare_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def log(*args):
    logging.info(*args)

def get_args():
    parser = argparse.ArgumentParser()

    # IO path
    parser.add_argument(
        '--src',
        type=str
    )
    parser.add_argument(
        '--test-src',
        dest='test_src',
        type=str
    )
    parser.add_argument(
        '--srcs',
        nargs='+',
        type=str
    )
    parser.add_argument(
        '--src-breakpoint',
        dest='src_breakpoint',
        type=str
    )
    parser.add_argument(
        '--src-centroid',
        dest='src_centroid',
        type=str
    )
    parser.add_argument(
        '--dests',
        nargs='+',
        type=str
    )
    parser.add_argument(
        '--dest-dir',
        dest='dest_dir',
        type=str
    )
    parser.add_argument(
        '--dest',
        type=str
    )
    parser.add_argument(
        '--log',
        type=str,
        help='Filename of logs'
    )
    parser.add_argument(
        '--report-roc',
        dest='report_roc',
        action='store_true'
    )

    # IO performance
    parser.add_argument(
        '--chunk-size',
        dest='chunk_size',
        type=int,
        default=10000
    )

    # threshold parameters
    parser.add_argument(
        '--alarm-minutes',
        dest='alarm_minutes',
        type=int
    )
    parser.add_argument(
        '--column',
        type=str
    )
    parser.add_argument(
        '--use-column',
        dest='use_column',
        type=int
    )
    parser.add_argument(
        '--use-columns',
        dest='use_columns',
        nargs='+',
        type=int
    )
    parser.add_argument(
        '--columns',
        nargs='+',
        type=str
    )
    parser.add_argument(
        '--ground-truth-column',
        dest='ground_truth_column',
        type=int
    )
    parser.add_argument(
        '--abs',
        dest='abs',
        action='store_true'
    )
    parser.add_argument(
        '--threshold',
        type=float
    )
    parser.add_argument(
        '--thresholds',
        nargs='+',
        type=float
    )

    # model parameters
    parser.add_argument(
        '--rnn-unit',
        dest='rnn_unit',
        type=str,
        default='LSTM'
    )
    parser.add_argument(
        '--step-size',
        dest='step_size',
        type=int
    )
    parser.add_argument(
        '--input-size',
        dest='input_size',
        type=int
    )
    parser.add_argument(
        '--hidden-size',
        dest='hidden_size',
        type=int
    )
    parser.add_argument(
        '--embedding-size',
        dest='embedding_size',
        type=int
    )
    parser.add_argument(
        '--symbol-size',
        dest='symbol_size',
        type=int
    )
    parser.add_argument(
        '--output-size',
        dest='output_size',
        type=int
    )
    parser.add_argument(
        '--layer-depth',
        dest='layer_depth',
        type=int
    )
    parser.add_argument(
        '--dropout-rate',
        dest='dropout_rate',
        type=float,
        default=0.0
    )
    parser.add_argument(
        '--learning-rates',
        dest='learning_rates',
        nargs='+',
        type=float
    )

    # visualization parameters
    parser.add_argument(
        '--sample-size',
        dest='sample_size',
        type=int
    )
    parser.add_argument(
        '--smooth',
        dest='smooth',
        type=int
    )
    parser.add_argument(
        '--batch-step',
        dest='batch_step',
        type=int,
        default=1
    )
    parser.add_argument(
        '--x-label',
        dest='x_label',
        type=str
    )
    parser.add_argument(
        '--y-label',
        dest='y_label',
        type=str
    )
    parser.add_argument(
        '--title',
        type=str
    )
    parser.add_argument(
        '--labels',
        nargs='+',
        type=str
    )
    parser.add_argument(
        '--colors',
        nargs='+',
        type=str
    )
    parser.add_argument(
        '--line-styles',
        dest='line_styles',
        nargs='+',
        type=str
    )
    parser.add_argument(
        '--markers',
        nargs='+',
        type=str
    )
    parser.add_argument(
        '--markersizes',
        nargs='+',
        type=float
    )
    parser.add_argument(
        '--ylim',
        nargs='+',
        type=float,
        default=[0, 1]
    )
    parser.add_argument(
        '--log-y-axis',
        dest='log_y_axis',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--grid',
        dest='grid',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--legend-outside',
        dest='legend_outside',
        type=float
    )

    # other parameters
    parser.add_argument(
        '--name',
        type=str
    )
    parser.add_argument(
        '--names',
        nargs='+',
        type=str
    )
    parser.add_argument(
        '--scope',
        type=str
    )
    parser.add_argument(
        '--batch-size',
        dest='batch_size',
        type=int,
        default=128
    )
    parser.add_argument(
        '--seed',
        dest='seed',
        type=int,
        default=0
    )

    args = parser.parse_args()
    return args

# http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
def get_row_count(filename):
    return sum(1 for line in open(filename))

def get_chunk_count(filename, chunk_size):
    n = get_row_count(filename)
    return int(math.ceil(float(n) / chunk_size)), n

def get_batch_count(arr, batch_size):
    length = arr.shape[0]
    return int(math.ceil(float(length) / batch_size)), length

# https://stackoverflow.com/questions/20618804/how-to-smooth-a-curve-in-the-right-way
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

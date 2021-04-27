# COMPLEXITY
# 1. assume the last dim is channel dim
# 2. batch dim must be excluded from input_shape
#
# prev_cx: previous complexity
# 
import copy
from utils import dict_add
from complexity import *


def simple_conv_stage_complexity(model_config: dict, input_shape):
    filters = model_config['filters']
    depth = model_config['depth']
    pool_size = model_config['pool_size']

    strides = model_config.get('strides', None)
    shape = input_shape
    cx = {}

    for i in range(depth):
       cx, shape = conv2d_complexity(shape, filters, 3, prev_cx=cx)
       cx, shape = norm_complexity(shape, prev_cx=cx)
    cx, shape = pool2d_complexity(shape, pool_size, strides, prev_cx=cx)
    return cx, shape


def another_conv_stage_complexity(model_config: dict, input_shape):
    return another_conv_block_complexity(model_config, input_shape)


def res_basic_stage_complexity(model_config, input_shape):
    # mandatory parameters
    depth = model_config['depth']
    strides = model_config['strides']

    model_config = copy.deepcopy(model_config)
    shape = input_shape
    total_cx = {}

    for i in range(depth):
        cx, shape = res_basic_block_complexity(model_config, shape)
        total_cx = dict_add(total_cx, cx)
        model_config['strides'] = 1
    return total_cx, shape


def res_bottleneck_stage_complexity(model_config, input_shape):
    # mandatory parameters
    depth = model_config['depth']
    strides = model_config['strides']

    model_config = copy.deepcopy(model_config)
    shape = input_shape
    total_cx = {}

    for i in range(depth):
        cx, shape = res_bottleneck_block_complexity(model_config, shape)
        total_cx = dict_add(total_cx, cx)
        model_config['strides'] = 1
    return total_cx, shape


def dense_net_stage_complexity(model_config, input_shape):
    return dense_net_block_complexity(model_config, input_shape)


def sepformer_stage_complexity(model_config, input_shape):
    depth = model_config['depth']

    shape = input_shape
    total_cx = {}

    for i in range(depth):
        cx, shape = sepformer_block_complexity(model_config, shape)
        total_cx = dict_add(total_cx, cx)
    return total_cx, shape


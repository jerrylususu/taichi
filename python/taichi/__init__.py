import sys

from taichi._funcs import *
from taichi._lib import core as _ti_core
from taichi._logging import *
from taichi._snode import *
from taichi.lang import *  # pylint: disable=W0622 # TODO(archibate): It's `taichi.lang.core` overriding `taichi.core`
from taichi.tools import *
from taichi.tools.patterns import taichi_logo
from taichi.types.annotations import *
# Provide a shortcut to types since they're commonly used.
from taichi.types.primitive_types import *

from taichi import ad
from taichi.ui import GUI, hex_to_rgb, rgb_to_hex, ui

# Issue#2223: Do not reorder, or we're busted with partially initialized module
from taichi import aot  # isort:skip
from taichi._testing import *  # isort:skip

__deprecated_names__ = {
    'SOA': 'Layout.SOA',
    'AOS': 'Layout.AOS',
    'print_profile_info': 'profiler.print_scoped_profiler_info',
    'clear_profile_info': 'profiler.clear_scoped_profiler_info',
    'CuptiMetric': 'profiler.CuptiMetric',
    'get_predefined_cupti_metrics': 'profiler.get_predefined_cupti_metrics',
    'print_kernel_profile_info': 'profiler.print_kernel_profiler_info',
    'query_kernel_profile_info': 'profiler.query_kernel_profiler_info',
    'clear_kernel_profile_info': 'profiler.clear_kernel_profiler_info',
    'kernel_profiler_total_time': 'profiler.get_kernel_profiler_total_time',
    'set_kernel_profiler_toolkit': 'profiler.set_kernel_profiler_toolkit',
    'set_kernel_profile_metrics': 'profiler.set_kernel_profiler_metrics',
    'collect_kernel_profile_metrics':
    'profiler.collect_kernel_profiler_metrics'
}

if sys.version_info.minor < 7:
    for name, alter in __deprecated_names__.items():
        exec(f'{name} = {alter}')
else:

    def __getattr__(attr):
        if attr in __deprecated_names__:
            lang.util.warning(
                f'ti.{attr} is deprecated. Please use ti.{__deprecated_names__[attr]} instead.',
                DeprecationWarning,
                stacklevel=2)
            exec(f'{attr} = {__deprecated_names__[attr]}')
            return locals()[attr]
        raise AttributeError(f"module '{__name__}' has no attribute '{attr}'")


__version__ = (_ti_core.get_version_major(), _ti_core.get_version_minor(),
               _ti_core.get_version_patch())

del sys
del _ti_core
__all__ = ['ad', 'lang', 'tools', 'ui', 'profiler']

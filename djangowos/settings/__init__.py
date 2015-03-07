import warnings

try:
    from djangowos.settings.local import *
except ImportError:
    warnings.warn('Couldn\'t import local settings')
    raise

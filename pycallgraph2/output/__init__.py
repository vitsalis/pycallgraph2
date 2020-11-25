import collections

from .output import Output
from .graphviz import GraphvizOutput
from .gephi import GephiOutput
from .ubigraph import UbigraphOutput
from .jsonout import JSONOutput
from .pickle import PickleOutput


outputters = collections.OrderedDict([
    ('graphviz', GraphvizOutput),
    ('gephi', GephiOutput),
    ('json', JSONOutput),
    # ('ubigraph', UbigraphOutput),
])

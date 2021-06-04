from graph_parser import load_source_file, BibleGraph

import igraph as ig

import chart_studio.plotly as py
from plotly.offline import iplot
import plotly.graph_objs as go

def visualize_network():
    weights = load_source_file("cross_references.txt")
    bibleGraph = BibleGraph.from_weights(weights)
    

if __name__ == '__main__':
    visualize_network()


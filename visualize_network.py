# References:
# https://towardsdatascience.com/how-to-visualize-interactive-3d-network-with-python-plotly-4ef6989d83cc
# https://plotly.com/python/v3/3d-network-graph/

from graph_parser import load_source_file, BibleGraph

import igraph as ig

import chart_studio.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go

def visualize_network(N, node_labels, node_groups, edges):
    print("Creating graph...")
    G = ig.Graph(edges, directed=False)

    print("Getting network coordinates with the Kamada-Kawai layout algorithm...")
    layt = G.layout('kk', dim=3) 

    # Get coordinates of the nodes
    Xn, Yn, Zn = [], [], []
    for k in range(N):
        Xn += [layt[k][0]]
        Yn += [layt[k][1]]
        Zn += [layt[k][2]]

    # Get coordinates of the edges
    Xe, Ye, Ze = [], [], []
    for e in edges:
        Xe += [layt[e[0]][0], layt[e[1]][0], None]
        Ye += [layt[e[0]][1], layt[e[1]][1], None]
        Ze += [layt[e[0]][2], layt[e[1]][2], None]

    print("Tracing edges...")
    trace_edges = go.Scatter3d(x=Xe, y=Ye, z=Ze, mode='lines', line=dict(color='rgb(125,125,125)', width=1),hoverinfo='none')
    print("Tracing nodes...")
    trace_nodes = go.Scatter3d(x=Xn, y=Yn, z=Zn, mode='markers', name='actors', 
                   marker=dict(symbol='circle', size=6, colorscale='Viridis', color=node_groups,
                      line=dict(color='rgb(50,50,50)', width=0.5)), text=node_labels, hoverinfo='text')
    axis = dict(showbackground=False, showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')
    print("Setting up layout...")
    layout = go.Layout(
         title="Network of references in the Bible (3D visualization)",
         width=1000,
         height=1000,
         showlegend=False,
         scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
             zaxis=dict(axis),
        ))
    
    data=[trace_edges, trace_nodes]
    print("Drawing figure...")
    fig = go.Figure(data=data, layout=layout)
    print("Saving plot...")
    plot(fig, filename='BibleReferences')


def main():
    weights = load_source_file("cross_references.txt")
    bibleGraph = BibleGraph.from_weights(weights)
    
    N = bibleGraph.lowest_unused_index
    node_labels = bibleGraph.index_to_verses
    d = {book: i for i, book in enumerate(set(bibleGraph.index_to_book))}
    node_groups = [d[ni] for ni in bibleGraph.index_to_book]

    edges = bibleGraph.references
    visualize_network(N, node_labels, node_groups, edges)


if __name__ == '__main__':
    main()


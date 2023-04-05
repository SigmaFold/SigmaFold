import dash
import dash_cytoscape as cyto
from dash import html
from dash.dependencies import Input, Output

# Create a graph using NetworkX
import networkx as nx
G = nx.Graph()
G.add_node("A", label="Node A", image="/Users/nico/Code/SigmaFold/data_analysis/capybara.png", info="Some extra data for node A")
G.add_node("B", label="Node B", image="/Users/nico/Code/SigmaFold/data_analysis/capybara.png", info="Some extra data for node B")
G.add_edge("A", "B", weight=1)

# Convert the graph to a Dash Cytoscape-compatible format
cyto_graph_data = []
for node in G.nodes:
    cyto_graph_data.append({"data": {"id": node, "label": G.nodes[node]["label"], "image": G.nodes[node]["image"], "info": G.nodes[node]["info"]}})
for edge in G.edges:
    cyto_graph_data.append({"data": {"source": edge[0], "target": edge[1]}})

# Create a Dash application
app = dash.Dash(__name__)
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=cyto_graph_data,
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)',
                    'background-image': 'data(image)',
                    'background-fit': 'cover',
                    'background-opacity': 1,
                    'width': '100px',
                    'height': '100px',
                    'border-color': 'black',
                    'border-width': 1,
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'curve-style': 'bezier',
                    'width': 2,
                    'line-color': '#cccccc',
                    'target-arrow-color': '#cccccc',
                    'target-arrow-shape': 'triangle'
                }
            }
        ]
    ),
    html.Div(id='output')
])

# Define a callback to display extra data and image when hovering over a node
@app.callback(
    Output('output', 'children'),
    Input('cytoscape', 'mouseoverNodeData')
)
def display_image_and_info(node_data):
    if node_data is not None:
        return [
            html.Img(src=node_data['image'], style={'width': '100px'}),
            html.P(node_data['info'])
        ]
    else:
        return []

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)


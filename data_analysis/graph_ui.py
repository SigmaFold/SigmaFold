"""
1. Gets all sequence data for a given n. Saves it locally for later use, in case the database is not available.
Save as pickle file.
2. Iterate through all elements. Every type a new shape_mapping is encountered, create the node and add it to the graph.
3. for every sequence, and an edge between all the shappe_mappings that it maps to.
4. Save the graph as a pickle file.
5. Display in a WEB UI using Dash.
"""
# Graph logic and data loading
import pandas as pd
import networkx as nx


import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from library.db_query_templates import get_all_sequence_data, get_all_shape_data
from library.shape_helper import deserialize_shape
from data_analysis.graph_logic import *

import os
import pickle

import pandas as pd
import plotly.express as px

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# n value controls based on what is available in the database
MIN_N = 8
MAX_N = 16
INITIAL_N = 10



def create_network_graph(n):
        # Housekeeping to avoid re-running the same queries
    if os.path.exists(f'data_analysis/sequences_df_{n}.pkl'):
        sequences_df = pd.read_pickle(f'data_analysis/sequences_df_{n}.pkl')
        shapes_df = pd.read_pickle(f'data_analysis/shapes_df_{n}.pkl')
    else:
        sequences_df = get_all_sequence_data(n)
        shapes_df = get_all_shape_data(n)
        sequences_df.to_pickle(f'data_analysis/sequences_df_{n}.pkl')
        shapes_df.to_pickle(f'data_analysis/shapes_df_{n}.pkl')

    print('Loaded data')
    # Housekeeping to avoid re-computing the entire graph every time
    graph_pickle_path = f'data_analysis/graph_{n}.pkl'

    if os.path.exists(graph_pickle_path):
        with open(graph_pickle_path, 'rb') as f:
            G = pickle.load(f)
    else:
        G = nx.Graph()

        for shape_id in shapes_df['shape_id']:
            if len(shape_id) >= 2:
                G.add_node(shape_id)

        for _, group in sequences_df.groupby('sequence'):
            shape_mappings = group['shape_mapping'].tolist()
            for i in range(len(shape_mappings)):
                for j in range(i+1, len(shape_mappings)):
                    if G.has_edge(shape_mappings[i], shape_mappings[j]):
                        G[shape_mappings[i]][shape_mappings[j]]['weight'] += 1
                    else:
                        G.add_edge(shape_mappings[i], shape_mappings[j], weight=1)

        nodes_to_remove = []
        for node in G.nodes:
            if len(node) < 2:
                nodes_to_remove.append(node)
        G.remove_nodes_from(nodes_to_remove)

        with open(graph_pickle_path, 'wb') as f:
            pickle.dump(G, f)

    # spring layout makes higher weights closer together
    pos = nx.spring_layout(G)
    shape_ids = list(G.nodes)
    xs = [pos[sid][0] for sid in shape_ids]
    ys = [pos[sid][1] for sid in shape_ids]
    shape_ids = [shape_id for shape_id in shape_ids if len(shape_id) >= 2]

    shape_matrices = {}
    for shape_id in shape_ids:
        try:
            matrix = deserialize_shape(shape_id)
            shape_matrices[shape_id] = matrix
        except:
            print("Error")
            print(shape_id)

    # Save the images and encode them as base64 strings
    base64_images = {}
    for shape_id, matrix in shape_matrices.items():
        image_path = save_image(matrix, f'{shape_id}.png')
        encoded_image = encode_image_base64(image_path)
        base64_images[shape_id] = encoded_image

    # Define node_colors
    node_colors = [G.degree(sid) for sid in shape_ids]

    fig = px.scatter(
        x=xs,
        y=ys,
        color=node_colors,
        color_continuous_scale='Viridis',
        color_continuous_midpoint=0,
        hover_name=shape_ids,
        custom_data=[shape_ids]
    )

    fig.update_traces(
        hovertemplate="Shape ID: %{customdata[0]}<br>X: %{x}<br>Y: %{y}"
    )

    fig.update_layout(
        autosize=False,
        width=900,
        height=900,
        title='Graph Visualization',
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        hovermode='closest',
        clickmode='event+select',
    )

    # Use the Dash app to serve the figure
    fig.update_layout(
        autosize=False,
        width=900,
        height=900,
        title='Graph Visualization',
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        hovermode='closest',
        clickmode='event+select',
    )

    return fig, shape_ids, shape_matrices, shapes_df, sequences_df

# Use the Dash app to serve the figure

# set initial figure
initial_fig, initial_shape_ids, initial_shape_matrices, initial_shapes_df, initial_sequences_df = create_network_graph(10)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3("Select n value"),
            dcc.Slider(
                id='n-slider',
                min=MIN_N,
                max=MAX_N,
                step=1,
                value=INITIAL_N,
                marks={i: f'{i}' for i in range(MIN_N, MAX_N + 1)}
            ),
            html.Br(),
            html.Button('Update Graph', id='update-graph-button', n_clicks=0),
            dcc.Graph(id='graph'),
            dcc.Loading(
                id="loading",
                type="circle",
                children=[html.Div(id="loading-output")]
            )
        ]),
        dbc.Col([
            html.Div([
                html.Img(id='hover-image', src=''),
                html.Pre(id='hover-data')
            ])
        ])
  
    ]),
dcc.Store(id='stored-shape-ids', data=initial_shape_ids),
dcc.Store(id='stored-shape-matrices', data=initial_shape_matrices),
dcc.Store(id='stored-shapes-df', data=initial_shapes_df.to_json(date_format='iso', orient='split')),
dcc.Store(id='stored-sequences-df', data=initial_sequences_df.to_json(date_format='iso', orient='split'))

])

@app.callback(
    Output('graph', 'figure'),
    Output('hover-image', 'src'),
    Output('hover-data', 'children'),
    Output('stored-shape-ids', 'data'),
    Output('stored-shape-matrices', 'data'),
    Output('stored-shapes-df', 'data'),
    Output('loading-output', 'children'),
    Input('update-graph-button', 'n_clicks'),
    Input('graph', 'hoverData'),
    State('n-slider', 'value'),
    State('stored-shape-ids', 'data'),
    State('stored-shape-matrices', 'data'),
    State('stored-shapes-df', 'data'),
    State('stored-sequences-df', 'data')
)
def update_graph_and_hover_data(n_clicks, hover_data, n_value, shape_ids, shape_matrices_json, shapes_df_json, sequences_df_json):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'update-graph-button':
        fig, shape_ids, shape_matrices, shapes_df, sequences_df = create_network_graph(n_value)
        shape_matrices_list = {k: v.tolist() for k, v in shape_matrices.items()}  # Convert numpy arrays to lists
        return fig, dash.no_update, dash.no_update, shape_ids, shape_matrices_list, shapes_df.to_json(date_format='iso', orient='split'), None
    elif triggered_id == 'graph' and hover_data is not None and shape_ids is not None and shape_matrices_json is not None and shapes_df_json is not None:
        shape_matrices = {k: np.array(v) for k, v in shape_matrices_json.items()}  # Convert back to numpy arrays
        point_index = hover_data['points'][0]['pointIndex']
        shape_id = shape_ids[point_index]
        image_path = f'{shape_id}.png'
        save_image(shape_matrices[shape_id], image_path)
        # get all sequences for shape_id in sequences_df
        sequences_df = pd.read_json(sequences_df_json, orient='split')
        sequences = sequences_df[sequences_df['shape_mapping'] == shape_id]
        # convert to string with newline characters
        sequences_str = '\n'.join(sequences['sequence'].values)
        
        shapes_df = pd.read_json(shapes_df_json, orient='split')
        shape_data = shapes_df[shapes_df['shape_id'] == shape_id].iloc[0]
        hover_data_text = f'\n'.join([f'{col}: {val}' for col, val in shape_data.items()])
        # add sequences to hover_data_text
        hover_data_text += f'\nSequences:\n{sequences_str}'
        
        return dash.no_update, f'/assets/{image_path}', hover_data_text, dash.no_update, dash.no_update, dash.no_update, None
    return dash.no_update, '', '', dash.no_update, dash.no_update, dash.no_update, None


if __name__ == '__main__':
    app.run_server(debug=False)
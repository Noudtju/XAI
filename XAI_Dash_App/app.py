import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import os
import random
import base64

# Constants
VIS_RESULT_DIR = 'data/Final_Dataset/visualization_results'
CLASS_NAMES = ['Acadian_Flycatcher', 'Western_Meadowlark', 'Common_Yellowthroat', 'Gadwall', 'Henslow_Sparrow']
TOTAL_TRIALS = len(CLASS_NAMES)

# Prepare 1 image per class, shuffled
def prepare_trials():
    trials = []
    for class_name in CLASS_NAMES:
        folder = os.path.join(VIS_RESULT_DIR, class_name)
        if os.path.exists(folder):
            files = os.listdir(folder)
            jpg_files = [f for f in files if f.lower().endswith('.jpg')]
            if jpg_files:
                selected = jpg_files[0]
                trials.append({
                    'class_name': class_name,
                    'image_path': os.path.join(folder, selected),
                    'image_name': selected
                })
    random.shuffle(trials)
    return trials

# Encode image
def encode_image(image_path):
    with open(image_path, 'rb') as f:
        return 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode()

# Initialize app and session
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "PIP-Net Bird Guessing App"
trials = prepare_trials()

app.layout = html.Div([
    dcc.Store(id='trial-index', data=0),
    dcc.Store(id='guesses', data=[]),
    dcc.Store(id='control-index', data=0),

    html.H2("Guess the Bird Species"),
    html.Div(id='trial-content', children=[]),
    html.Div(id='completion-message', style={'color': 'green', 'fontSize': '18px', 'marginTop': '20px'}),
    html.Div(id='post-phase1-buttons', style={'marginTop': '20px'}, children=[
        html.Button("Control Phase", id='control-btn', n_clicks=0, style={'display': 'none'}),
        html.Button("Treatment Phase", id='treatment-btn', n_clicks=0, style={'display': 'none'})
    ]),
    html.Div(id='control-phase-content', style={'marginTop': '20px'})
])

@app.callback(
    Output('trial-content', 'children'),
    Input('trial-index', 'data'),
    State('guesses', 'data')
)
def show_trial(index, guesses):
    if index >= TOTAL_TRIALS:
        return []

    trial = trials[index]
    return html.Div([
        html.H4(f"Bird {index + 1} of {TOTAL_TRIALS}"),
        html.Img(src=encode_image(trial['image_path']), style={'width': '400px', 'marginBottom': '20px'}),
        html.Label("Select the bird species:"),
        dcc.Dropdown(
            id='user-guess',
            options=[{'label': name.replace('_', ' '), 'value': name} for name in CLASS_NAMES],
            placeholder="Choose a species",
            style={'width': '300px', 'marginBottom': '20px'}
        ),
        html.Button("Next", id='next-btn', n_clicks=0)
    ])

@app.callback(
    Output('trial-index', 'data'),
    Output('guesses', 'data'),
    Output('completion-message', 'children'),
    Input('next-btn', 'n_clicks'),
    State('user-guess', 'value'),
    State('trial-index', 'data'),
    State('guesses', 'data'),
    prevent_initial_call=True
)
def save_guess(n_clicks, selection, index, guesses):
    if index < TOTAL_TRIALS and selection:
        trial = trials[index]
        guesses.append({
            "class_name": trial["class_name"],
            "image_name": trial["image_name"],
            "user_selection": selection
        })

        index += 1
        if index == TOTAL_TRIALS:
            pd.DataFrame(guesses).to_csv("user_guesses.csv", index=False)
            return index, guesses, "✅ Thank you! Your guesses have been saved."

    return index, guesses, ""

# Show Control and Treatment phase buttons after completion message
@app.callback(
    Output('control-btn', 'style'),
    Output('treatment-btn', 'style'),
    Input('completion-message', 'children')
)
def show_phase_buttons(msg):
    if msg:
        return {'display': 'inline-block', 'marginRight': '10px'}, {'display': 'inline-block'}
    return {'display': 'none'}, {'display': 'none'}


@app.callback(
    Output('control-phase-content', 'children'),
    Input('control-btn', 'n_clicks'),
    prevent_initial_call=True
)
def render_control_phase_all(n_clicks):
    children = []
    for class_name in CLASS_NAMES:
        folder = os.path.join(VIS_RESULT_DIR, class_name)
        jpg_files = [f for f in os.listdir(folder) if f.lower().endswith('.jpg')]
        if jpg_files:
            img_path = os.path.join(folder, jpg_files[0])
            encoded = encode_image(img_path)
            children.append(html.Div([
                html.H4(f"This is a {class_name.replace('_', ' ')}"),
                html.Img(src=encoded, style={'width': '400px', 'marginBottom': '40px'})
            ]))
    return children

if __name__ == '__main__':
    app.run(debug=True)

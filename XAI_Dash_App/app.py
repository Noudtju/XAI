import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import os
import random
from PIL import Image
import base64

# Paths
CSV_PATH = 'data/prediction.csv'
TRAIN_DIR = 'data/JADS_PIPNET_CARS/dataset/train'

# Prepare trials by randomly sampling 5 unique class_names, using the row with the highest activation_score for each
def prepare_trials():
    df = pd.read_csv(CSV_PATH)
    all_class_names = df['class_name'].unique()
    sampled_class_names = random.sample(list(all_class_names), 5)
    trials = []
    for class_name in sampled_class_names:
        filtered_rows = df[df['class_name'] == class_name]
        top_row = filtered_rows.loc[filtered_rows['activation_score'].idxmax()]
        folder_path = os.path.join(TRAIN_DIR, class_name)
        if os.path.exists(folder_path):
            image_files = os.listdir(folder_path)
            if image_files:
                img_path = os.path.join(folder_path, random.choice(image_files))
                trials.append({
                    'class_name': class_name,
                    'prototype_id': top_row['prototype_id'],
                    'image_path': img_path,
                    'image_name': os.path.basename(img_path)
                })
    return trials

# Encode image to base64
def encode_image(img_path):
    with open(img_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"

# Prepare session data
trials = prepare_trials()
TOTAL_TRIALS = len(trials)

# App Initialization
app = dash.Dash(__name__)
app.title = "PIP-Net Phase 1"

app.layout = html.Div([
    dcc.Store(id='phase-started', data=False),
    dcc.Store(id='phase-two-started', data=False),
    html.Div(id='welcome-section', children=[
        html.Div(id='welcome-screen', children=[
            html.H2("Welcome to the PIP-Net Car Brand Evaluation"),
            html.P("You will be shown 5 car images. Try to guess the brand based on the photo."),
            html.Label("Enter your name:"),
            dcc.Input(id='user-name', type='text', style={'marginBottom': '10px', 'width': '250px'}),
            html.Button("Start Phase 1", id='start-btn', n_clicks=0)
        ])
    ]),
    html.Div(id='phase1-section', style={'display': 'none'}, children=[
        html.Div(id='main-wrapper', children=[
            html.Div(id='main-content', children=[
                html.H3(id='trial-header'),
                html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
                    html.Img(id='car-image', style={'width': '50%', 'margin': '20px'}),
                    html.Div(style={'flex': '1', 'padding': '20px'}, children=[
                        html.Label("Guess the car brand:"),
                        dcc.Input(id='user-guess', type='text', debounce=False, style={'width': '100%', 'marginBottom': '10px'}),
                        html.Button("Next", id='next-btn', n_clicks=0),
                    ])
                ])
            ])
        ])
    ]),
    dcc.Store(id='trial-index', data=0),
    dcc.Store(id='guesses', data=[]),
    dcc.Store(id='user-name-store'),
    dcc.Store(id='user-id-store'),

    html.Div(id='completion-controls', children=[
        html.Div(id='completion-message', style={'color': 'green', 'fontSize': '20px'}),
        html.Button("Proceed to Phase 2", id='phase2-btn', n_clicks=0, style={'display': 'none', 'marginTop': '10px'})
    ]),

    html.Div(id='phase-two-container', style={'marginTop': '30px'})
])

@app.callback(
    Output('user-name-store', 'data'),
    Output('user-id-store', 'data'),
    Input('start-btn', 'n_clicks'),
    State('user-name', 'value')
)
def store_user_info(n_clicks, user_name):
    if n_clicks > 0 and user_name:
        user_id = 1
        try:
            if os.path.exists("user_guesses.csv"):
                df = pd.read_csv("user_guesses.csv")
                if 'user_id' in df.columns:
                    user_id = df['user_id'].max() + 1
        except:
            pass
        return user_name, int(user_id)
    return dash.no_update, dash.no_update

@app.callback(
    Output('trial-header', 'children'),
    Output('car-image', 'src'),
    Output('user-guess', 'value'),
    Output('main-content', 'style'),
    Output('completion-message', 'children'),
    Output('guesses', 'data'),
    Output('trial-index', 'data'),
    Input('next-btn', 'n_clicks'),
    State('user-guess', 'value'),
    State('trial-index', 'data'),
    State('guesses', 'data'),
    State('phase-started', 'data'),
    Input('start-btn', 'n_clicks'),
    State('user-name-store', 'data'),
    State('user-id-store', 'data')
)
def update_trial(n_clicks, current_guess, index, guesses, started, start_clicks, user_name, user_id):
    if not started and start_clicks == 0:
        return "", "", "", {'display': 'none'}, "", guesses, index
    elif start_clicks > 0 and index == 0 and n_clicks == 0:
        trial = trials[0]
        return (
            f"Trial 1/5",
            encode_image(trial['image_path']),
            "",
            {'display': 'block'},
            "",
            guesses,
            0
        )

    # Save the current guess
    if index < TOTAL_TRIALS:
        guesses.append({
            "index": index + 1,
            "user_name": user_name,
            "user_id": user_id,
            "class_name": trials[index]['class_name'],
            "prototype_id": trials[index]['prototype_id'],
            "image_name": trials[index]['image_name'],
            "guess": current_guess
        })

    # If this was the last trial, save and show thank you
    if index == TOTAL_TRIALS - 1:
        df = pd.DataFrame(guesses)
        df.to_csv("user_guesses.csv", index=False, columns=["index", "user_name", "user_id", "class_name", "prototype_id", "image_name", "guess"])
        return (
            "",
            "",
            "",
            {'display': 'none'},
            "✅ Thank you for participating! Your responses have been recorded.",
            guesses,
            index + 1
        )

    # Move to next trial
    next_index = index + 1
    trial = trials[next_index]
    return (
        f"Trial {next_index + 1}/5",
        encode_image(trial['image_path']),
        "",
        {'display': 'block'},
        "",
        guesses,
        next_index
    )


# Show Phase 2 button when completion message is present
@app.callback(
    Output('phase2-btn', 'style'),
    Input('completion-message', 'children')
)
def show_phase2_button(message):
    if message:
        return {'display': 'block', 'marginTop': '10px'}
    return {'display': 'none'}

# Handle transition to Phase 2
@app.callback(
    Output('phase-two-container', 'children'),
    Output('phase-two-started', 'data'),
    Input('phase2-btn', 'n_clicks'),
    prevent_initial_call=True
)
def launch_phase_two(n_clicks):
    if n_clicks > 0:
        return html.Div("📘 Phase 2: Teaching Phase begins here..."), True
    return dash.no_update, dash.no_update

@app.callback(
    Output('welcome-section', 'style'),
    Output('phase1-section', 'style'),
    Input('start-btn', 'n_clicks'),
    prevent_initial_call=True
)
def switch_sections(n_clicks):
    if n_clicks > 0:
        return {'display': 'none'}, {'display': 'block'}
    return dash.no_update, dash.no_update

if __name__ == '__main__':
    app.run(debug=True)
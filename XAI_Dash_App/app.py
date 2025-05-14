import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import os
import random
import base64

# Constants
VIS_RESULT_DIR = 'data/dataset/visualization_results'
TEST_IMAGE_DIR = 'data/dataset/train'
CLASS_NAMES = ['Acadian_Flycatcher', 'Western_Meadowlark', 'Common_Yellowthroat', 'Gadwall', 'Henslow_Sparrow']
TOTAL_TRIALS = len(CLASS_NAMES)
test_trials = []

# Prepare 1 image per class, randomized
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

#Prepare 1 image per class for testing, randomized
def prepare_test_trials():
    trials = []
    for class_name in CLASS_NAMES:
        folder = os.path.join(TEST_IMAGE_DIR, class_name)
        if os.path.exists(folder):
            files = os.listdir(folder)
            jpg_files = [f for f in files if f.lower().endswith('.jpg')]
            if jpg_files:
                selected = random.choice(jpg_files)
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
user_guesses_data = []
csv_path = "user_guesses.csv"
if os.path.exists(csv_path):
    user_guesses_data = pd.read_csv(csv_path).to_dict(orient='records')
trials = prepare_trials()

# Initialize layout
app.layout = html.Div(style={
    'backgroundImage': 'url("/assets/pip_net_bird_image.png")', 
    'backgroundSize': 'cover',
    'backgroundRepeat': 'no-repeat',
    'backgroundPosition': 'center',
    'minHeight': '100vh',
    'padding': '30px'
}, children=[
    dcc.Store(id='trial-index', data=0),
    dcc.Store(id='guesses', data=[]),
    dcc.Store(id='control-index', data=0),
    dcc.Store(id='phase3-index', data=0),
    dcc.Store(id='phase3-guesses', data=[]),
    dcc.Store(id='user-name', data=''),

    html.Div(id='user-info', style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'marginBottom': '30px',
        'height': '100vh',
        'textAlign': 'center'
    }, children=[
        html.Label("Enter your name:", style={'fontSize': '22px', 'marginBottom': '15px'}),
        dcc.Input(
            id='user-name-input',
            type='text',
            placeholder='Your name',
            style={'marginBottom': '20px', 'padding': '10px', 'fontSize': '18px', 'width': '350px'}
        ),
        html.Button("Start Phase 1: Guess the Bird", id='start-phase1-btn', n_clicks=0, style={
            'padding': '12px 24px',
            'fontSize': '18px',
            'cursor': 'pointer'
        })
    ]),

    html.Div(
        id='phase1-container',
        style={'display': 'none', 'width': '100%', 'maxWidth': '600px', 'margin': '0 auto', 'padding': '30px 0'},
        children=[
            html.H2("Guess the Bird Species", style={'textAlign': 'center', 'marginBottom': '30px'}),
            html.Div(
                id='guess-phase-container',
                style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'minHeight': '100vh',
                    'textAlign': 'center'
                },
                children=[
                    html.Div(id='trial-content', children=[]),
                    html.Div(
                        id='completion-message',
                        style={
                            'color': 'white',
                            'backgroundColor': 'green',
                            'padding': '15px 25px',
                            'borderRadius': '8px',
                            'fontSize': '20px',
                            'marginTop': '30px',
                            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                            'display': 'block'
                        }
                    )
                ]
            )
        ]
    ),

    html.Div(id='phase2-container', children=[
        html.Div(
            id='post-phase1-buttons',
            style={
                'marginTop': '20px',
                'display': 'flex',
                'justifyContent': 'center',
                'gap': '20px'
            },
            children=[
                html.Button(
                    "Control Phase",
                    id='control-btn',
                    n_clicks=0,
                    style={
                        'display': 'none',
                        'padding': '18px 36px',
                        'fontSize': '20px',
                        'cursor': 'pointer',
                        'border': 'none',
                        'borderRadius': '6px',
                        'backgroundColor': '#ffffff',
                        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'
                    }
                ),
                html.Button(
                    "Treatment 1 Patch",
                    id='treatment1-btn',
                    n_clicks=0,
                    style={
                        'display': 'none',
                        'padding': '18px 36px',
                        'fontSize': '20px',
                        'cursor': 'pointer',
                        'border': 'none',
                        'borderRadius': '6px',
                        'backgroundColor': '#ffffff',
                        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'
                    }
                ),
                html.Button(
                    "Treatment 2 Rectangle",
                    id='treatment2-btn',
                    n_clicks=0,
                    style={
                        'display': 'none',
                        'padding': '18px 36px',
                        'fontSize': '20px',
                        'cursor': 'pointer',
                        'border': 'none',
                        'borderRadius': '6px',
                        'backgroundColor': '#ffffff',
                        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'
                    }
                )
            ]
        ),
        html.Div(id='treatment1-content', style={'marginTop': '20px'}),
        html.Div(id='control-phase-content', style={'marginTop': '20px'}),
        html.Div(id='treatment2-content', style={'marginTop': '20px'}),
    ]),

    html.Button("Move to Phase 3", id='to-phase3-btn', n_clicks=0, style={'display': 'none', 'marginTop': '20px'}),
    html.Div(id='phase3-content', style={'marginTop': '20px'}),
    dcc.Dropdown(id='phase3-user-guess', style={'display': 'none'}),
    html.Button(id='phase3-next-btn', style={'display': 'none'}),
])

@app.callback(
    Output('phase1-container', 'style'),
    Output('user-name', 'data'),
    Output('user-info', 'style'),
    Input('start-phase1-btn', 'n_clicks'),
    State('user-name-input', 'value'),
    prevent_initial_call=True
)
def start_phase1(n_clicks, name):
    if name:
        return {'display': 'block'}, name, {'display': 'none'}
    return dash.no_update, dash.no_update, dash.no_update

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
        html.Div([
            html.Label("Select the bird species:", style={'fontSize': '18px', 'marginRight': '10px'}),
            dcc.Dropdown(
                id='user-guess',
                options=[{'label': name.replace('_', ' '), 'value': name} for name in CLASS_NAMES] + [{'label': "I don't know", 'value': "I don't know"}],
                placeholder="Choose a species",
                style={'width': '300px', 'fontSize': '16px'}
            )
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'marginBottom': '20px'
        }),
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
    State('user-name', 'data'),
    prevent_initial_call=True
)
def save_guess(n_clicks, selection, index, guesses, user_name):
    if index < TOTAL_TRIALS and selection:
        trial = trials[index]
        guesses.append({
            "class_name": trial["class_name"],
            "image_name": trial["image_name"],
            "user_selection": selection,
            "user_name": user_name
        })

        index += 1
        if index == TOTAL_TRIALS:
            for guess in guesses:
                guess["teaching_phase"] = ""
            global user_guesses_data
            user_guesses_data = guesses
            # Write combined CSV
            df_existing = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame()
            df_new = pd.DataFrame(user_guesses_data)
            df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["class_name", "user_name"], keep="last")
            df_combined.to_csv(csv_path, index=False)
            return index, guesses, "✅ Thank you! Your guesses have been saved."

    return index, guesses, ""

# Show Control and Treatment phase buttons after completion message
@app.callback(
    Output('control-btn', 'style'),
    Output('treatment1-btn', 'style'),
    Output('treatment2-btn', 'style'),
    Input('completion-message', 'children')
)
def show_phase_buttons(msg):
    if msg:
        return {'display': 'inline-block', 'marginRight': '10px'}, {'display': 'inline-block', 'marginRight': '10px'}, {'display': 'inline-block'}
    return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

@app.callback(
    Output('to-phase3-btn', 'style'),
    Input('control-btn', 'n_clicks'),
    Input('treatment1-btn', 'n_clicks'),
    Input('treatment2-btn', 'n_clicks')
)
def show_phase3_button(n1, n2, n3):
    if any([n1, n2, n3]):
        return {'display': 'inline-block', 'marginTop': '20px'}
    return {'display': 'none'}

# Phase 3 callback
@app.callback(
    Output('phase3-index', 'data'),
    Output('phase3-guesses', 'data'),
    Output('phase3-content', 'children'),
    Input('to-phase3-btn', 'n_clicks'),
    Input('phase3-next-btn', 'n_clicks'),
    State('phase3-user-guess', 'value'),
    State('phase3-index', 'data'),
    State('phase3-guesses', 'data'),
    State('user-name', 'data'),
    prevent_initial_call=True
)
def handle_phase3(to_phase3_clicks, next_clicks, selection, index, guesses, user_name):
    global test_trials

    # Prepare test trials on first click
    if dash.callback_context.triggered_id == 'to-phase3-btn':
        if not test_trials:
            test_trials = prepare_test_trials()
        if index >= len(test_trials):
            return index, guesses, html.Div("✅ Testing phase completed!", style={
                'color': 'white',
                'backgroundColor': 'green',
                'padding': '15px 25px',
                'borderRadius': '8px',
                'fontSize': '20px',
                'marginTop': '30px',
                'textAlign': 'center',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
            })
        trial = test_trials[index]
        # Updated layout for both 'to-phase3-btn' and 'phase3-next-btn'
        return index, guesses, html.Div([
            html.Div(style={
                'width': '100%',
                'maxWidth': '600px',
                'margin': '0 auto',
                'padding': '30px 0',
                'textAlign': 'center'
            }, children=[
                html.H4(f"Testing Phase: Bird {index + 1} of {len(test_trials)}", style={'marginBottom': '30px'}),
                html.Img(src=encode_image(trial['image_path']), style={'width': '400px', 'marginBottom': '20px'}),
                html.Div([
                    html.Label("Select the bird species:", style={'fontSize': '18px', 'marginRight': '10px'}),
                    dcc.Dropdown(
                        id='phase3-user-guess',
                        options=[{'label': name.replace('_', ' '), 'value': name} for name in CLASS_NAMES] + [{'label': "I don't know", 'value': "I don't know"}],
                        placeholder="Choose a species",
                        style={'width': '300px', 'fontSize': '16px'}
                    )
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'marginBottom': '20px'
                }),
                html.Button("Next (Testing)", id='phase3-next-btn', n_clicks=0)
            ])
        ])

    # Handle next guess
    elif dash.callback_context.triggered_id == 'phase3-next-btn':
        if index < len(test_trials) and selection:
            trial = test_trials[index]
            global user_guesses_data
            for record in user_guesses_data:
                if record["class_name"] == trial["class_name"]:
                    record["testing_phase_class_shown"] = trial["class_name"]
                    record["testing_phase_user_answer"] = selection
                    break
            index += 1
            
            # Write combined CSV
            df_existing = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame()
            df_new = pd.DataFrame(user_guesses_data)
            df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["class_name", "user_name"], keep="last")
            df_combined.to_csv(csv_path, index=False)
            if index == len(test_trials):
                return index, guesses, html.Div("✅ Testing phase completed!", style={
                    'color': 'white',
                    'backgroundColor': 'green',
                    'padding': '15px 25px',
                    'borderRadius': '8px',
                    'fontSize': '20px',
                    'marginTop': '30px',
                    'textAlign': 'center',
                    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
                })
            next_trial = test_trials[index]
            # Updated layout for both 'to-phase3-btn' and 'phase3-next-btn'
            return index, guesses, html.Div([
                html.Div(style={
                    'width': '100%',
                    'maxWidth': '600px',
                    'margin': '0 auto',
                    'padding': '30px 0',
                    'textAlign': 'center'
                }, children=[
                    html.H4(f"Testing Phase: Bird {index + 1} of {len(test_trials)}", style={'marginBottom': '30px'}),
                    html.Img(src=encode_image(next_trial['image_path']), style={'width': '400px', 'marginBottom': '20px'}),
                    html.Div([
                        html.Label("Select the bird species:", style={'fontSize': '18px', 'marginRight': '10px'}),
                        dcc.Dropdown(
                            id='phase3-user-guess',
                            options=[{'label': name.replace('_', ' '), 'value': name} for name in CLASS_NAMES] + [{'label': "I don't know", 'value': "I don't know"}],
                            placeholder="Choose a species",
                            style={'width': '300px', 'fontSize': '16px'}
                        )
                    ], style={
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'marginBottom': '20px'
                    }),
                    html.Button("Next (Testing)", id='phase3-next-btn', n_clicks=0)
                ])
            ])
        return index, guesses, dash.no_update

    return dash.no_update, dash.no_update, dash.no_update

# Control Phase callback
@app.callback(
    Output('control-phase-content', 'children'),
    Input('control-btn', 'n_clicks'),
    prevent_initial_call=True
)
def render_control_phase_all(n_clicks):
    for record in user_guesses_data:
        record["teaching_phase"] = "control"
    # Write combined CSV
    df_existing = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame()
    df_new = pd.DataFrame(user_guesses_data)
    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["class_name", "user_name"], keep="last")
    df_combined.to_csv(csv_path, index=False)
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

# Treatment 1 Patch callback
@app.callback(
    Output('treatment1-content', 'children'),
    Input('treatment1-btn', 'n_clicks'),
    prevent_initial_call=True
)
def render_treatment1_patch(n_clicks):
    for record in user_guesses_data:
        record["teaching_phase"] = "treatment1"
    # Write combined CSV
    df_existing = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame()
    df_new = pd.DataFrame(user_guesses_data)
    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["class_name", "user_name"], keep="last")
    df_combined.to_csv(csv_path, index=False)
    children = []
    for class_name in CLASS_NAMES:
        class_dir = os.path.join(VIS_RESULT_DIR, class_name)
        if not os.path.exists(class_dir):
            continue
        subdirs = [d for d in os.listdir(class_dir) if os.path.isdir(os.path.join(class_dir, d)) and class_name in d]
        if not subdirs:
            continue
        full_path = os.path.join(class_dir, subdirs[0])
        patch_files = [f for f in os.listdir(full_path) if f.endswith('_patch.png')]

        patch_images = []
        for file in patch_files:
            parts = file.replace('.png', '').split('_')
            mul = next((p[3:] for p in parts if p.startswith('mul')), 'N/A')
            sim = next((p[3:] for p in parts if p.startswith('sim')), 'N/A')
            weight = next((p[1:] for p in parts if p.startswith('w')), 'N/A')

            img_path = os.path.join(full_path, file)
            encoded = encode_image(img_path)

            patch_images.append(html.Div([
                html.Img(src=encoded, style={'width': '150px'}),
                html.P(f"Mul: {mul} | Similarity: {sim} | Weight: {weight}", style={'fontSize': '12px'})
            ], style={'marginRight': '20px'}))

        # Fetch class-level image
        jpg_files = [f for f in os.listdir(class_dir) if f.lower().endswith('.jpg')]
        class_img = None
        if jpg_files:
            class_img_path = os.path.join(class_dir, jpg_files[0])
            class_img_encoded = encode_image(class_img_path)
            class_img = html.Img(src=class_img_encoded, style={'width': '150px', 'marginRight': '15px'})

        children.append(html.Div([
            html.Div([
                html.H4(class_name.replace('_', ' ')),
                class_img
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            html.Div(patch_images, style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '40px'})
        ]))
    return children

# Treatment 2 Rectangle callback
@app.callback(
    Output('treatment2-content', 'children'),
    Input('treatment2-btn', 'n_clicks'),
    prevent_initial_call=True
)
def render_treatment2_rectangle(n_clicks):
    for record in user_guesses_data:
        record["teaching_phase"] = "treatment2"
    # Write combined CSV
    df_existing = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame()
    df_new = pd.DataFrame(user_guesses_data)
    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["class_name", "user_name"], keep="last")
    df_combined.to_csv(csv_path, index=False)
    children = []
    for class_name in CLASS_NAMES:
        class_dir = os.path.join(VIS_RESULT_DIR, class_name)
        if not os.path.exists(class_dir):
            continue
        subdirs = [d for d in os.listdir(class_dir) if os.path.isdir(os.path.join(class_dir, d)) and class_name in d]
        if not subdirs:
            continue
        full_path = os.path.join(class_dir, subdirs[0])
        rect_files = [f for f in os.listdir(full_path) if f.endswith('_rect.png')]

        rect_images = []
        for file in rect_files:
            parts = file.replace('.png', '').split('_')
            mul = next((p[3:] for p in parts if p.startswith('mul')), 'N/A')
            sim = next((p[3:] for p in parts if p.startswith('sim')), 'N/A')
            weight = next((p[1:] for p in parts if p.startswith('w')), 'N/A')

            img_path = os.path.join(full_path, file)
            encoded = encode_image(img_path)

            rect_images.append(html.Div([
                html.Img(src=encoded, style={'width': '150px'}),
                html.P(f"Mul: {mul} | Similarity: {sim} | Weight: {weight}", style={'fontSize': '12px'})
            ], style={'marginRight': '20px'}))

        # Fetch class-level image
        jpg_files = [f for f in os.listdir(class_dir) if f.lower().endswith('.jpg')]
        class_img = None
        if jpg_files:
            class_img_path = os.path.join(class_dir, jpg_files[0])
            class_img_encoded = encode_image(class_img_path)
            class_img = html.Img(src=class_img_encoded, style={'width': '150px', 'marginRight': '15px'})

        children.append(html.Div([
            html.Div([
                html.H4(class_name.replace('_', ' ')),
                class_img
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            html.Div(rect_images, style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '40px'})
        ]))
    return children

# Hide phase 2 container when moving to phase 3
@app.callback(
    Output('phase2-container', 'style'),
    Input('to-phase3-btn', 'n_clicks'),
    prevent_initial_call=True
)
def hide_phase2(n):
    if n:
        return {'display': 'none'}
    return dash.no_update

if __name__ == '__main__':
    app.run(debug=True)

# Hide phase1-container when any Phase 2 button is clicked
@app.callback(
    Output('phase1-container', 'style'),
    Input('control-btn', 'n_clicks'),
    Input('treatment1-btn', 'n_clicks'),
    Input('treatment2-btn', 'n_clicks'),
    prevent_initial_call=True
)
def hide_phase1(n1, n2, n3):
    if any([n1, n2, n3]):
        return {'display': 'none'}
    return dash.no_update

# Hide completion-message when any Phase 2 button is clicked
@app.callback(
    Output('completion-message', 'style'),
    Input('control-btn', 'n_clicks'),
    Input('treatment1-btn', 'n_clicks'),
    Input('treatment2-btn', 'n_clicks'),
    prevent_initial_call=True
)
def hide_completion_msg(n1, n2, n3):
    if any([n1, n2, n3]):
        return {'display': 'none'}
    return dash.no_update
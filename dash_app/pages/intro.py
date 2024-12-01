from dash import html, dcc, Input, Output, callback
import dash

dash.register_page(__name__, path="/")

layout = html.Div(
    id="intro-page",
    style={
        'backgroundColor': 'black',
        'height': '100vh',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'position': 'absolute',
        'top': '0',
        'left': '0',
        'width': '100%',
        'zIndex': 2,
        'transition': 'opacity 1s ease-in-out',
    },
    children=[
        html.Video(
            id="intro-video",
            src='/assets/SpotifyLogo.mp4',
            autoPlay=True,
            controls=False,
            loop=False,
            muted=True,
            style={'width': '50%'},
        ),
        dcc.Interval(
            id="show-button-timer",
            interval=4000,  # Show button after 4 seconds
            n_intervals=0,
            max_intervals=1,
        ),
        html.Div(
            id="button-container",
            children=html.Button(
                "Enter App",  # Button text
                id="enter-button",
                style={
                    'marginTop': '20px',
                    'padding': '10px 20px',
                    'fontSize': '16px',
                    'backgroundColor': '#1DB954',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '30px',
                    'cursor': 'pointer',
                    'display': 'none',  # Initially hidden
                },
                className="fade-in",  # Add animation class
            ),
            style={'height': '80px', 'display': 'flex', 'alignItems': 'center'},
        ),
    ]
)

# Callback to show the button after timer completes
@callback(
    Output("enter-button", "style"),
    Input("show-button-timer", "n_intervals"),
)
def show_button(n_intervals):
    if n_intervals > 0:
        return {
            'marginTop': '20px',
            'padding': '10px 20px',
            'fontSize': '16px',
            'backgroundColor': '#1DB954',
            'color': 'white',
            'border': 'none',
            'borderRadius': '30px',
            'cursor': 'pointer',
            'display': 'inline-block',  # Make it visible
            'transition': 'opacity 1s ease-in-out, transform 0.3s ease',
            'opacity': '1',
        }
    return {'display': 'none'}

# Callback to navigate to main page
@callback(
    Output("url", "pathname"),
    Input("enter-button", "n_clicks"),
    prevent_initial_call=True,
)
def navigate_to_main(n_clicks):
    if n_clicks:
        return "/main"
    return "/"

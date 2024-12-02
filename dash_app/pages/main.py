from dash import html, dcc, Input, Output, State, callback
import dash
import pandas as pd
import requests
from io import BytesIO
from colorthief import ColorThief
from colorsys import rgb_to_hls, hls_to_rgb

dash.register_page(__name__, path="/main")

# Load the podcast data
podcast_data = pd.read_csv("podcast_details.csv")  # Replace with the actual path to your CSV

# Extract relevant fields
podcast_options = sorted(
    [{"label": row["name"], "value": row["name"]} for _, row in podcast_data.iterrows()],
    key=lambda x: x["label"]
)

# Function to get dominant colors from an image
def get_dominant_colors(image_url, num_colors=3):
    response = requests.get(image_url)
    image = BytesIO(response.content)
    color_thief = ColorThief(image)
    palette = color_thief.get_palette(color_count=num_colors)
    return [f"rgb({r}, {g}, {b})" for r, g, b in palette]

# Custom CSS for more advanced styling
app_css = {
    'background': 'linear-gradient(135deg, #121212 0%, #1E1E1E 100%)',
    'fontFamily': '"Circular", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
}

layout = html.Div(
    style={
        **app_css,
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100vh',
        'color': 'white',
        'padding': '20px',
        'overflow': 'hidden',
    },
    children=[
        # Header
        html.Div(
            style={
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'space-between',  # Ensures logo on the left and dropdown on the right
                'marginBottom': '20px',
                'padding': '0 20px',
            },
            children=[
                # Spotify Logo on the left
                html.Img(
                    src="/assets/SpotifyLogo.png",
                    alt="Spotify Logo",
                    style={
                        'width': '300px',  # Adjust the size of the logo
                        'height': 'auto',
                    }
                ),
                # Dropdown on the right
                dcc.Dropdown(
                    id="podcast-dropdown",
                    options=podcast_options,
                    placeholder="Search for a podcast...",
                    style={
                        'width': '300px',
                        'height': '50px',
                        'backgroundColor': '#282828',
                        'color': '#1DB954',
                        'borderRadius': '20px',
                        'textAlign': 'left',
                    },
                    optionHeight=50,
                    className='custom-dropdown',
                ),
            ]
        ),
        
        # Main Content Area
        html.Div(
            style={
                'display': 'flex',
                'flex': '1',
                'gap': '20px',
                'overflow': 'hidden',
            },
            children=[
                # Podcast Details Column
                html.Div(
                    id="podcast-details-container",
                    style={
                        'width': '400px',
                        'backgroundColor': '#282828',
                        'borderRadius': '15px',
                        'padding': '20px',
                        'overflowY': 'auto',
                        'boxShadow': '0 10px 20px rgba(0,0,0,0.2)',
                    },
                    children=[
                        html.Div(
                            id="podcast-details",
                            style={
                                'textAlign': 'center',
                            }
                        )
                    ]
                )
            ]
        )
    ]
)

# Callback to update podcast details
@callback(
    [Output("podcast-details", "children"), Output("podcast-details-container", "style")],
    Input("podcast-dropdown", "value"),
)
def update_podcast_details(selected_podcast):
    default_style = {
        'width': '400px',
        'backgroundColor': '#282828',  # Static background
        'borderRadius': '15px',
        'padding': '20px',
        'overflowY': 'auto',
        'boxShadow': '0 10px 20px rgba(0,0,0,0.2)',
        'border': '2px solid #282828',  # Default border
        'transition': 'all 0.5s ease-in-out',
    }
    
    if not selected_podcast:
        return (
            html.Div(
                "Select a podcast to view details.",
                style={'color': '#B3B3B3', 'textAlign': 'center'}
            ),
            default_style
        )
    
    # Fetch podcast details
    podcast = podcast_data[podcast_data["name"] == selected_podcast].iloc[0]
    image_url = podcast["image_url"]

    # Try extracting dominant colors, fallback if needed
    try:
        colors = get_dominant_colors(image_url)
        border_color = colors[0]
        shadow_color = colors[0]

    except Exception:
        # Fallback colors (Spotify green gradient)
        border_color = "#1DB954"
        shadow_color = "rgba(29, 185, 84, 0.3)"

    # Ensure colors are lightened if too dark for visibility
    def ensure_contrast(rgb_color):
        r, g, b = [x / 255.0 for x in rgb_color]
        h, l, s = rgb_to_hls(r, g, b)
        if l < 0.3:  # If luminance is too low
            l += 0.3
        r, g, b = hls_to_rgb(h, l, s)
        return f"rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)})"

    try:
        border_color = ensure_contrast(tuple(int(c) for c in border_color[4:-1].split(", ")))
        shadow_color = ensure_contrast(tuple(int(c) for c in shadow_color[4:-1].split(", ")))
    except:
        pass  # Keep fallback colors if processing fails

    # Details content
    details = html.Div(
        children=[
            html.Img(
                src=podcast["image_url"],
                style={
                    'width': '250px',
                    'height': '250px',
                    'objectFit': 'cover',
                    'borderRadius': '15px',
                    'marginBottom': '20px',
                    'boxShadow': '0 10px 20px rgba(0,0,0,0.3)',
                },
            ),
            html.H3(
                podcast["name"], 
                style={
                    'color': '#1DB954', 
                    'marginBottom': '10px',
                    'fontSize': '1.5rem',
                }
            ),
            html.P(f"Publisher: {podcast['publisher']}", style={'color': '#B3B3B3', 'marginBottom': '10px'}),
            html.P(f"{podcast['description']}", style={'color': '#B3B3B3', 'marginBottom': '10px'}),
            html.P(f"Total Episodes: {podcast['total_episodes']}", style={'color': '#B3B3B3', 'marginBottom': '10px'}),
            html.P(f"Category: {podcast['category']}", style={'color': '#B3B3B3', 'marginBottom': '20px'}),
            html.Div(
                children=[
                    dcc.Link(
                        "Listen on Spotify",
                        href=podcast["external_url"],
                        target="_blank",
                        style={
                            'backgroundColor': '#1DB954',
                            'color': 'white',
                            'padding': '10px 20px',
                            'borderRadius': '25px',
                            'textDecoration': 'none',
                            'fontWeight': 'bold',
                            'transition': 'transform 0.2s',
                            'display': 'inline-block',
                        },
                        className='click-button'
                    ),
                    html.Button(
                        "+",
                        id="add-to-plot",
                        style={
                            'marginLeft': '10px',
                            'backgroundColor': '#1DB954',
                            'border': 'none',
                            'borderRadius': '25px',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'padding': '10px 15px',
                            'cursor': 'pointer',
                            'transition': 'all 0.3s ease',
                        },
                        className="click-button"
                    )
                ],
                style={'display': 'flex', 'justifyContent': 'center', 'gap': '10px'}
            )
        ],
        style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'textAlign': 'center',
        }
    )
    
    # Update container style with dynamic border and shadow
    container_style = {
        **default_style,
        'boxShadow': f"0 10px 20px {shadow_color}",  # Dynamic shadow
        'border': f"2px solid {border_color}",  # Dynamic border color
    }

    return details, container_style

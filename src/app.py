import dash
import dash_bootstrap_components as dbc
from src.layout import *
from src.callbacks import *
import os

# Initialize Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "QuantaTrack"

# Bind layout
app.layout = layout

# Register callback functions
register_callbacks(app)

# Run application
if __name__ == "__main__":
    app.run_server(debug=True)
    # port = int(os.environ.get("PORT", 8080))  # Use port provided by Render
    # app.run_server(debug=False, host="0.0.0.0", port=port)

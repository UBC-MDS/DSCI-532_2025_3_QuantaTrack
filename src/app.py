import dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import *

# 初始化 Dash 应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "QuantaTrack"

# 绑定布局
app.layout = layout

# 注册回调函数
register_callbacks(app)

# 运行应用
if __name__ == "__main__":
    app.run_server(debug=False)

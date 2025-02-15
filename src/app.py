import dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

# 初始化 Dash 应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "NASDAQ 100 Companies"

# 绑定布局
app.layout = layout

# 注册回调函数
register_callbacks(app)

# 运行应用
if __name__ == "__main__":
    app.run_server(debug=True)

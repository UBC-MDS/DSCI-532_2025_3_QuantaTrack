import dash
import dash_bootstrap_components as dbc
from src.layout import layout
from src.callbacks import *
import os

# 初始化 Dash 应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "QuantaTrack"

# 绑定布局
app.layout = layout

# 注册回调函数
register_callbacks(app)

# 运行应用
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8080))  # 使用 Render 提供的端口
#     app.run_server(debug=False, host="0.0.0.0", port=port)

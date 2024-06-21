import dash_bootstrap_components as dbc

from dash import Dash, Input, Output, dcc, html
from pages import country_sravnenie, university_results, analiz_kriterii, global_tendensii, university_sravnenie

external_stylesheets = [dbc.themes.PULSE] 
app = Dash(__name__, external_stylesheets=external_stylesheets,  use_pages=True)
app.config.suppress_callback_exceptions = True

# Задаем аргументы стиля для боковой панели. Мы используем position:fixed и фиксированную ширину
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#6AABE4", # Цвет фона боковой панели меняем на тот, который больше всего подходит
}

# Справа от боковой панели размешается основной дашборд. Добавим отступы
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    }

sidebar = html.Div(
    [
        html.H2("Показатели университетов мира", className="display-6"),
        html.Hr(),
        html.P(
            "Учебный проект студентов БСБО-15-21 Савчука Ивана, Булавина Даниила", className="lead", 
        ),
        dbc.Nav(
            [
                dbc.NavLink("Глобальные тенденции", href="/", active="exact"),
                dbc.NavLink("Сравнение стран", href="/page-1", active="exact"),
                dbc.NavLink("Результаты университетов", href="/page-2", active="exact"),
                dbc.NavLink("Анализ критериев", href="/page-3", active="exact"),
                dbc.NavLink("Сравнение университетов", href="/page-4", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return global_tendensii.layout
    elif pathname == "/page-1":
        return country_sravnenie.layout
    elif pathname == "/page-2":
        return university_results.layout
    elif pathname == "/page-3":
        return analiz_kriterii.layout
    elif pathname == "/page-4":
        return university_sravnenie.layout
    # Если пользователь попытается перейти на другую страницу, верните сообщение 404. Мы изменим её в следующей практической.
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

if __name__ == '__main__':
        app.run_server(debug=True)


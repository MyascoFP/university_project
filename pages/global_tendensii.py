from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from data import df

# Предобработка данных
df['teaching'] = pd.to_numeric(df['teaching'], errors='coerce').fillna(0)
df['research'] = pd.to_numeric(df['research'], errors='coerce').fillna(0)
df['citations'] = pd.to_numeric(df['citations'], errors='coerce').fillna(0)
df['income'] = pd.to_numeric(df['income'], errors='coerce').fillna(0)
df['world_rank'] = pd.to_numeric(df['world_rank'], errors='coerce').fillna(0)

# Группировка данных по годам
average_ranking = df.groupby('year')['world_rank'].mean().reset_index()
average_scores = df.groupby('year')[['teaching', 'research', 'citations', 'income']].mean().reset_index()

# Создание Dash приложения
layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H1("Анализ рейтингов университетов"),
            html.P("Анализ средних показателей университетов по годам."),
            html.P("Используйте фильтр, чтобы увидеть результат."),
            html.Hr(style={'color': 'black'}),
        ], style={'textAlign': 'center'})
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Выберите показатель:"),
            dbc.RadioItems(
                options=[
                    {'label': 'Средний мировой рейтинг', 'value': 'world_rank'},
                    {'label': 'Преподавание', 'value': 'teaching'},
                    {'label': 'Исследование', 'value': 'research'},
                    {'label': 'Цитирование', 'value': 'citations'},
                    {'label': 'Доход от индустрии', 'value': 'income'},
                ],
                value='world_rank',
                id='indicator-radioitems',
            ),
        ], width=3, style={'padding': '0px', 'margin-right': '0px'}),  # Убираем отступы

        dbc.Col([
            html.H3(id='graph-title', style={'textAlign': 'center'}),
            dcc.Graph(id='line-graph', config={'displayModeBar': False})
        ], width=9, style={'padding': '0px', 'margin-left': '0px'})  # Убираем отступы
    ], style={'margin': '0px'})  # Убираем отступы между строками
], fluid=True)

@callback(
    [Output('line-graph', 'figure'),
     Output('graph-title', 'children')],
    Input('indicator-radioitems', 'value')
)
def update_line_graph(indicator):
    if indicator == 'world_rank':
        title = 'Средний мировой рейтинг университетов по годам'
        fig = px.line(average_ranking, x='year', y='world_rank',
                      labels={'year': 'Год', 'world_rank': 'Мировой рейтинг'})
    else:
        indicator_labels = {
            'teaching': 'Преподавание',
            'research': 'Исследование',
            'citations': 'Цитирование',
            'income': 'Доход от индустрии'
        }
        title = f'Средний балл по критерию: {indicator_labels[indicator]} по годам'
        fig = px.line(average_scores, x='year', y=indicator,
                      labels={'year': 'Год', indicator: indicator_labels[indicator]})

    fig.update_traces(mode='lines', line=dict(width=4, color='green'))  # Утолщаем линии и меняем цвет на зеленый
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      showlegend=False)
    return fig, title

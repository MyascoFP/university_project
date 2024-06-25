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
df['num_students'] = df['num_students'].str.replace(',', '').astype(float)
df['international_students'] = df['international_students'].str.replace('%', '').astype(float)
df['student_staff_ratio'] = pd.to_numeric(df['student_staff_ratio'], errors='coerce').fillna(0)

# Группировка данных по годам
average_ranking = df.groupby('year')['world_rank'].mean().reset_index()
average_scores = df.groupby('year')[['teaching', 'research', 'citations', 'income']].mean().reset_index()
average_students = df.groupby('year')['num_students'].sum().reset_index()
average_international_students = df.groupby('year')['international_students'].mean().reset_index()
average_student_staff_ratio = df.groupby('year')['student_staff_ratio'].mean().reset_index()

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
                    {'label': 'Преподавание', 'value': 'teaching'},
                    {'label': 'Исследование', 'value': 'research'},
                    {'label': 'Цитирование', 'value': 'citations'},
                    {'label': 'Доход от индустрии', 'value': 'income'},
                    {'label': 'Количество студентов', 'value': 'num_students'},
                    {'label': 'Процент иностранных студентов', 'value': 'international_students'},
                    {'label': 'Отношение студентов к преподавателям', 'value': 'student_staff_ratio'},
                ],
                value='world_rank',
                id='indicator-radioitems',
            ),
        ], width=3),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='line-graph'), className="mb-4")
    ])
], fluid=True)


@callback(
    Output('line-graph', 'figure'),
    Input('indicator-radioitems', 'value')
)
def update_line_graph(indicator):
    if indicator == 'world_rank':
        fig = px.line(average_ranking, x='year', y='world_rank',
                      title='Средний мировой рейтинг университетов по годам')
    elif indicator in ['teaching', 'research', 'citations', 'income']:
        fig = px.line(average_scores, x='year', y=indicator,
                      title=f'Средний балл по критерию: {indicator.capitalize()} по годам')
    elif indicator == 'num_students':
        fig = px.line(average_students, x='year', y='num_students',
                      title='Количество студентов по годам')
    elif indicator == 'international_students':
        fig = px.line(average_international_students, x='year', y='international_students',
                      title='Средний процент иностранных студентов по годам')
    elif indicator == 'student_staff_ratio':
        fig = px.line(average_student_staff_ratio, x='year', y='student_staff_ratio',
                      title='Среднее отношение студентов к преподавателям по годам')

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      showlegend=True)
    return fig
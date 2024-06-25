from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from data import df


# Преобразование столбцов в числовой формат, обработка ошибок и пропусков
df['teaching'] = pd.to_numeric(df['teaching'], errors='coerce').fillna(0)
df['research'] = pd.to_numeric(df['research'], errors='coerce').fillna(0)
df['citations'] = pd.to_numeric(df['citations'], errors='coerce').fillna(0)
df['income'] = pd.to_numeric(df['income'], errors='coerce').fillna(0)
df['world_rank'] = pd.to_numeric(df['world_rank'], errors='coerce').fillna(0)

# Ensure 'female_male_ratio' is treated as a string before conversion
df[['female_percentage', 'male_percentage']] = df['female_male_ratio'].astype(str).str.split(' : ', expand=True)
df['female_percentage'] = pd.to_numeric(df['female_percentage'], errors='coerce')
df['male_percentage'] = pd.to_numeric(df['male_percentage'], errors='coerce')
df['female_percentage'] = df['female_percentage'] / (df['female_percentage'] + df['male_percentage']) * 100
df['male_percentage'] = 100 - df['female_percentage']

# Получение списка уникальных университетов
universities = df['university_name'].unique()

# Layout of the Dash app
layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H1("Анализ университетов по годам"),
            html.P("Выберите университет для анализа его мирового рейтинга и баллов по критериям."),
            html.Hr(style={'color': 'black'}),
        ], style={'textAlign': 'center'})
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Выберите университет:"),
            dcc.Dropdown(
                id='university-dropdown',
                options=[{'label': uni, 'value': uni} for uni in universities],
                value=universities[0]
            ),
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='line-graph-ranking', config={'displayModeBar': False}),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='line-graph-scores', config={'displayModeBar': False}),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph-students', config={'displayModeBar': False}),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph-gender-ratio', config={'displayModeBar': False}),
        ]),
    ]),
], fluid=True)


@callback(
    [Output('line-graph-ranking', 'figure'),
     Output('line-graph-scores', 'figure'),
     Output('bar-graph-students', 'figure'),
     Output('bar-graph-gender-ratio', 'figure')],
    [Input('university-dropdown', 'value')]
)
def update_graphs(selected_university):
    filtered_data = df[df['university_name'] == selected_university]

    # Line graph for world ranking
    ranking_fig = px.line(
        filtered_data,
        x='year',
        y='world_rank',
        title=f'Изменение мирового рейтинга университета {selected_university} по годам',
        labels={'year': 'Год', 'world_rank': 'Мировой рейтинг'},
    )
    ranking_fig.update_yaxes(autorange='reversed')

    # Line graph for scores
    scores_fig = px.line(
        filtered_data,
        x='year',
        y=['teaching', 'research', 'citations', 'income'],
        title=f'Изменение баллов по критериям для университета {selected_university} по годам',
        labels={'year': 'Год', 'value': 'Баллы', 'variable': 'Критерий'}
    )

    # Bar graph for number of students
    students_fig = px.bar(
        filtered_data,
        x='year',
        y='num_students',
        title=f'Количество студентов в университете {selected_university} по годам',
        labels={'year': 'Год', 'num_students': 'Количество студентов'}
    )

    # Stacked bar graph for gender ratio
    gender_ratio_fig = px.bar(
        filtered_data,
        x='year',
        y=['female_percentage', 'male_percentage'],
        title=f'Процент студентов по гендерному соотношению в университете {selected_university} по годам',
        labels={'year': 'Год', 'value': 'Процент', 'variable': 'Гендер'},
        barmode='stack'
    )

    ranking_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    scores_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    students_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    gender_ratio_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return ranking_fig, scores_fig, students_fig, gender_ratio_fig

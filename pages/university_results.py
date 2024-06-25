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

# Получение списка уникальных университетов
universities = df['university_name'].unique()

# Создание Dash приложения
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
], fluid=True)


@callback(
    [Output('line-graph-ranking', 'figure'),
     Output('line-graph-scores', 'figure')],
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
        labels={'year': 'Год', 'world_rank': 'Мировой рейтинг'}
    )

    # Line graph for scores
    scores_fig = px.line(
        filtered_data,
        x='year',
        y=['teaching', 'research', 'citations', 'income'],
        title=f'Изменение баллов по критериям для университета {selected_university} по годам',
        labels={'year': 'Год', 'value': 'Баллы', 'variable': 'Критерий'}
    )

    # Переводим критерии на русский
    criteria_labels = {
        'teaching': 'Преподавание',
        'research': 'Исследования',
        'citations': 'Цитирования',
        'income': 'Доход от индустрии'
    }
    
    # Обновляем линии графиков
    ranking_fig.update_traces(mode='lines', line=dict(width=4))  # Утолщаем линии и убираем маркеры
    scores_fig.update_traces(mode='lines', line=dict(width=4))  # Утолщаем линии и убираем маркеры

    # Обновляем оси графиков
    scores_fig.for_each_trace(lambda t: t.update(name=criteria_labels[t.name]))

    ranking_fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    scores_fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

    return ranking_fig, scores_fig


if __name__ == '__main__':
    app.run_server(debug=True)

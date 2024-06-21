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

# Получение списка уникальных университетов и стран
universities = df['university_name'].unique()
countries = df['country'].unique()


layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H1("Анализ критериев университетов"),
            html.P("Выберите университет или страну для анализа."),
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
                value=None,
                placeholder='Выберите университет'
            ),
            html.Br(),
            dbc.Label("Или выберите страну:"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in countries],
                value=None,
                placeholder='Выберите страну'
            ),
        ], width=6),

        dbc.Col([
            dbc.Label("Выберите критерии для диаграммы рассеяния:"),
            dcc.RadioItems(
                options=[
                    {'label': 'Преподавание и Исследование', 'value': 'teaching_research'},
                    {'label': 'Исследование и Цитирование', 'value': 'research_citations'},
                    {'label': 'Цитирование и Доход от индустрии', 'value': 'citations_income'},
                ],
                value='research_citations',
                id='scatter-criteria-radioitems',
            ),
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='radar-chart', config={'displayModeBar': False}),
        ], width=6),

        dbc.Col([
            dcc.Graph(id='histogram', config={'displayModeBar': False}),
        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='scatter-plot', config={'displayModeBar': False}),
        ]),
    ]),
], fluid=True)


@callback(
    [Output('radar-chart', 'figure'),
     Output('histogram', 'figure'),
     Output('scatter-plot', 'figure')],
    [Input('university-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('scatter-criteria-radioitems', 'value')]
)
def update_graphs(selected_university, selected_country, scatter_criteria):
    # Radar Chart
    if selected_university:
        radar_data = df[df['university_name'] == selected_university][['teaching', 'research', 'citations', 'income']].mean().reset_index()
        radar_data.columns = ['criteria', 'value']
        radar_fig = px.line_polar(
            radar_data,
            r='value',
            theta='criteria',
            line_close=True,
            title=f'Оценки по критериям для университета {selected_university}'
        )
    elif selected_country:
        radar_data = df[df['country'] == selected_country][['teaching', 'research', 'citations', 'income']].mean().reset_index()
        radar_data.columns = ['criteria', 'value']
        radar_fig = px.line_polar(
            radar_data,
            r='value',
            theta='criteria',
            line_close=True,
            title=f'Оценки по критериям для страны {selected_country}'
        )
    else:
        radar_fig = px.line_polar(title='Пожалуйста, выберите университет или страну')

    # Histogram
    histogram_fig = px.histogram(
        df,
        x='teaching',
        nbins=30,
        title='Распределение баллов по критериям: Преподавание'
    )
    histogram_fig.add_trace(px.histogram(df, x='research', nbins=30).data[0])
    histogram_fig.add_trace(px.histogram(df, x='citations', nbins=30).data[0])
    histogram_fig.add_trace(px.histogram(df, x='income', nbins=30).data[0])

    # Scatter Plot
    criteria_map = {
        'teaching_research': ('teaching', 'research'),
        'research_citations': ('research', 'citations'),
        'citations_income': ('citations', 'income')
    }
    x_criteria, y_criteria = criteria_map[scatter_criteria]

    scatter_fig = px.scatter(
        df,
        x=x_criteria,
        y=y_criteria,
        title=f'Взаимосвязь между {x_criteria.capitalize()} и {y_criteria.capitalize()}',
        labels={x_criteria: x_criteria.capitalize(), y_criteria: y_criteria.capitalize()}
    )

    radar_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    histogram_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    scatter_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return radar_fig, histogram_fig, scatter_fig
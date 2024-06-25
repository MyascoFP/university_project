from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from data import df


df['teaching'] = pd.to_numeric(df['teaching'], errors='coerce').fillna(0)
df['research'] = pd.to_numeric(df['research'], errors='coerce').fillna(0)
df['citations'] = pd.to_numeric(df['citations'], errors='coerce').fillna(0)
df['income'] = pd.to_numeric(df['income'], errors='coerce').fillna(0)
df['world_rank'] = pd.to_numeric(df['world_rank'], errors='coerce').fillna(0)

# Группировка данных по странам
average_ranking_by_country = df.groupby('country')['world_rank'].mean().reset_index()
average_scores_by_country = df.groupby('country')[['teaching', 'research', 'citations', 'income']].mean().reset_index()

layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H1("Сравнение стран по рейтингам университетов"),
            html.P("Анализ средних показателей университетов по странам."),
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
        ], width=3),

        dbc.Col([
            dcc.Graph(id='choropleth-map', config={'displayModeBar': False}),
        ], width=9)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-chart', config={'displayModeBar': False}),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='box-plot', config={'displayModeBar': False}),
        ]),
    ]),
], fluid=True)


@callback(
    [Output('choropleth-map', 'figure'),
     Output('bar-chart', 'figure'),
     Output('box-plot', 'figure')],
    [Input('indicator-radioitems', 'value')]
)
def update_graphs(indicator):
    # Choropleth Map
    choropleth_fig = px.choropleth(
        average_ranking_by_country if indicator == 'world_rank' else average_scores_by_country,
        locations='country',
        locationmode='country names',
        color=indicator,
        hover_name='country',
        color_continuous_scale=px.colors.sequential.Blues,
        title=f'Средний {indicator.capitalize()} университетов по странам'
    )

    # Bar Chart
    bar_fig = px.bar(
        average_scores_by_country,
        x='country',
        y=indicator,
        title=f'Средние баллы по критерию: {indicator.capitalize()} по странам',
        labels={indicator: indicator.capitalize(), 'country': 'Страна'}
    )

    # Box Plot
    box_fig = px.box(
        df,
        x='country',
        y='world_rank',
        title='Распределение мировых рейтингов университетов по странам',
        labels={'world_rank': 'Мировой рейтинг', 'country': 'Страна'}
    )

    choropleth_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    bar_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    box_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return choropleth_fig, bar_fig, box_fig
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from data import df


df['teaching'] = pd.to_numeric(df['teaching'], errors='coerce').fillna(0)
df['research'] = pd.to_numeric(df['research'], errors='coerce').fillna(0)
df['citations'] = pd.to_numeric(df['citations'], errors='coerce').fillna(0)
df['income'] = pd.to_numeric(df['income'], errors='coerce').fillna(0)
df['world_rank'] = pd.to_numeric(df['world_rank'], errors='coerce').fillna(0)

# Группировка данных по странам
average_ranking_by_country = df.groupby('country')['world_rank'].mean().reset_index()
average_scores_by_country = df.groupby('country')[['teaching', 'research', 'citations', 'income']].mean().reset_index()

layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H1("Сравнение стран по рейтингам университетов"),
            html.P("Анализ средних показателей университетов по странам."),
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
                ],
                value='world_rank',
                id='indicator-radioitems',
            ),
        ], width=3),

        dbc.Col([
            dcc.Graph(id='choropleth-map', config={'displayModeBar': False}),
        ], width=9)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-chart', config={'displayModeBar': False}),
        ]),
    ]),
], fluid=True)


@callback(
    [Output('choropleth-map', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('indicator-radioitems', 'value')]
)
def update_graphs(indicator):
    # Choropleth Map
    choropleth_fig = px.choropleth(
        average_ranking_by_country if indicator == 'world_rank' else average_scores_by_country,
        locations='country',
        locationmode='country names',
        color=indicator,
        hover_name='country',
        color_continuous_scale=px.colors.sequential.Blues,
        title=f'Средний {indicator.capitalize()} университетов по странам'
    )

    # Bar Chart
    bar_fig = px.bar(
        average_scores_by_country,
        x='country',
        y=indicator,
        title=f'Средние баллы по критерию: {indicator.capitalize()} по странам',
        labels={indicator: indicator.capitalize(), 'country': 'Страна'}
    )

    choropleth_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    bar_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return choropleth_fig, bar_fig
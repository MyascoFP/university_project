from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from data import df


# Преобразование столбцов в числовой формат, удаляя запятые и символы '%'
def clean_column(column):
    if isinstance(column, str):
        column = column.replace(',', '').replace('%', '')
    return pd.to_numeric(column, errors='coerce')

additional_columns = ['num_students', 'student_staff_ratio', 'international_students']
for column in additional_columns:
    df[column] = df[column].apply(clean_column)


# Предобработка данных
df['teaching'] = pd.to_numeric(df['teaching'], errors='coerce')
df['research'] = pd.to_numeric(df['research'], errors='coerce')
df['citations'] = pd.to_numeric(df['citations'], errors='coerce')
df['income'] = pd.to_numeric(df['income'], errors='coerce')

# Создание списка уникальных университетов
universities = df['university_name'].unique()
years = df['year'].unique()

# Группировка данных по годам
average_ranking = df.groupby('year')['world_rank'].mean().reset_index()
average_scores = df.groupby('year')[['teaching', 'research', 'citations', 'income']].mean().reset_index()


layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Анализ рейтингов университетов"), className="mb-2")
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='university-dropdown',
            options=[{'label': uni, 'value': uni} for uni in universities],
            value=[universities[0]],
            multi=True
        ), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in years],
            value=years[0],
            clearable=False
        ), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(
            id='average-world-ranking',
            figure=px.line(average_ranking, x='year', y='world_rank', title='Средний мировой рейтинг университетов по годам')
        ), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(
            id='average-scores',
            figure=px.line(average_scores, x='year', y=['teaching', 'research', 'citations', 'income'],
                           title='Средние баллы по критериям по годам')
        ), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='ranking-comparison'), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='criteria-comparison'), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='grouped-bar-comparison'), className="mb-4")
    ])
], fluid=True)

@callback(
    [Output('criteria-comparison', 'figure'),
     Output('ranking-comparison', 'figure'),
     Output('grouped-bar-comparison', 'figure')],
    [Input('university-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_graphs(selected_universities, selected_year):
    filtered_data = df[(df['university_name'].isin(selected_universities)) & (df['year'] == selected_year)]
    filtered_data_1 = df[(df['university_name'].isin(selected_universities))]

    # Удаление строк с пропущенными значениями для выбранных университетов
    filtered_data = filtered_data.dropna(subset=additional_columns)

    # Проверка, что после фильтрации остались данные
    if filtered_data.empty:
        return {}, {}, {}

    # Гистограмма: Сравнение баллов по критериям для выбранных университетов
    criteria_comparison = px.bar(filtered_data, x='university_name', y=['teaching', 'research', 'citations', 'income'],
                                 barmode='group', title=f'Сравнение баллов по критериям для выбранных университетов ({selected_year})')

    # Линейный график: Сравнение изменения мирового рейтинга для нескольких университетов по годам
    ranking_comparison = px.line(filtered_data_1, x='year', y='world_rank', color='university_name',
                                 title='Сравнение изменения мирового рейтинга для нескольких университетов по годам')

    # Группированный столбчатый график: Сравнение численности студентов, соотношения студентов и преподавателей и процента иностранных студентов для выбранных университетов
    grouped_bar_comparison = px.bar(filtered_data, x='university_name', y=['num_students', 'student_staff_ratio', 'international_students'],
                                    barmode='group', title=f'Сравнение численности студентов, соотношения студентов и преподавателей и процента иностранных студентов для выбранных университетов ({selected_year})')

    return criteria_comparison, ranking_comparison, grouped_bar_comparison
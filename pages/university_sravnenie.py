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
average_scores = df.groupby('year')[['teaching', 'research', 'citations', 'income']].mean().reset_index()

# Переводим критерии на русский
criteria_labels = {
    'teaching': 'Преподавание',
    'research': 'Исследования',
    'citations': 'Цитирования',
    'income': 'Доход от индустрии'
}

# Создаем график средних баллов по критериям по годам с переводом на русский
average_scores_fig = px.line(
    average_scores, 
    x='year', 
    y=['teaching', 'research', 'citations', 'income'],
    title='Средние баллы по критериям по годам',
    labels={'year': 'Год', 'value': 'Баллы', 'variable': 'Критерий'}
)
average_scores_fig.for_each_trace(lambda t: t.update(name=criteria_labels[t.name]))

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
            id='average-scores',
            figure=average_scores_fig
        ), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='ranking-comparison'), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='criteria-comparison'), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='student-count-comparison'), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='additional-bar-comparison'), className="mb-4")
    ])
], fluid=True)

@callback(
    [Output('criteria-comparison', 'figure'),
     Output('ranking-comparison', 'figure'),
     Output('student-count-comparison', 'figure'),
     Output('additional-bar-comparison', 'figure')],
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
        return {}, {}, {}, {}

    # Переводим критерии на русский
    criteria_labels = {
        'teaching': 'Преподавание',
        'research': 'Исследования',
        'citations': 'Цитирования',
        'income': 'Доход от индустрии'
    }

    additional_labels = {
        'num_students': 'Число студентов',
        'student_staff_ratio': 'Соотношение студентов и преподавателей',
        'international_students': 'Процент иностранных студентов'
    }

    # Гистограмма: Сравнение баллов по критериям для выбранных университетов
    criteria_comparison = px.bar(
        filtered_data, 
        x='university_name', 
        y=['teaching', 'research', 'citations', 'income'],
        barmode='group', 
        title=f'Сравнение баллов по критериям для выбранных университетов ({selected_year})',
        labels={'variable': 'Критерий', 'value': 'Баллы', 'university_name': 'Университет'}
    )
    
    criteria_comparison.for_each_trace(lambda t: t.update(name=criteria_labels[t.name]))

    # Линейный график: Сравнение изменения мирового рейтинга для нескольких университетов по годам
    ranking_comparison = px.line(
        filtered_data_1, 
        x='year', 
        y='world_rank', 
        color='university_name',
        title='Сравнение изменения мирового рейтинга для нескольких университетов по годам',
        labels={'year': 'Год', 'world_rank': 'Мировой рейтинг', 'university_name': 'Университет'}
    )

    ranking_comparison.update_traces(mode='lines', line=dict(width=4))

    # Столбчатый график: Сравнение численности студентов для выбранных университетов
    student_count_comparison = px.bar(
        filtered_data, 
        x='university_name', 
        y='num_students',
        title=f'Сравнение численности студентов для выбранных университетов ({selected_year})',
        labels={'num_students': 'Число студентов', 'university_name': 'Университет'},
        text='num_students'
    )

    student_count_comparison.update_traces(marker_line_width=1.5, marker_line_color="black", width=0.3)  # Уменьшаем ширину столбцов

    # Столбчатый график: Сравнение соотношения студентов и преподавателей и процента иностранных студентов для выбранных университетов
    additional_bar_comparison = px.bar(
        filtered_data, 
        x='university_name', 
        y=['student_staff_ratio', 'international_students'],
        barmode='group', 
        title=f'Сравнение соотношения студентов и преподавателей и процента иностранных студентов для выбранных университетов ({selected_year})',
        labels={'variable': 'Показатель', 'value': 'Значение', 'university_name': 'Университет'}
    )

    additional_bar_comparison.for_each_trace(lambda t: t.update(name=additional_labels[t.name]))
    additional_bar_comparison.update_traces(marker_line_width=1.5, marker_line_color="black", width=0.3)  # Уменьшаем ширину столбцов

    # Обновление макетов графиков
    criteria_comparison.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    ranking_comparison.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    student_count_comparison.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    additional_bar_comparison.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

    return criteria_comparison, ranking_comparison, student_count_comparison, additional_bar_comparison


if __name__ == '__main__':
    app.run_server(debug=True)

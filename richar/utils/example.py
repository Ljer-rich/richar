import pandas as pd
import numpy as np
from chart_utils import (
    DataProcessor, ChartGenerator, ChartConfig, 
    ChartData, SeriesData
)

# 创建示例数据
data = pd.DataFrame({
    'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
    'sales': [100, np.nan, 300, 400, 500],
    'profit': [20, 30, np.nan, 80, 100],
    'category': ['A', 'B', 'C', 'A', 'B']
})

# 1. 数据处理示例
processor = DataProcessor()

# 处理缺失值
cleaned_data = processor.handle_missing_values(data, method='fill', fill_value=0)

# 标准化数值列
normalized_data = processor.normalize_data(
    cleaned_data,
    columns=['sales', 'profit'],
    method='minmax'
)

# 格式化日期
formatted_data = processor.format_datetime(
    normalized_data,
    datetime_columns=['date']
)

# 2. 图表生成示例
chart_gen = ChartGenerator()

# 生成基础柱状图
sales_series = SeriesData(name='销售额', data=formatted_data['sales'].tolist())
profit_series = SeriesData(name='利润', data=formatted_data['profit'].tolist())
bar_data = ChartData(
    x_data=formatted_data['date'].tolist(),
    series=[sales_series, profit_series]
)

bar_chart = chart_gen.generate_basic_chart(
    chart_type='bar',
    data=bar_data,
    title='销售数据分析',
    subtitle='销售额和利润对比'
)

# 生成自定义复杂图表
custom_config = ChartConfig(
    title={
        'text': '销售数据多维分析',
        'subtext': '包含多个维度的数据展示'
    },
    tooltip={'trigger': 'axis'},
    legend={'data': ['销售额', '利润']},
    xAxis={
        'type': 'category',
        'data': formatted_data['date'].tolist()
    },
    yAxis=[
        {
            'type': 'value',
            'name': '销售额',
            'position': 'left'
        },
        {
            'type': 'value',
            'name': '利润',
            'position': 'right'
        }
    ],
    series=[
        {
            'name': '销售额',
            'type': 'bar',
            'data': formatted_data['sales'].tolist()
        },
        {
            'name': '利润',
            'type': 'line',
            'yAxisIndex': 1,
            'data': formatted_data['profit'].tolist()
        }
    ]
)

custom_chart = chart_gen.generate_custom_chart(custom_config)

# 保存图表配置
chart_gen.save_chart_config(bar_chart, 'sales_bar_chart.json')
chart_gen.save_chart_config(custom_chart, 'sales_custom_chart.json')

print("数据处理和图表生成完成！")

from dataclasses import dataclass
from typing import Any
import pandas as pd
import numpy as np
import json

@dataclass
class SeriesData:
    name: str
    data: list[float | int]

@dataclass
class ChartData:
    x_data: list[str]
    series: list[SeriesData]

@dataclass
class PieData:
    name: str
    data: list[dict[str, Any]]

@dataclass
class ChartConfig:
    title: dict[str, str]
    tooltip: dict[str, str]
    legend: dict[str, list[str]]
    xAxis: dict[str, Any]
    yAxis: dict[str, Any] | list[dict[str, Any]]
    series: list[dict[str, Any]]

class DataProcessor:
    """数据处理工具类"""
    
    @staticmethod
    def handle_missing_values(
        data: pd.DataFrame,
        method: str,  # 'drop' | 'fill'
        fill_value: str | int | float | None = None
    ) -> pd.DataFrame:
        """
        处理缺失值
        :param data: 输入的DataFrame
        :param method: 处理方法 ('drop'删除, 'fill'填充)
        :param fill_value: 填充值
        :return: 处理后的DataFrame
        """
        match method:
            case 'drop':
                return data.dropna()
            case 'fill':
                return data.fillna(fill_value)
            case _:
                raise ValueError("method must be 'drop' or 'fill'")

    @staticmethod
    def normalize_data(
        data: pd.DataFrame,
        columns: list[str],
        method: str  # 'minmax' | 'zscore'
    ) -> pd.DataFrame:
        """
        数据标准化
        :param data: 输入的DataFrame
        :param columns: 需要标准化的列
        :param method: 标准化方法 ('minmax'最小最大化, 'zscore'z-score标准化)
        :return: 标准化后的DataFrame
        """
        result = data.copy()
        
        for col in columns:
            match method:
                case 'minmax':
                    min_val = data[col].min()
                    max_val = data[col].max()
                    result[col] = (data[col] - min_val) / (max_val - min_val)
                case 'zscore':
                    mean = data[col].mean()
                    std = data[col].std()
                    result[col] = (data[col] - mean) / std
                
        return result

    @staticmethod
    def format_datetime(
        data: pd.DataFrame,
        datetime_columns: list[str],
        format: str = '%Y-%m-%d'
    ) -> pd.DataFrame:
        """
        格式化日期时间
        :param data: 输入的DataFrame
        :param datetime_columns: 需要格式化的日期时间列
        :param format: 日期格式
        :return: 处理后的DataFrame
        """
        result = data.copy()
        for col in datetime_columns:
            result[col] = pd.to_datetime(data[col]).dt.strftime(format)
        return result

class ChartGenerator:
    """图表生成工具类"""
    
    @staticmethod
    def generate_basic_chart(
        chart_type: str,  # 'bar' | 'line' | 'pie'
        data: ChartData | PieData,
        title: str = '',
        subtitle: str = ''
    ) -> ChartConfig:
        """
        生成基础图表配置
        :param chart_type: 图表类型 ('bar'柱状图, 'line'折线图, 'pie'饼图)
        :param data: 图表数据
        :param title: 图表标题
        :param subtitle: 图表副标题
        :return: ECharts配置字典
        """
        base_option = ChartConfig(
            title={'text': title, 'subtext': subtitle},
            tooltip={'trigger': 'axis' if chart_type != 'pie' else 'item'},
            legend={'data': []},
            xAxis={},
            yAxis={},
            series=[]
        )

        match chart_type:
            case 'bar' | 'line':
                chart_data = data if isinstance(data, ChartData) else ChartData(x_data=[], series=[])
                base_option.xAxis = {
                    'type': 'category',
                    'data': chart_data.x_data
                }
                base_option.yAxis = {
                    'type': 'value'
                }
                base_option.series = [
                    {
                        'name': series.name,
                        'type': chart_type,
                        'data': series.data
                    } for series in chart_data.series
                ]
            
            case 'pie':
                pie_data = data if isinstance(data, PieData) else PieData(name='', data=[])
                base_option.series = [{
                    'name': pie_data.name,
                    'type': 'pie',
                    'radius': '50%',
                    'data': pie_data.data
                }]

        return base_option

    @staticmethod
    def generate_custom_chart(config: ChartConfig) -> ChartConfig:
        """
        生成自定义图表配置
        :param config: 完整的ECharts配置
        :return: ECharts配置字典
        """
        return config

    @staticmethod
    def save_chart_config(config: ChartConfig, file_path: str) -> None:
        """
        保存图表配置到文件
        :param config: ECharts配置
        :param file_path: 保存路径
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(vars(config), f, ensure_ascii=False, indent=2)

# 使用示例
if __name__ == '__main__':
    # 数据处理示例
    data = pd.DataFrame({
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'value': [100, np.nan, 300],
        'category': ['A', 'B', 'C']
    })
    
    processor = DataProcessor()
    # 处理缺失值
    cleaned_data = processor.handle_missing_values(data, method='fill', fill_value=0)
    
    # 生成图表示例
    chart_gen = ChartGenerator()
    
    # 生成基础柱状图
    series_data = SeriesData(name='数值', data=cleaned_data['value'].tolist())
    chart_data = ChartData(
        x_data=cleaned_data['date'].tolist(),
        series=[series_data]
    )
    
    basic_chart = chart_gen.generate_basic_chart(
        chart_type='bar',
        data=chart_data,
        title='示例图表',
        subtitle='数据展示'
    )
    
    # 生成自定义图表
    custom_config = ChartConfig(
        title={'text': '自定义图表'},
        tooltip={'trigger': 'axis'},
        legend={'data': []},
        xAxis={
            'type': 'category',
            'data': cleaned_data['date'].tolist()
        },
        yAxis={'type': 'value'},
        series=[{
            'type': 'bar',
            'data': cleaned_data['value'].tolist()
        }]
    )
    
    custom_chart = chart_gen.generate_custom_chart(custom_config)
    
    # 保存图表配置
    chart_gen.save_chart_config(basic_chart, 'basic_chart.json')
    chart_gen.save_chart_config(custom_chart, 'custom_chart.json')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read and analyze Agentic AI Performance Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

def load_excel_data(file_path):
    """Load Excel data and return DataFrame with record count"""
    try:
        # Read Excel file - column names are in row 1 (index 1), data starts from row 2
        df = pd.read_excel(file_path, header=1)
        record_count = len(df)
        print(f"Successfully loaded {record_count} records")
        return df, record_count
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None, 0

def analyze_question1(df):
    """Analyze agent_type multimodal capability percentage"""
    # Check if required columns exist
    if 'agent_type' not in df.columns or 'multimodal_capability' not in df.columns:
        print("Missing required columns for Question 1")
        return None

    # Group by agent_type and calculate multimodal percentage
    result = df.groupby('agent_type').agg(
        total_count=('multimodal_capability', 'count'),
        multimodal_count=('multimodal_capability', lambda x: (x == True).sum() if x.dtype == bool else (x == 'Yes').sum() if x.dtype == object else x.sum())
    )

    result['multimodal_percentage'] = (result['multimodal_count'] / result['total_count'] * 100).round(2)
    result = result.sort_values('multimodal_percentage', ascending=False)

    return result.head(3)

def analyze_question2(df):
    """Analyze model_architecture multimodal capability percentage"""
    # Check if required columns exist
    if 'model_architecture' not in df.columns or 'multimodal_capability' not in df.columns:
        print("Missing required columns for Question 2")
        return None

    # Group by model_architecture and calculate multimodal percentage
    result = df.groupby('model_architecture').agg(
        total_count=('multimodal_capability', 'count'),
        multimodal_count=('multimodal_capability', lambda x: (x == True).sum() if x.dtype == bool else (x == 'Yes').sum() if x.dtype == object else x.sum())
    )

    result['multimodal_percentage'] = (result['multimodal_count'] / result['total_count'] * 100).round(2)
    result = result.sort_values('multimodal_percentage', ascending=False)

    return result.head(3)

def analyze_question3(df):
    """Analyze task_category bias detection median"""
    # Check if required columns exist
    if 'task_category' not in df.columns or 'bias_detection_score' not in df.columns:
        print("Missing required columns for Question 3")
        return None

    # Group by task_category and calculate median bias detection
    result = df.groupby('task_category').agg(
        median_bias=('bias_detection_score', 'median')
    ).round(2)

    result = result.sort_values('median_bias', ascending=False)

    return result.head(3)

def create_chart_base64(fig):
    """Convert matplotlib figure to base64 string"""
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_str

def generate_visualizations(df, results_q1, results_q2, results_q3):
    """Generate all required visualizations"""
    charts = {}

    # Chart 1: Agent Type Multimodal Percentage
    if results_q1 is not None and not results_q1.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#FF9AA2', '#FFB7B2', '#FFDAC1']
        results_q1['multimodal_percentage'].plot(kind='barh', color=colors, ax=ax)
        ax.set_xlabel('Multimodal Percentage (%)')
        ax.set_title('Top 3 Agent Types by Multimodal Capability Percentage')
        ax.invert_yaxis()
        charts['q1_chart'] = create_chart_base64(fig)

    # Chart 2: Model Architecture Multimodal Percentage
    if results_q2 is not None and not results_q2.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#E2F0CB', '#B5EAD7', '#C7CEEA']
        results_q2['multimodal_percentage'].plot(kind='barh', color=colors, ax=ax)
        ax.set_xlabel('Multimodal Percentage (%)')
        ax.set_title('Top 3 Model Architectures by Multimodal Capability Percentage')
        ax.invert_yaxis()
        charts['q2_chart'] = create_chart_base64(fig)

    # Chart 3: Task Category Bias Detection Median
    if results_q3 is not None and not results_q3.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#FFD700', '#87CEEB', '#98FB98']
        results_q3['median_bias'].plot(kind='barh', color=colors, ax=ax)
        ax.set_xlabel('Median Bias Detection Score')
        ax.set_title('Top 3 Task Categories by Median Bias Detection Score')
        ax.invert_yaxis()
        charts['q3_chart'] = create_chart_base64(fig)

    return charts

def generate_html_dashboard(results_q1, results_q2, results_q3, charts, record_count):
    """Generate comprehensive HTML dashboard"""

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic AI Performance Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
        }}
        .section {{
            margin-bottom: 40px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 5px solid #667eea;
        }}
        .chart-container {{
            text-align: center;
            margin: 20px 0;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        th, td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .record-count {{
            background: #28a745;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            display: inline-block;
            margin: 10px 0;
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            .section {{
                padding: 15px;
            }}
            th, td {{
                padding: 10px;
                font-size: 14px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Agentic AI Performance Dashboard</h1>
            <p>Comprehensive analysis of AI agent performance metrics</p>
            <div class="record-count">
                📊 Total Records Processed: <strong>{record_count}</strong>
            </div>
        </div>

        <div class="section">
            <h2>📈 1. Agent Types with Highest Multimodal Capability</h2>
            <div class="chart-container">
                <img src="data:image/png;base64,{charts.get('q1_chart', '')}" alt="Agent Type Multimodal Analysis">
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Agent Type</th>
                        <th>Total Count</th>
                        <th>Multimodal Count</th>
                        <th>Percentage (%)</th>
                    </tr>
                </thead>
                <tbody>
"""

    # Add Q1 results to table
    if results_q1 is not None and not results_q1.empty:
        for agent_type, row in results_q1.iterrows():
            html_template += f"""                    <tr>
                        <td>{agent_type}</td>
                        <td>{int(row['total_count'])}</td>
                        <td>{int(row['multimodal_count'])}</td>
                        <td>{row['multimodal_percentage']}%</td>
                    </tr>
"""

    html_template += """                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>🏗️ 2. Model Architectures with Highest Multimodal Capability</h2>
            <div class="chart-container">
                <img src="data:image/png;base64,""" + charts.get('q2_chart', '') + """" alt="Model Architecture Multimodal Analysis">
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Model Architecture</th>
                        <th>Total Count</th>
                        <th>Multimodal Count</th>
                        <th>Percentage (%)</th>
                    </tr>
                </thead>
                <tbody>
"""

    # Add Q2 results to table
    if results_q2 is not None and not results_q2.empty:
        for architecture, row in results_q2.iterrows():
            html_template += f"""                    <tr>
                        <td>{architecture}</td>
                        <td>{int(row['total_count'])}</td>
                        <td>{int(row['multimodal_count'])}</td>
                        <td>{row['multimodal_percentage']}%</td>
                    </tr>
"""

    html_template += """                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>⚖️ 3. Task Categories with Highest Bias Detection Scores</h2>
            <div class="chart-container">
                <img src="data:image/png;base64,""" + charts.get('q3_chart', '') + """" alt="Task Category Bias Analysis">
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Task Category</th>
                        <th>Median Bias Detection Score</th>
                    </tr>
                </thead>
                <tbody>
"""

    # Add Q3 results to table
    if results_q3 is not None and not results_q3.empty:
        for task_category, row in results_q3.iterrows():
            html_template += f"""                    <tr>
                        <td>{task_category}</td>
                        <td>{row['median_bias']}</td>
                    </tr>
"""

    html_template += """                </tbody>
            </table>
        </div>

        <div style="text-align: center; margin-top: 40px; color: #666; font-size: 14px;">
            <p>Generated from Agentic AI Performance Dataset 2025 | Dashboard created with Python & Matplotlib</p>
        </div>
    </div>
</body>
</html>"""

    return html_template

def main():
    """Main function to orchestrate the analysis"""
    excel_file = "first-80-rows-agentic_ai_performance_dataset_20250622.xlsx"

    # Load data
    df, record_count = load_excel_data(excel_file)

    if df is None:
        print("Failed to load data. Exiting.")
        return

    print(f"Dataset columns: {list(df.columns)}")
    print(f"First few rows:\n{df.head()}")

    # Perform analyses
    print("\n=== Analyzing Question 1 ===")
    results_q1 = analyze_question1(df)
    print("Top 3 Agent Types by Multimodal Percentage:")
    print(results_q1)

    print("\n=== Analyzing Question 2 ===")
    results_q2 = analyze_question2(df)
    print("Top 3 Model Architectures by Multimodal Percentage:")
    print(results_q2)

    print("\n=== Analyzing Question 3 ===")
    results_q3 = analyze_question3(df)
    print("Top 3 Task Categories by Median Bias Detection:")
    print(results_q3)

    # Generate visualizations
    print("\n=== Generating Visualizations ===")
    charts = generate_visualizations(df, results_q1, results_q2, results_q3)

    # Generate HTML dashboard
    print("\n=== Generating HTML Dashboard ===")
    html_content = generate_html_dashboard(results_q1, results_q2, results_q3, charts, record_count)

    # Save HTML file
    with open('data-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\nDashboard saved as 'data-dashboard.html'")
    print(f"Total records processed: {record_count}")
    print("Analysis complete!")

if __name__ == "__main__":
    main()
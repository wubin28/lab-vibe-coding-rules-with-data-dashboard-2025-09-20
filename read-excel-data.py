import pandas as pd
import json

def load_excel_data():
    """Load Excel data and return pandas DataFrame"""
    try:
        df = pd.read_excel('first-80-rows-agentic_ai_performance_dataset_20250622.xlsx', header=1)
        print(f"Successfully loaded {len(df)} records from Excel file")
        return df
    except FileNotFoundError:
        print("Error: Excel file not found")
        return None
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def analyze_agent_type_multimodal(df):
    """Calculate top 3 agent types by multimodal capability percentage"""
    if df is None:
        return None

    # Group by agent_type and calculate multimodal percentage
    agent_stats = df.groupby('agent_type').agg({
        'multimodal_capability': ['count', 'sum']
    }).round(2)

    # Flatten column names
    agent_stats.columns = ['total', 'multimodal_count']

    # Calculate percentage
    agent_stats['multimodal_percentage'] = (agent_stats['multimodal_count'] / agent_stats['total'] * 100).round(2)

    # Get top 3
    top_3 = agent_stats.nlargest(3, 'multimodal_percentage')

    print("\nTop 3 Agent Types by Multimodal Capability Percentage:")
    for i, (agent_type, row) in enumerate(top_3.iterrows(), 1):
        print(f"{i}. {agent_type}: {row['multimodal_percentage']:.2f}% ({int(row['multimodal_count'])}/{int(row['total'])})")

    return top_3

def analyze_model_architecture_multimodal(df):
    """Calculate top 3 model architectures by multimodal capability percentage"""
    if df is None:
        return None

    # Group by model_architecture and calculate multimodal percentage
    model_stats = df.groupby('model_architecture').agg({
        'multimodal_capability': ['count', 'sum']
    }).round(2)

    # Flatten column names
    model_stats.columns = ['total', 'multimodal_count']

    # Calculate percentage
    model_stats['multimodal_percentage'] = (model_stats['multimodal_count'] / model_stats['total'] * 100).round(2)

    # Get top 3
    top_3 = model_stats.nlargest(3, 'multimodal_percentage')

    print("\nTop 3 Model Architectures by Multimodal Capability Percentage:")
    for i, (model_arch, row) in enumerate(top_3.iterrows(), 1):
        print(f"{i}. {model_arch}: {row['multimodal_percentage']:.2f}% ({int(row['multimodal_count'])}/{int(row['total'])})")

    return top_3

def analyze_task_category_bias(df):
    """Calculate top 3 task categories by median bias detection score"""
    if df is None:
        return None

    # Group by task_category and calculate median bias detection score
    bias_stats = df.groupby('task_category').agg({
        'bias_detection_score': ['count', 'median', 'mean']
    }).round(4)

    # Flatten column names
    bias_stats.columns = ['count', 'median_bias', 'mean_bias']

    # Get top 3 by median
    top_3 = bias_stats.nlargest(3, 'median_bias')

    print("\nTop 3 Task Categories by Median Bias Detection Score:")
    for i, (task_cat, row) in enumerate(top_3.iterrows(), 1):
        print(f"{i}. {task_cat}: {row['median_bias']:.4f} (n={int(row['count'])}, mean={row['mean_bias']:.4f})")

    return top_3

def generate_dashboard_data(agent_results, model_results, bias_results, total_records):
    """Format all analysis results for HTML dashboard embedding"""
    if agent_results is None or model_results is None or bias_results is None:
        return None

    dashboard_data = {
        "totalRecords": total_records,
        "processedRecords": total_records,
        "agentTypeData": {
            "labels": list(agent_results.index),
            "values": list(agent_results['multimodal_percentage'])
        },
        "modelArchitectureData": {
            "labels": list(model_results.index),
            "values": list(model_results['multimodal_percentage'])
        },
        "taskCategoryData": {
            "labels": list(bias_results.index),
            "values": list(bias_results['median_bias'])
        }
    }

    print("\nDashboard Data Generated:")
    print(json.dumps(dashboard_data, indent=2))

    return dashboard_data

if __name__ == "__main__":
    print("Agentic AI Performance Dataset Analysis")
    print("=" * 40)

    # Load data
    df = load_excel_data()
    if df is None:
        print("Failed to load data. Exiting.")
        exit(1)

    # Run all analyses
    agent_results = analyze_agent_type_multimodal(df)
    model_results = analyze_model_architecture_multimodal(df)
    bias_results = analyze_task_category_bias(df)

    # Generate dashboard data
    dashboard_data = generate_dashboard_data(agent_results, model_results, bias_results, len(df))

    print(f"\nAnalysis completed successfully for {len(df)} records.")
    print("Dashboard data is ready for HTML embedding.")
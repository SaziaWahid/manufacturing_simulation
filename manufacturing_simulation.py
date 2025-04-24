
# manufacturing_simulation.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import datetime

# 1. Data Import and Cleaning
def load_and_clean_data(filepath):
    df = pd.read_csv(filepath)
    
    # Handle missing values
    df.fillna(method='ffill', inplace=True)
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Basic outlier handling: clip values using IQR
    for col in df.select_dtypes(include=np.number).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df[col] = df[col].clip(lower, upper)
    return df

# 2. Cycle Time Calculation
def calculate_cycle_times(df, start_col='Start_Time', end_col='End_Time'):
    df[start_col] = pd.to_datetime(df[start_col])
    df[end_col] = pd.to_datetime(df[end_col])
    df['Cycle_Time'] = (df[end_col] - df[start_col]).dt.total_seconds() / 60.0
    return df

# 3. Bottleneck Identification
def identify_bottlenecks(df, stage_col='Stage', cycle_time_col='Cycle_Time'):
    avg_cycle_times = df.groupby(stage_col)[cycle_time_col].mean().sort_values(ascending=False)
    bottlenecks = avg_cycle_times.head()
    return bottlenecks

# 4. Optimization Recommendations
def recommend_optimizations(bottlenecks):
    recommendations = {}
    for stage, time in bottlenecks.items():
        recommendations[stage] = f"Consider redistributing workload or adding resources to reduce average cycle time ({time:.2f} mins)."
    return recommendations

# 5. Visualization
def plot_gantt_chart(df):
    df['Task'] = df['Stage'] + ": " + df['Product_ID'].astype(str)
    fig = ff.create_gantt(df, index_col='Stage', show_colorbar=True, group_tasks=True,
                          title="Production Timeline - Gantt Chart", showgrid_x=True, showgrid_y=True)
    fig.show()

def plot_heatmap(df, stage_col='Stage', cycle_time_col='Cycle_Time'):
    pivot = df.pivot_table(index=stage_col, values=cycle_time_col, aggfunc='mean')
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, cmap='coolwarm')
    plt.title("Average Cycle Time by Stage - Heatmap")
    plt.show()

# Main execution
if __name__ == "__main__":
    filepath = 'Sazia_Wahid_Manufacturing_Process_Simulation_and_Optimization (1).csv'
    df = load_and_clean_data(filepath)
    df = calculate_cycle_times(df)

    bottlenecks = identify_bottlenecks(df)
    print("\nTop Bottlenecks:")
    print(bottlenecks)

    recommendations = recommend_optimizations(bottlenecks)
    print("\nOptimization Recommendations:")
    for stage, rec in recommendations.items():
        print(f"- {stage}: {rec}")

    # Visualizations
    plot_gantt_chart(df)
    plot_heatmap(df)

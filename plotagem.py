import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

df = pd.read_csv('output\portfolio_solutions_20241121_035327.csv')

def plot_pareto_3d(df, x_col, y_col, z_col):
    df_sorted = df.sort_values(by='Score', ascending=False)
    
    df_sorted['Cumulative'] = df_sorted['Score'].cumsum() / df_sorted['Score'].sum()

    x = df_sorted[x_col]
    y = df_sorted[y_col]
    z = df_sorted[z_col]
    cumulative = df_sorted['Cumulative']
    
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    scatter = ax.scatter(x, y, z, c=cumulative, cmap='viridis', s=50)
    
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_zlabel(z_col)
    ax.set_title(f'Gráfico de Pareto 3D ({x_col}, {y_col}, {z_col})')

    fig.colorbar(scatter, ax=ax, label='Soma Cumulativa')

    plt.tight_layout()
    plt.show()

def print_top_3_with_allocations_and_save(df):
    df_sorted = df.sort_values(by='Score', ascending=False)
    
    top_3 = df_sorted.head(3)
    
    top_3_data = []

    for index, row in top_3.iterrows():
        allocations_str = row['Allocations']
        allocations = [float(x.strip()) for x in allocations_str.strip('[]').split(',')]
        
        allocations_percentage = [alloc * 100 for alloc in allocations]
        
        top_3_data.append({
            'ID': row['ID'],
            'Return': row['Return'],
            'Risk': row['Risk'],
            'Diversification': row['Diversification'],
            'Allocations (%)': allocations_percentage,
            'Score': row['Score']
        })
        
        print(f"ID: {row['ID']}")
        print(f"Return: {row['Return']:.6f}")
        print(f"Risk: {row['Risk']:.6f}")
        print(f"Diversification: {row['Diversification']:.6f}")
        print(f"Score: {row['Score']:.6f}")
        print("Alocações (%):")
        for i, alloc in enumerate(allocations_percentage):
            print(f"  Alocação {i + 1}: {alloc:.2f}%")  # Agora é possível formatar corretamente
        print("-" * 30)
    
    top_3_df = pd.DataFrame(top_3_data)
    
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f'output/top_3_allocations_{current_time}.csv'
    
    top_3_df.to_csv(file_name, index=False)
    print(f"Arquivo salvo como {file_name}")

# imprimir os 3 melhores resultados com as alocações e salvar
print_top_3_with_allocations_and_save(df)

# Gerar o gráfico de Pareto 3D
plot_pareto_3d(df, 'Risk', 'Diversification', 'Score')

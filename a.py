import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Initial Data
values = [20, 2, 3, 10, 10, 3, 2, 0.5, 2.6, 10]

# Function to calculate the second column
def calculate_second_row(values, total_area):
    sum_values = sum(values)
    return [round((value * total_area) / sum_values, 1) for value in values]

# Function to create DataFrame
def create_dataframe(values, total_area):
    second_row = calculate_second_row(values, total_area)
    
    df = pd.DataFrame({
        'Category': [
            'Residential',
            'Residential', 
            'Residential',
            'Industrial', 
            'Industrial',
            'Industrial',
            'Services', 
            'Services',
            'Services', 
            'Services',
        ],
        'Sub-Category': [
            'Living Space', 
            'Circulation & Common Areas', 
            'Shared Amenities',
            'Energy Generation', 
            'Food Production', 
            'Waste Management',
            'Schools', 
            'Hospitals', 
            'Retail & Amenities', 
            'Green Spaces'
        ],
        'Area per person (m²)': values,
        'Total Area (m²)': second_row
    })
    
    # Append Grand Totals
    grand_totals = pd.DataFrame({
        'Category': ['Grand Totals'],
        'Area per person (m²)': [sum(values)],
        'Total Area (m²)': [round(sum(second_row),0)]
    })
    
    df = pd.concat([df, grand_totals], ignore_index=True)
    return df

# Function to create category totals
def create_df_categoryTotals(df):
    categories = df['Category'].unique()
    category_totals = []

    for category in categories:
        if category != 'Grand Totals':
            area_per_person = df.loc[df['Category'] == category, 'Area per person (m²)'].sum()
            total_area = df.loc[df['Category'] == category, 'Total Area (m²)'].sum()
            category_totals.append({
                'Category': category,
                'Total Area per person (m²)': area_per_person,
                'Total Area (m²)': total_area
            })

    df_totals = pd.DataFrame(category_totals)
    grand_totals = pd.DataFrame({
        'Category': ['Grand Totals'],
        'Total Area per person (m²)': [df_totals['Total Area per person (m²)'].sum()],
        'Total Area (m²)': [round(df_totals['Total Area (m²)'].sum(), 0)]
    })
    
    df_totals = pd.concat([df_totals, grand_totals], ignore_index=True)
    return df_totals


# Function to calculate population
def calculate_population(df):
    total_area = df.loc[df['Category'] == 'Grand Totals', 'Total Area (m²)'].values[0]
    total_person_area = df.loc[df['Category'] == 'Grand Totals', 'Area per person (m²)'].values[0]
    return int(total_area / total_person_area)

def create_piechart(values, names):
    # Define a professional color palette
    colors = plt.cm.Paired(np.linspace(0, 1, len(names)))
    # Create the pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, _, _ = ax.pie(
        values,
        startangle=90,
        colors=colors,
        autopct=lambda p: f'{p:.1f}%' if p > 0 else '',  # Only show percentages > 5%
        pctdistance=0.85,
        # wedgeprops=dict(edgecolor='black', linewidth=1.5)
    )
    # Add a hole in the center to make it a donut chart (optional)
    # centre_circle = plt.Circle((0, 0), 0.70, fc='none')  # Transparent center
    # fig.gca().add_artist(centre_circle)
    # Add a legend
    ax.legend(
        wedges,
        names,
        loc="lower left",
        bbox_to_anchor=(1, 0.5),
        fontsize=10,
    )
    # Equal aspect ratio ensures the pie is drawn as a circle
    ax.axis('equal')
    # Set transparent background
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    # Tight layout for better spacing
    plt.tight_layout()
    return fig


# Initial calculation
default_total_area = 1000000
initial_df = create_dataframe(values, default_total_area)
initial_population = calculate_population(initial_df)
initial_dfTotals = create_df_categoryTotals(initial_df)

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## 🌇 Space Distribution Calculator")   
    with gr.Row():
            with gr.Column(scale = 1):
                
                with gr.Row():
                    # with gr.Column():
                        total_area_input = gr.Number(label="Total area of plot in sq.m.", value=default_total_area, interactive=True) 
                        gr.Examples(examples=[10000, 50000, 100000, 500000, 1000000], inputs = total_area_input)
                with gr.Row(variant = 'panel'):
                        with gr.Column(scale =1, variant = 'panel',  min_width = 80):
                            gr.Markdown("### Residential area in sq.m. per person")
                            input_1 = gr.Number(value=values[0], label="Living Space (minimum 10m²)", interactive=True)
                            input_2 = gr.Number(value=values[1], label="Circulation & Common Areas", interactive=True) 
                            input_3 = gr.Number(value=values[2], label="Shared Amenities", interactive=True)
                        with gr.Column(scale =1, variant = 'panel',  min_width = 80):
                            gr.Markdown("### Industrial area in sq.m. per person")
                            input_4 = gr.Number(value=values[3], label="Energy Generation", interactive=True)
                            input_5 = gr.Number(value=values[4], label="Food Production", interactive=True) 
                            input_6 = gr.Number(value=values[5], label="Waste Management", interactive=True) 
                        with gr.Column(scale =1, variant = 'panel',  min_width = 80):
                            gr.Markdown("### Service area in sq.m. per person")
                            input_7 = gr.Number(value=values[6], label="Schools", interactive=True)
                            input_8 = gr.Number(value=values[7], label="Hospitals", interactive=True) 
                            input_9 = gr.Number(value=values[8], label="Retail & Amenities", interactive=True)
                            input_10 = gr.Number(value=values[9], label="Green Spaces", interactive=True) 
                        
                with gr.Row():        
                        btn = gr.Button(value="Calculate")

                population_output = gr.Number(value=initial_population, label="Population", interactive=False)

                output_df = gr.DataFrame(value=initial_df, label="Calculated Space Distribution", interactive=False)
                output_dfTotals = gr.DataFrame(value=initial_dfTotals, label="Calculated Space Distribution by Group", interactive=False)
            with gr.Column():
                output_pie_chart = gr.Plot(value=create_piechart(initial_df['Total Area (m²)'][:-1], initial_df['Sub-Category'][:-1]), label="Space Distribution Pie Chart")
                output_pie_chartTotals = gr.Plot(value=create_piechart(initial_dfTotals['Total Area (m²)'][:-1], initial_dfTotals['Category'][:-1]), label="Space Distribution Pie Chart by Group")


            def update_outputs(input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, total_area):
                    values = [input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10]
                    df = create_dataframe(values, total_area)
                    population = calculate_population(df)
                    dfTotals = create_df_categoryTotals(df)
                    pie_chart = create_piechart(df['Total Area (m²)'][:-1], df['Sub-Category'][:-1])
                    pie_chartTotals = create_piechart(dfTotals['Total Area (m²)'][:-1], dfTotals['Category'][:-1])
                    return df, population, dfTotals, pie_chart, pie_chartTotals
                
            btn.click(fn=update_outputs, inputs=[input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, total_area_input], outputs=[output_df, population_output, output_dfTotals, output_pie_chart, output_pie_chartTotals])

# Launch the app
demo.launch(share = True)

# with gr.Blocks() as demo:
#     with gr.Row():
#         # Left Column with 3 sub-columns
#         with gr.Column(scale=1):
#             with gr.Row():
#                 gr.Textbox(label="Input 1")
#                 gr.Textbox(label="Input 2")
#                 gr.Textbox(label="Input 3")
        
#         # Right Column
#         with gr.Column(scale=1):
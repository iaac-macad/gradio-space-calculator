import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Initial Data
values = [13, 2, 1, 20, 50, 3, 2, 0.5, 2.6, 10]


# Function to calculate the second column
def calculate_total_area(values, total_area):
    sum_values = sum(values)
    return [round((value * total_area) / sum_values, 2) for value in values]

# Function to create DataFrame with the correct layout
def create_dataframe(values, total_areas):
    total_area_sum = sum(total_areas)
    # Calculate Grand Total row
    grand_total_row = {
        "Category": "Grand Total",
        "Area per person (m²)": "",
        "Total area (m²)": total_area_sum
    }
    
    data = {
        "Category": ['Living Space', 
                     'Circulation & Common Areas', 
                     'Shared Amenities', 
                     'Energy Generation', 
                     'Food Production', 
                     'Waste Management', 
                     'Schools', 
                     'Hospitals', 
                     'Retail & Amenities', 
                     'Green Spaces', 
                     grand_total_row["Category"]],
        "Area per person (m²)": values + [""],
        "Total area (m²)": total_areas + [grand_total_row["Total area (m²)"]]
    }

    df = pd.DataFrame(data)
    return df

# Function to create a professional-looking pie chart with a transparent background
def create_professional_pie_chart(df):
    # Define a professional color palette
    colors = plt.cm.Paired(np.linspace(0, 1, len(df["Category"].iloc[:-1])))

    # Create the pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, _, _ = ax.pie(
        df["Total area (m²)"].iloc[:-1],
        startangle=90,
        colors=colors,
        autopct=lambda p: f'{p:.1f}%' if p > 5 else '',  # Only show percentages > 5%
        pctdistance=0.85,
        wedgeprops=dict(edgecolor='white', linewidth=1.5)
    )

    # Add a hole in the center to make it a donut chart (optional)
    centre_circle = plt.Circle((0, 0), 0.70, fc='none')  # Transparent center
    fig.gca().add_artist(centre_circle)

    # Add a title
    ax.set_title("Space Distribution", fontsize=16, fontweight='bold', pad=20)

    # Add a legend
    ax.legend(
        wedges,
        df["Category"].iloc[:-1],
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=10,
        title_fontsize=12
    )

    # Equal aspect ratio ensures the pie is drawn as a circle
    ax.axis('equal')

    # Set transparent background
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    # Tight layout for better spacing
    plt.tight_layout()

    return fig

# Function to calculate population
def calculate_population(df):
    sum_area = df["Total area (m²)"].sum()
    sum_person_area = df["Area per person (m²)"].sum()
    if sum_person_area != 0:
        return int(sum_area / sum_person_area)
    return 0

# Initial calculation
default_total_area = 1000000
initial_total_areas = calculate_total_area(values, default_total_area)
initial_df = create_dataframe(values, initial_total_areas)

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## 🌇 Space Distribution Calculator")

    with gr.Row():
        with gr.Column():
            area_input = gr.Number(label="Total area of plot in sq.m.", value=default_total_area)
            output_df = gr.DataFrame(
                value=initial_df,
                label="Calculated Space Distribution",
                interactive=True,
                elem_classes=["dataframe-container"]  # Apply custom CSS class
            )

        with gr.Column():
            pie_chart = gr.Plot(value=create_professional_pie_chart(initial_df), label="Space Distribution Pie Chart")

    # Callback function to update the DataFrame and Pie Chart
    def update_interface(total_area, updated_df):
        # Extract the updated values from the DataFrame
        updated_area_values = updated_df["Area per person (m²)"].astype(float).tolist()

        # If the total area or area per person values are updated, we need to recalculate total areas
        total_areas = calculate_total_area(updated_area_values, total_area)

        # Create new DataFrame and pie chart
        new_df = create_dataframe(updated_area_values, total_areas)
        pie = create_professional_pie_chart(new_df)
        population = calculate_population(new_df)

        return new_df, pie, population

    # Trigger update on input change
    area_input.change(fn=update_interface, inputs=[area_input, output_df], outputs=[output_df, pie_chart])

    # Trigger recalculation when any "Area per person (m²)" column value is changed
    output_df.change(fn=update_interface, inputs=[area_input, output_df], outputs=[output_df, pie_chart])

demo.launch()



#python app.py

#sheet_id = "1t2OtpaCdslukleltKIDfKnaAJaqLMjAN"

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import gradio as gr

def load_data():
    sheet_id = "1t2OtpaCdslukleltKIDfKnaAJaqLMjAN"  # Replace with actual Google Sheets ID
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(csv_url)

def calculate_formulas(df):
    # Apply calculation dynamically if columns exist
    if {'C', 'D'}.issubset(df.columns):
        df['E'] = pd.to_numeric(df['C'], errors='coerce') * pd.to_numeric(df['D'], errors='coerce')
    return df

def create_dashboard(df):
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "table"}, {"type": "pie"}]],
        column_widths=[0.6, 0.4]
    )

    # Add table
    fig.add_trace(
        go.Table(
            header=dict(
                values=[f'<b>{col}</b>' for col in df.columns],
                fill_color='rgb(40, 40, 50)',
                align='center',
                font=dict(color='white', size=14),
                height=35
            ),
            cells=dict(
                values=[df[col] for col in df.columns],
                fill_color='rgb(50, 50, 60)',
                align='center',
                font=dict(color='white', size=13),
                height=30
            )
        ),
        row=1, col=1
    )

    # Add pie chart if applicable
    if 'B' in df.columns and 'E' in df.columns:
        fig.add_trace(
            go.Pie(
                labels=df['B'],
                values=df['E'],
                hole=0.4,
                textinfo='percent',
                marker=dict(colors=px.colors.qualitative.Set3)
            ),
            row=1, col=2
        )

    fig.update_layout(
        template='plotly_dark',
        title=dict(text='<b>Interactive Data Dashboard</b>', x=0.5, font=dict(color='white', size=24)),
        width=1400,
        height=800
    )

    return fig

def update_interface(*inputs):
    num_cols = len(initial_data.columns)
    reshaped_data = {col: inputs[i::num_cols] for i, col in enumerate(initial_data.columns)}
    df = pd.DataFrame(reshaped_data)
    df = calculate_formulas(df)
    return create_dashboard(df)

# Load data
initial_data = load_data()
initial_data = calculate_formulas(initial_data)

# Create Gradio Interface
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", neutral_hue="slate")) as iface:
    input_components = []

    for i, row in initial_data.iterrows():
        with gr.Row():
            for col in initial_data.columns:
                value = row[col]
                if col in ['C', 'D']:
                    input_components.append(gr.Number(label=f"{col} (Row {i+1})", value=value, interactive=True))
                else:
                    input_components.append(gr.Textbox(label=f"{col} (Row {i+1})", value=str(value), interactive=False))

    plot_output = gr.Plot()

    for field in input_components:
        if isinstance(field, gr.Number):
            field.change(fn=update_interface, inputs=input_components, outputs=plot_output)

    iface.load(fn=lambda: create_dashboard(initial_data), inputs=None, outputs=plot_output)

if __name__ == "__main__":
    iface.launch()

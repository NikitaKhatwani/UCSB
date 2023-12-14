from re import U
import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.offline as pyo
import matplotlib.pyplot as plt


@st.cache_data
def load_data(path):
    """
    Write 1-2 lines of code here to load the data from CSV to a pandas dataframe
    and return it.
    """

    # Load data
    raw_df = pd.read_excel(path)
    # Move the last row to become the first row
    raw_df = pd.concat([raw_df.iloc[-1:], raw_df.iloc[:-1]], ignore_index=True)
    return raw_df


@st.cache_data
def area_pieChart(df2):

    # Replace 'Auxiliary' with 'Academic'
    df2['Building Categorization Notes'] = df2['Building Categorization Notes'].replace('Auxiliary', 'Academic')
    # Group data by building category and sum area
    grouped_data = df2.groupby('Building Categorization Notes')['Building_Area (GSF)'].sum()
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('Breakdown of Building Area by Building Category')
    ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is drawn as a circle.

    # Display pie chart using Streamlit
    st.pyplot(fig)





def make_graph(index):

    # Create a new figure for the selected building
    fig = go.Figure()

    # Plot the first line (CHW)
    fig.add_trace(
        go.Scatter(x=CW_df['Dates'], y=CW_df.iloc[:,index], mode='lines', name='Chilled water', line=dict(color='#5289C7')))


    # Plot the second line (HW)
    fig.add_trace(
            go.Scatter(x=HW_df['Dates'], y=HW_df.iloc[:, index], mode='lines', name='Heating water',line=dict(color='#FF6961')))

    # Plot the third line (DHW)
    fig.add_trace(
            go.Scatter(x=DHW_df['Dates'], y=DHW_df.iloc[:, index], mode='lines', name='DHW', line=dict(color='#A94064')))

    # Set title
    fig.update_layout(
        title_text=f"{CW_df.columns[index]}"
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )


    # Display in Streamlit
    st.plotly_chart(fig)


# MAIN CODE


st.title("UCSB Decarbonization")

CHW_path = "UCSB_Chilled Water loads_8670 kWH.xlsx"
HHW_path = "UCSB_HHW loads_8670 kWH.xlsx"
DHW_path = "UCSB_DHW loads_8670 kWH.xlsx"
Area_path = "1204_Program&Areas.xlsx"

with st.spinner(text="Loading data..."):
    CW_df = load_data(CHW_path)
    HW_df = load_data(HHW_path)
    DHW_df = load_data(DHW_path)
    Area_df = load_data(Area_path)
# st.text("Visualize the overall dataset and some distributions here...")

if st.checkbox("Show Area Data"):
    st.write(Area_df)
    area_pieChart(Area_df)

if st.checkbox("Show CHW Raw Data"):
    st.write(CW_df)

if st.checkbox("Show HHW Raw Data"):
    st.write(HW_df)

if st.checkbox("Show DHW Raw Data"):
    st.write(DHW_df)

# st.header("Custom slicing")
# st.text("Implement your interactive slicing tool here...")

# st.header("Person sampling")
# st.text("Implement a button to sample and describe a random person here...")
# Create an empty list to store the graphs
figs = []


# Convert 'DateColumn' to datetime
CW_df['Dates'] = pd.to_datetime(CW_df['Dates'])
HW_df['Dates'] = pd.to_datetime(HW_df['Dates'])
DHW_df['Dates'] = pd.to_datetime(DHW_df['Dates'])

#get maximum number of columns
coolingCols = int(CW_df.shape[1])


# Create graph of full campus
make_graph(26)


# Create a list of building names
building_names = CW_df.columns[1:]

# Allow the user to select a building
selected_building = st.selectbox("Select a building", building_names, index=0)

# Get the index of the selected building
index = building_names.get_loc(selected_building) +1



make_graph(index)


# index = 0

# for i in range(coolingCols):
#     # Create a new figure for each pair of columns
#     fig = go.Figure()

#     # Calculate the index to skip dates
#     if i < 26:
#         index += 1

    

    
# Display in Streamlit
# st.plotly_chart(figs[26])
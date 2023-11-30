import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm

st.set_page_config(page_title="Lab10")

st.write("# Lab 10")

st.markdown(
    """
    ### Introduction 
    
    Introduction
    At the onset of the COVID pandemic in 2020, many opted to stop traveling and there was a 
    noticeable decline in airport travel. By 2022, airports seemed to be back to pre-pandemic 
    business. I want to investigate 2022 statistics for the most popular airports in the United 
    States.  
    """)

airports = pd.read_csv('2022Airports.csv')

st.write("# Dataset")
st.dataframe(airports) 

st.markdown(
    """
    ### About the Data

    I created an extensive table for the top 200 ranked airports in the United States. Data for 
    this ranked list was sourced from the Bureau of Transportation Statistics. 

    DataCleaning.ipynb is where the data was cleaned and organized. 
    - The ranked list file that was read into python needed to be cleaned. 
    - I cleaned it using a LOCID table and a supplementary LOCID table. 
    - Next, I added originating and enplaned passenger data for each airport. 
    - Then, I used rapidAPI to get ICAO codes for each row.
    - Next, I used a second API and the ICAO values to get long, lat, etc. columns. 
    - Last, I found a blog that compiled an updated table of US airports for 2020 and 
    interesting statistics. I accessed the table as a text file and merged it onto my pandas 
    DataFrame. 

    I saved this table as a csv file which can be viewed above. 

    # EDA

    In this EDA, I want to exlpore the relationship bewteen *2022 Delays* proportion and 
    other quantitative variables using a scatterplot.
        
    Then, I want to perform a regression analysis for the Q → Q scatterplots.
    """)

#  filters
st.write("### Scatterplot Filters")
selected_rank = st.slider("Select Rank Range", min_value=1, max_value=200, value=(1, 200))
selected_variable = st.selectbox("Select Variable for X-axis", ['Elevation', '2022 Enplaned Passengers'])

# Apply filters to the dataframe
filtered_airports = airports[(airports['2022 Rank'] >= selected_rank[0]) & (airports['2022 Rank'] <= selected_rank[1])]

fig = px.scatter(filtered_airports, x=selected_variable, y='Delays',
                 hover_data={'Airport': True, 'IATA': True, '2022 Rank': True, selected_variable: True, 'Delays': True},
                 color_discrete_sequence=['#4b7b9b'])

# Add trendline using statsmodels
X = sm.add_constant(filtered_airports[selected_variable])
y = filtered_airports['Delays']
model = sm.OLS(y, X).fit()
line = pd.DataFrame({selected_variable: [filtered_airports[selected_variable].min(), filtered_airports[selected_variable].max()]})
line['Delays'] = model.predict(sm.add_constant(line[selected_variable]))

fig.add_scatter(x=line[selected_variable], y=line['Delays'], mode='lines', name='Regression Line', line=dict(color='#00204e', width=2))

# Update layout
fig.update_traces(marker=dict(size=10, line=dict(width=2, color='#00204e')), selector=dict(mode='markers'))
fig.update_layout(title=f'Top 200 Airports 2022: Delays vs. {selected_variable} Insights',
                  xaxis_title=f'{selected_variable}',
                  yaxis_title='Delays (2022 proportion)',
                  height=650,
                  width=800)

st.plotly_chart(fig)

st.write("### Summary Statistics")
st.write(filtered_airports[[selected_variable, 'Delays']].describe())

# Get regression results
X = sm.add_constant(filtered_airports[selected_variable])
y = filtered_airports['Delays']
model = sm.OLS(y, X).fit()

# Display regression results
st.write("### Regression Analysis Results")
st.write(model.summary())

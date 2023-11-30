import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm

st.set_page_config(page_title="Lab10")

st.write("# Lab 10")

st.markdown(
    """
    ### EDA for Final Project

    In this EDA, I want to exlpore the relationship bewteen *2022 Delays* proportion and other quantitative variables using a scatterplot.
        
    Then, I want to perform a regression analysis for these scatterplots.  
    """)

airports = pd.read_csv('2022Airports.csv')

st.write("### Dataset Preview")
st.dataframe(airports) 

st.markdown(
    """
    ### About the Data

    This data was created...
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

st.write("## Summary Statistics")
st.write(filtered_airports[[selected_variable, 'Delays']].describe())

# Get regression results
#X = sm.add_constant(filtered_airports[selected_variable])
#y = filtered_airports['Delays']
#model = sm.OLS(y, X).fit()

# Display regression results
#st.write("## Regression Analysis Results")
#st.write(model.summary())
#"""
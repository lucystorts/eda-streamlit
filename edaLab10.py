import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px

airports = pd.read_csv('2022Airports.csv')


def run():
    st.set_page_config(
        page_title="Lab10",
    )

    st.write("# Lab 10")


    st.markdown(
        """
        ### EDA for Final Project

        In this EDA, I want to exlpore the relationship bewteen *2022 Delays* proportion and other quantitative variables using a scatterplot.
        
        Then, I want to perform a regression analysis for these scatterplots.  
    """
    )


if __name__ == "__main__":
    run()


import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")
st.title("BUNDESLIGA SALARIES EXPEDITURE ANALYSIS")

def calculate_expenditure(data, column):
    """
    Calculate the total salary expenditure for each category.
    
    Parameters:
    data (DataFrame): DataFrame containing salary data.
    column (str): Column name group by.
    
    Returns:
    DataFrame: DataFrame containing the total salary expenditure for each category.
    """
    expenditure = data.groupby(column)['GROSS P/Y'].sum().reset_index()
    return expenditure.sort_values(by='GROSS P/Y', ascending=False)

def plot_expenditure(expenditure, column, title):
    """
    Plot total salary expenditure for each category.
    
    Parameters:
    expenditure (DataFrame): DataFrame containing the total salary expenditure for each category.
    column (str): Column name to group by.
    title (str): Title of the plot.
    """
    #plot with streamlit, color by CLUB
    fig = px.bar(expenditure, x=column, y='GROSS P/Y', color=column, title=title, height=600, width=1000)
    st.plotly_chart(fig)

def choose_plot(expenditure_club, expenditure_position, expenditure_nationality, expenditure_age):
    """
    Allow the user to choose which plot to display.
    
    Parameters:
    expenditure_club (DataFrame): Expenditure data grouped by club.
    expenditure_position (DataFrame): Expenditure data grouped by position.
    expenditure_nationality (DataFrame): Expenditure data grouped by nationality.
    expenditure_age (DataFrame): Expenditure data grouped by age.
    """
    # make choice a dropdown as sidebar in streamlit page
    options=["1. ANUAL SALARIES PER CLUB", "2. ANUAL SALARIES PER POSITION", "3. ANUAL SALARIES PER NATIONALITY", "4. ANUAL SALARIES PER AGE"]
    choice = st.sidebar.selectbox("EXPENDITURE TYPE:", options=options)

    if choice == options[0]:
        plot_expenditure(expenditure_club, 'CLUB', 'ANUAL SALARIES PER CLUB')
    elif choice == options[1]:
        plot_expenditure(expenditure_position, 'POS SPECIFIC', 'ANUAL SALARIES PER POSITION')
    elif choice == options[2]:
        plot_expenditure(expenditure_nationality, 'NATIONALITY', 'ANUAL SALARIES PER NATIONALITY')
    elif choice == options[3]:
        plot_expenditure(expenditure_age, 'AGE', 'ANUAL SALARIES PER AGE')
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")

def main():
    try:
        # Read Excel file
        data = pd.read_excel('Salarios-BL-2024.xlsx')

        # Ensure AGE is treated as a string if it is not numeric
        if not pd.api.types.is_numeric_dtype(data['AGE']):
            data['AGE'] = data['AGE'].astype(str)
        
        # Calculate expenditure for each category
        expenditure_club = calculate_expenditure(data, 'CLUB')
        expenditure_position = calculate_expenditure(data, 'POS SPECIFIC')
        expenditure_nationality = calculate_expenditure(data, 'NATIONALITY')
        expenditure_age = calculate_expenditure(data, 'AGE')

        # Allow the user to choose which plot to display
        choose_plot(expenditure_club, expenditure_position, expenditure_nationality, expenditure_age)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

import streamlit as st

# Define a function that takes a name and returns a greeting
def greet(name):
    return f"Welcome, {name}!"

# Create a Streamlit app
def app():
    # Add a title to the app
    st.title("Algo_Trading App")

    # Ask the user for their name
    name = st.text_input("Enter your name:")

    # If the user has entered a name, display a greeting
    if name:
        greeting = greet(name)
        st.write(greeting)

# Run the app
if __name__ == '__main__':
    app()

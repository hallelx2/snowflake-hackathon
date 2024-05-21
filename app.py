import streamlit as st
from database import list_databases, list_warehouses, connect_to_database


def main():
    st.title("Snowflake Database Explorer")

    # Initialize session state variables
    if 'conn' not in st.session_state:
        st.session_state.conn = None
    if 'databases' not in st.session_state:
        st.session_state.databases = []
    if 'warehouses' not in st.session_state:
        st.session_state.warehouses = []
    if 'selected_database' not in st.session_state:
        st.session_state.selected_database = None
    if 'selected_warehouse' not in st.session_state:
        st.session_state.selected_warehouse = None

    # Sidebar for Snowflake connection
    st.sidebar.header("Snowflake Connection")
    st.session_state.user = st.sidebar.text_input("Snowflake User", value=st.session_state.get("user", ""))
    st.session_state.password = st.sidebar.text_input("Snowflake Password", type="password", value=st.session_state.get("password", ""))
    st.session_state.account = st.sidebar.text_input("Snowflake Account", value=st.session_state.get("account", ""))

    if st.sidebar.button("Connect to Snowflake"):
        user = st.session_state.user
        password = st.session_state.password
        account = st.session_state.account
        if user and password and account:
            st.session_state.databases = list_databases(user, password, account)
            st.session_state.warehouses = list_warehouses(user, password, account)
            if st.session_state.databases is not None and st.session_state.warehouses is not None:
                st.sidebar.success("Successfully connected to Snowflake!")
            else:
                st.sidebar.error("Failed to retrieve databases or warehouses.")
        else:
            st.sidebar.warning("Please enter all the required credentials.")

    # Display databases and warehouses in the sidebar
    if st.session_state.databases:
        st.sidebar.header("Select Database")
        st.session_state.selected_database = st.sidebar.selectbox("Database", st.session_state.databases)
    if st.session_state.warehouses:
        st.sidebar.header("Select Warehouse")
        st.session_state.selected_warehouse = st.sidebar.selectbox("Warehouse", st.session_state.warehouses)

    # Main area for displaying connection status and other functionalities
    if st.session_state.selected_database:
        st.header("Connect to Selected Database")
        if st.button("Connect"):
            st.session_state.conn = connect_to_database(
                st.session_state.user,
                st.session_state.password,
                st.session_state.account,
                database=st.session_state.selected_database
            )
            if st.session_state.conn:
                st.success(f"Connected to database: {st.session_state.selected_database}")
            else:
                st.error("Failed to connect to the selected database.")

if __name__ == "__main__":
    main()

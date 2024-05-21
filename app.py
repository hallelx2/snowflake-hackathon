import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from database import list_databases, list_warehouses, connect_to_database

def get_response(db, user_query):
    pass


def main():
    st.title("Snowflake Database Explorer")

    # Initialize session state variables
    if 'user' not in st.session_state:
        st.session_state.user = ""
    if 'password' not in st.session_state:
        st.session_state.password = ""
    if 'account' not in st.session_state:
        st.session_state.account = ""
    if 'databases' not in st.session_state:
        st.session_state.databases = []
    if 'warehouses' not in st.session_state:
        st.session_state.warehouses = []
    if 'selected_database' not in st.session_state:
        st.session_state.selected_database = None
    if 'selected_warehouse' not in st.session_state:
        st.session_state.selected_warehouse = None
    if 'conn' not in st.session_state:
        st.session_state.conn = None

    # Sidebar for Snowflake connection and chat interface
    st.sidebar.title("Snowflake Connection")
    st.sidebar.write("---")
    st.session_state.user = st.sidebar.text_input("Snowflake User", value=st.session_state.user)
    st.session_state.password = st.sidebar.text_input("Snowflake Password", type="password", value=st.session_state.password)
    st.session_state.account = st.sidebar.text_input("Snowflake Account", value=st.session_state.account)
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

    if st.session_state.databases:
        st.sidebar.write("---")
        st.sidebar.title("Choose Database")
        st.sidebar.write("Select a database to use in the chat and also for the summary.")
        st.session_state.selected_database = st.sidebar.selectbox("Select a database", st.session_state.databases)
        if st.sidebar.button("Connect to Database"):
            st.session_state.conn = connect_to_database(st.session_state.user, st.session_state.password, st.session_state.account, database=st.session_state.selected_database)
            if st.session_state.conn:
                st.sidebar.success(f"Connected to database: {st.session_state.selected_database}")
            else:
                st.sidebar.error("Failed to connect to the selected database.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content = "Hello, I can help you find the right answers to the questions about your PDF, How can I help you"),
        ]
    
    db = st.file_uploader('Upload your PDF', type='pdf')

    # User functionality
    user_query = st.chat_input('Ask your question')
    if user_query is not None and user_query!='':
        response = get_response(user_query, db)
        st.session_state.chat_history.append(HumanMessage(content= user_query))
        st.session_state.chat_history.append(AIMessage(content = response))
        
    # conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message('AI'):
                st.write(message.content)
        elif isinstance(message,HumanMessage):
            with st.chat_message('Human'):
                st.write(message.content)

if __name__ == "__main__":
    main()

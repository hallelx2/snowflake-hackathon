import streamlit as st
from rich import print
import snowflake.connector

# Helper functions
def get_snowflake_connection(user: str, password: str, account: str):
    """
    Establishes a connection to the Snowflake account.

    Args:
        user (str): The Snowflake user.
        password (str): The Snowflake user's password.
        account (str): The Snowflake account.

    Returns:
        snowflake.connector.connection.SnowflakeConnection: The connection object to Snowflake.
    """
    try:
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account
        )
        print("[bold green]Successfully connected to Snowflake![/bold green]")
        return conn
    except Exception as e:
        print(f"[bold red]Error connecting to Snowflake: {e}[/bold red]")
        return None

def list_databases(user: str, password: str, account: str):
    """
    Lists all databases in the Snowflake account.

    Args:
        user (str): The Snowflake user.
        password (str): The Snowflake user's password.
        account (str): The Snowflake account.

    Returns:
        List[str]: A list of database names.
    """
    conn = get_snowflake_connection(user, password, account)
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()
        cursor.close()
        database_names = [db[1] for db in databases]
        return database_names
    except Exception as e:
        print(f"[bold red]Error listing databases: {e}[/bold red]")
        return None
    finally:
        conn.close()

def list_warehouses(user: str, password: str, account: str):
    """
    Lists all warehouses in the Snowflake account.

    Args:
        user (str): The Snowflake user.
        password (str): The Snowflake user's password.
        account (str): The Snowflake account.

    Returns:
        List[str]: A list of warehouse names.
    """
    conn = get_snowflake_connection(user, password, account)
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW WAREHOUSES;")
        warehouses = cursor.fetchall()
        cursor.close()
        warehouse_names = [wh[1] for wh in warehouses]
        return warehouse_names
    except Exception as e:
        print(f"[bold red]Error listing warehouses: {e}[/bold red]")
        return None
    finally:
        conn.close()

def connect_to_database(user: str, password: str, account: str, database: str):
    """
    Establishes a connection to the specified Snowflake database.

    Args:
        user (str): The Snowflake user.
        password (str): The Snowflake user's password.
        account (str): The Snowflake account.
        database (str): The database to connect to.

    Returns:
        snowflake.connector.connection.SnowflakeConnection: The connection object to Snowflake.
    """
    try:
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            database=database
        )
        print(f"[bold green]Successfully connected to database: {database}![/bold green]")
        return conn
    except Exception as e:
        print(f"[bold red]Error connecting to Snowflake database: {e}[/bold red]")
        return None

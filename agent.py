import os
from dotenv import load_dotenv

from artic import SnowflakeArticModel, CustomLanguageModel

from langchain.tools import StructuredTool, tool, BaseTool

api_token = os.getenv('REPLICATE_API_TOKEN')
model_name = "snowflake/snowflake-arctic-instruct"

custom_model = CustomLanguageModel(model_name=model_name, api_token=api_token)
llm = SnowflakeArticModel(custom_model=custom_model)
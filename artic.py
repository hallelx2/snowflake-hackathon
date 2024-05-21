import os
import replicate
from langchain.llms.base import LLM
from typing import Generator, List, Optional, Dict, Any
from pydantic import Field

from dotenv import load_dotenv
from rich import print

import warnings

warnings.filterwarnings("ignore")

load_dotenv()

class CustomLanguageModel:
    def __init__(self, model_name: str, api_token: str):

        """
        Initializes the CustomLanguageModel.

        Args:
            model_name (str): The name of the model to use from Replicate.
            api_token (str): The API token for authenticating with Replicate.
        """

        self.model_name = model_name
        self.api_token = api_token

    def predict(self, prompt: str, stop: Optional[str] = "<|im_end|>", **kwargs) -> str:
        """
        Generates a prediction for a given prompt.

        Args:
            prompt (str): The input text prompt.
            stop (Optional[str]): The sequence where the model should stop generating further tokens.
            **kwargs: Additional parameters for the model.

        Returns:
            str: The generated text from the model.
        """

        try:
            output = replicate.run(
                self.model_name,
                input={
                    "top_k": kwargs.get("top_k", 50),
                    "top_p": kwargs.get("top_p", 0.9),
                    "prompt": prompt,
                    "temperature": kwargs.get("temperature", 0.2),
                    "max_new_tokens": kwargs.get("max_new_tokens", 512),
                    "min_new_tokens": kwargs.get("min_new_tokens", 0),
                    "stop_sequences": stop or "",
                    "prompt_template": kwargs.get("prompt_template", "system\nYou're a helpful assistant\nuser\n{prompt}\n\nassistant\n"),
                    "presence_penalty": kwargs.get("presence_penalty", 1.15),
                    "frequency_penalty": kwargs.get("frequency_penalty", 0.2)
                }
            )
            # Concatenate the list of strings into a single string
            if isinstance(output, list):
                return ''.join(output)
            return str(output)
        except Exception as e:
            print(f"Error during prediction: {e}")
            return ""

    def stream_predict(self, prompt: str, stop: str = "<|im_end|>", **kwargs) -> Generator[str, None, None]:
        """
        Streams the prediction for a given prompt.

        Args:
            prompt (str): The input text prompt.
            stop (str): The sequence where the model should stop generating further tokens.
            **kwargs: Additional parameters for the model.

        Yields:
            str: The generated text from the model, one event at a time.
        """
        try:
            for event in replicate.stream(
                self.model_name,
                input={
                    "top_k": kwargs.get("top_k", 50),
                    "top_p": kwargs.get("top_p", 0.9),
                    "prompt": prompt,
                    "temperature": kwargs.get("temperature", 0.2),
                    "max_new_tokens": kwargs.get("max_new_tokens", 512),
                    "min_new_tokens": kwargs.get("min_new_tokens", 0),
                    "stop_sequences": stop,
                    "prompt_template": kwargs.get("prompt_template", "system\nYou're a helpful assistant\nuser\n{prompt}\n\nassistant\n"),
                    "presence_penalty": kwargs.get("presence_penalty", 1.15),
                    "frequency_penalty": kwargs.get("frequency_penalty", 0.2)
                },
            ):
                yield str(event)
        except Exception as e:
            print(f"Error during streaming prediction: {e}")
            yield ""

class SnowflakeArticModel(LLM):
    custom_model: CustomLanguageModel = Field(...)

    def __init__(self, custom_model: CustomLanguageModel):
        """
        Initializes the CustomLangChainModel.

        Args:
            custom_model (CustomLanguageModel): An instance of the CustomLanguageModel.
        """
        super().__init__()
        object.__setattr__(self, 'custom_model', custom_model)


    def _call(self, prompt: str, stop: str = "<|im_end|>") -> str:
        """
        Calls the model to generate a prediction.

        Args:
            prompt (str): The input text prompt.
            stop (Optional[str]): The sequence where the model should stop generating further tokens.

        Returns:
            str: The generated text from the model.
        """
        try:
            response = self.custom_model.predict(prompt=prompt, stop=stop)
            return response
        except Exception as e:
            print(f"Error during _call: {e}")
            return ""

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """
        Returns identifying parameters of the model.

        Returns:
            Dict[str, Any]: A dictionary of identifying parameters.
        """

        return {"model_name": self.custom_model.model_name}

    def stream(self, prompt: str, stop: Optional[List[str]] = None) -> Generator[str, None, None]:
        """
        Streams the model's prediction.

        Args:
            prompt (str): The input text prompt.
            stop (Optional[str]): The sequence where the model should stop generating further tokens.

        Yields:
            str: The generated text from the model, one event at a time.
        """
        
        try:
            stop_sequences = "".join(stop) if stop else ""
            for event in self.custom_model.stream_predict(prompt, stop=stop_sequences):
                yield event
        except Exception as e:
            print(f"Error during stream: {e}")
            yield ""

    @property
    def _llm_type(self) -> str:
        """
        Returns the type of the language model.

        Returns:
            str: The type of the language model.
        """

        return "custom_langchain_model"

# Example usage
api_token = os.getenv('REPLICATE_API_TOKEN')
model_name = "snowflake/snowflake-arctic-instruct"

custom_model = CustomLanguageModel(model_name=model_name, api_token=api_token)
llm = SnowflakeArticModel(custom_model=custom_model)

# Synchronous prediction
response = llm("Write fizz buzz in SQL", stop="<|im_end|>")
print(f"Synchronous response: {response}")

# # Streaming prediction
# for event in llm.stream("Write fizz buzz in SQL", stop=["<|im_end|>"]):
#     print(f"Streaming event: {event}", end="")
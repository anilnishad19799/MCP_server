from autogen_ext.models.openai import OpenAIChatCompletionClient

def get_model_client(api_key: str):
    return OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=api_key,
        model_kwargs={"max_tokens": 1000}
    )

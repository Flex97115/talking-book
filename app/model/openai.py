from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from .base import BaseModel


class OpenAiModel(BaseModel):
    def __init__(self, temperature=0, streaming=True):
        super().__init__(
            llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=temperature, streaming=streaming),
            embeddings=OpenAIEmbeddings()
        )



from langchain.llms.ollama import Ollama
from langchain_community.embeddings import OllamaEmbeddings

from .base import BaseModel


class LocalModel(BaseModel):
    def __init__(self, model_name="mistral", embeddings_name="nomic-embed-text"):
        super().__init__(
            llm=Ollama(model=model_name),
            embeddings=OllamaEmbeddings(model=embeddings_name)
        )

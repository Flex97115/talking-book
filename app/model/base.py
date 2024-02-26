
class BaseModel:
    def __init__(self, llm=None, embeddings=None):
        self._llm = llm
        self._embeddings = embeddings

    @property
    def llm(self):
        return self._llm

    @property
    def embeddings(self):
        return self._embeddings

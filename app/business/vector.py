import chainlit as cl
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


async def create_vector_store(text):
    embeddings = cl.user_session.get("embeddings")

    # Split the text into chunks
    texts = text_splitter.split_text(text)

    # Create a metadata for each chunk
    metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]

    return await cl.make_async(Chroma.from_texts)(
        texts, embeddings, metadatas=metadatas
    )

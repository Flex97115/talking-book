import chainlit as cl
from chainlit.input_widget import Select
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_message_histories import ChatMessageHistory

from model.local import LocalModel
from model.openai import OpenAiModel

from langchain.memory import ConversationBufferMemory

from business.file.file_manager import upload_file
from business.vector import create_vector_store


def __get_memory():
    message_history = ChatMessageHistory()

    return ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )


async def setup_model(settings):
    print("Setup with following settings: ", settings)

    model = None

    if settings["model"] == "OpenAI":
        print("Using OpenAI")
        model = OpenAiModel()
    elif settings["model"] == "Ollama":
        print("Using Ollama")
        model = LocalModel()
    else:
        raise ValueError(f"Model {settings['model']} is not supported")

    memory = __get_memory()

    cl.user_session.set("llm", model.llm)
    cl.user_session.set("embeddings", model.embeddings)
    cl.user_session.set("memory", memory)


async def setup_chain(settings=None):
    if settings:
        await setup_model(settings)

    memory = cl.user_session.get("memory")
    llm = cl.user_session.get("llm")

    # Upload the file
    text, file_messenger = await upload_file()

    # Create a Chroma vector store
    docsearch = await create_vector_store(text)

    # Create a chain that uses the Chroma vector store
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )

    # Let the user know that the system is ready
    await file_messenger.send_done_msg()

    cl.user_session.set("chain", chain)


async def create_settings():
    settings = await cl.ChatSettings(
        [
            Select(
                id='model',
                label='Select model',
                values=["OpenAI", "Ollama"],
                initial_index=1,
            )
        ]
    ).send()
    await setup_model(settings)

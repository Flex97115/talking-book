from typing import List

from langchain.chains import (
    ConversationalRetrievalChain,
)

import chainlit as cl

from dotenv import load_dotenv

from life_cycle.settings import setup_chain, create_settings

load_dotenv()

@cl.on_chat_start
async def on_chat_start():
    await create_settings()
    await setup_chain()


@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")  # type: ConversationalRetrievalChain
    cb = cl.AsyncLangchainCallbackHandler()

    res = await chain.acall(message.content, callbacks=[cb])
    answer = res["answer"]
    source_documents = res["source_documents"]  # type: List[Document]

    text_elements = []  # type: List[cl.Text]

    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            # Create the text element referenced in the message
            text_elements.append(
                cl.Text(content=source_doc.page_content, name=source_name)
            )
        source_names = [text_el.name for text_el in text_elements]

        if source_names:
            answer += f"\nSources: {', '.join(source_names)}"
        else:
            answer += "\nNo sources found"

    await cl.Message(content=answer, elements=text_elements).send()

@cl.on_settings_update
async def on_settings_update(settings):
    await cl.Message(content=f"Using {settings['model']}").send()
    await setup_chain(settings)
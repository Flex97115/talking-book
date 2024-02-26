import chainlit as cl

from .file_messenger import FileProcessingMessenger


async def upload_file():
    files = None

    # Wait for the user to upload a file
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a text file to begin!",
            accept=["text/plain"],
            max_size_mb=20,
            timeout=180,
        ).send()

    file = files[0]

    file_messenger = FileProcessingMessenger(file)

    await file_messenger.send_pending_msg()

    with open(file.path, "r", encoding="utf-8") as f:
        text = f.read()

    return text, file_messenger

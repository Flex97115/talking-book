import chainlit as cl


class FileProcessingMessenger:
    messenger = None

    def __init__(self, file, initial_msg=None):
        self.file = file
        self.initial_msg = initial_msg

    async def __send(self, msg_content):
        if self.messenger:
            self.messenger.content = msg_content
            await self.messenger.update()
        else:
            self.messenger = cl.Message(content=msg_content, disable_feedback=True)
            await self.messenger.send()

    async def send_pending_msg(self):
        await self.__send(f"Processing `{self.file.name}`...", )

    async def send_done_msg(self):
        await self.__send(f"Processing `{self.file.name}` done. You can now ask questions!", )
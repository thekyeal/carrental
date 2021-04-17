# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount

from config import DefaultConfig


class QnABot(ActivityHandler):
    def __init__(self, config: DefaultConfig):
        self.qna_maker = QnAMaker(
            QnAMakerEndpoint(
                knowledge_base_id="42d7fd23-2f81-4320-b37a-ad569e8defd1",
                endpoint_key="27c71abc-47c7-4dfd-8595-df5b21be3d98",
                host="https://honeypot-a90b.azurewebsites.net/qnamaker",
            )
        )
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Welcome to Universal Rentals.")
                await turn_context.send_activity("I am here to answer any questions you may have regarding to our services")

    async def on_message_activity(self, turn_context: TurnContext):
        # The actual call to the QnA Maker service.
        response = await self.qna_maker.get_answers(turn_context)
        if response and len(response) > 0:
            await turn_context.send_activity(MessageFactory.text(response[0].answer))
        else:
            await turn_context.send_activity("No QnA Maker answers were found.")

from botbuilder.core import ActivityHandler, ConversationState, TurnContext, UserState, MessageFactory
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper
from config import DefaultConfig


class DialogBot(ActivityHandler):

    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
        config: DefaultConfig,):

        if conversation_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. user_state is required but None was given"
            )
        if dialog is None:
            raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext):


        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Welcome to Universal Rental {member.name}."                        
                    )
                )
                await self._send_suggested_actions(turn_context)        

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have ocurred during the turn.
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        userInput = turn_context.activity.text
        await DialogHelper.run_dialog(self.dialog,turn_context,self.conversation_state.create_property("DialogState"))
    
    
    async def _send_suggested_actions(self, turn_context: TurnContext):

        reply = MessageFactory.text("How May I assist.")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Ask Question",
                    type=ActionTypes.im_back,
                    value="sure",     
                ),
                CardAction(
                    title="Register",
                    type=ActionTypes.im_back,
                    value="Register",     
                ),
            ]
        )
        return await turn_context.send_activity(reply)


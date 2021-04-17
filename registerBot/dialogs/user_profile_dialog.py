from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    NumberPrompt,
    ChoicePrompt,
    ConfirmPrompt,
    PromptOptions,
    PromptValidatorContext,
)
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState


from data_models import UserProfile
import mysql.connector
import random, hashing


cnx = mysql.connector.connect(user="kreation@carrentals", password="Wethepeople@3", host="carrentals.mysql.database.azure.com", port=3306, database="universalRentals")


class UserProfileDialog(ComponentDialog):
    def __init__(self, user_state: UserState,):
        super(UserProfileDialog, self).__init__(UserProfileDialog.__name__)

        self.user_profile_accessor = user_state.create_property("UserProfile")

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.fName_step,
                    self.lName_step,
                    self.password_step,
                    self.color_step,
                    self.email_step,
                    self.summary_step,
                ],
            )
        )
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.initial_dialog_id = WaterfallDialog.__name__

    async def fName_step(
        self, step_context: WaterfallStepContext) -> DialogTurnResult:

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Please enter your first name"),
            ),
        )

    async def lName_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["fname"] = step_context.result
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Please enter your Last name")),
        )

    async def password_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["lname"] = step_context.result
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Please enter your password")),
        )

    async def color_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["password"] = step_context.result
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Please enter your favorite color.")),
            )

    async def email_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["color"] = step_context.result

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Please enter your email address")),
        )


    async def summary_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["email"] = step_context.result
        if step_context.result:
            
            user_profile = await self.user_profile_accessor.get(step_context.context, UserProfile)

            user_profile.fname = step_context.values["fname"]
            user_profile.lname = step_context.values["lname"]
            user_profile.password = step_context.values["password"]
            user_profile.color = step_context.values["color"]
            user_profile.email = step_context.values["email"]

            userID = random.randint(0,100)
            uname = user_profile.fname[0:3] + user_profile.lname[0:3] + str(userID)
            hashedpassword = hashing.hash_password(user_profile.password)
            fullname = user_profile.fname +" "+user_profile.lname

            msg = f"Your username is: {uname} \n\n"
            msg += f"Feel free to login to you account at https://universalrentals.herokuapp.com/login"

            
            cursor = cnx.cursor()
            cursor.execute("INSERT INTO users (username, password, colour, email_address, fullName, points) VALUES (%s, %s, %s, %s, %s, %s);", (uname, hashedpassword, user_profile.color,  user_profile.email, fullname, 1))
            cnx.commit()
            cursor.close()
            cnx.close()

            await step_context.context.send_activity(MessageFactory.text(msg))

        return await step_context.end_dialog()

        
    



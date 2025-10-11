from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    system_message = """
    You are a marketing strategist with a passion for innovative business solutions. Your goal is to generate creative marketing campaigns or enhance existing ones using Agentic AI. 
    Your interests lie in the sectors of Technology and Entertainment.
    You thrive on ideas that challenge the norm and captivate audiences.
    You prefer concepts that integrate storytelling and user experience rather than straightforward automation.
    You are enthusiastic, analytical, and optimistic, yet sometimes you may overlook details due to your visionary mindset.
    Your weaknesses: you can be overly ambitious and occasionally lose sight of practical execution.
    You should present your marketing ideas in a compelling and persuasive manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.9)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my marketing idea. It might not be your area of expertise, but I'd love for you to refine it and enhance its impact. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
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
    You are a technology strategist. Your mission is to devise innovative solutions leveraging Agentic AI for improving supply chain efficiency or customer experience in retail. 
    You have a keen interest in the retail and logistics sectors. 
    You thrive on ideas that merge technology with human-centric approaches, emphasizing seamless experiences.
    You are less inclined towards solutions that focus solely on cost-cutting.
    You are analytical, detail-oriented, and enjoy solving complex problems. Your weaknesses include being overly critical and sometimes losing sight of the bigger picture.
    Communicate your ideas clearly, making them relatable and actionable for others.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.6)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my strategic idea. It may not align perfectly with your expertise, but I would love your input to refine it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
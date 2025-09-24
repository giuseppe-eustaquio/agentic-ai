from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field, config
from crewai_tools import SerperDevTool
import os
import requests
from crewai.tools import BaseTool
from typing import Type
# from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
# from crewai.memory.storage.rag_storage import RAGStorage
# from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
import logging
# from .tools.push_tool import PushNotificationTool

class PushNotification(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="The message to be sent to the user.")

# vibe code = added debug because pushnotification isn't working
class PushNotificationTool(BaseTool):
    name: str = "Send a Push Notification"
    description: str = (
        "This tool is used to send a push notification to the user."
    )
    args_schema: Type[BaseModel] = PushNotification

    def _run(self, message: str) -> str:
        print("="*80)
        print("PUSH NOTIFICATION TOOL DEBUG START")
        print("="*80)
        print(f"DEBUG: Tool called with message: {message}")
        
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        
        print(f"DEBUG: User key length: {len(pushover_user) if pushover_user else 0}")
        print(f"DEBUG: Token length: {len(pushover_token) if pushover_token else 0}")
        print(f"DEBUG: User key starts with: {pushover_user[:8] if pushover_user else 'None'}...")
        print(f"DEBUG: Token starts with: {pushover_token[:8] if pushover_token else 'None'}...")
        
        if not pushover_user or not pushover_token:
            error_msg = "Missing Pushover credentials"
            print(f"ERROR: {error_msg}")
            return f'{{"error": "{error_msg}"}}'
        
        pushover_url = "https://api.pushover.net/1/messages.json"
        
        payload = {
            "user": pushover_user,
            "token": pushover_token, 
            "message": message,
            "title": "Stock Picker Alert"
        }
        
        print(f"DEBUG: Making request to: {pushover_url}")
        print(f"DEBUG: Payload keys: {list(payload.keys())}")
        
        try:
            print("DEBUG: Sending POST request...")
            response = requests.post(pushover_url, data=payload, timeout=30)
            
            print(f"DEBUG: Response status code: {response.status_code}")
            print(f"DEBUG: Response headers: {dict(response.headers)}")
            
            try:
                response_json = response.json()
                print(f"DEBUG: Response JSON: {response_json}")
            except:
                print(f"DEBUG: Response text: {response.text}")
                response_json = {}
            
            if response.status_code == 200:
                if response_json.get("status") == 1:
                    print("SUCCESS: Push notification sent successfully!")
                    print("="*80)
                    print("PUSH NOTIFICATION TOOL DEBUG END")
                    print("="*80)
                    # Return a unique confirmation that the agent can't fake
                    import time
                    timestamp = int(time.time())
                    unique_id = f"REAL_TOOL_EXECUTION_{timestamp}_{hash(message) % 10000}"
                    return f'{{"notification": "sent successfully", "status": "ok", "unique_confirmation": "{unique_id}", "pushover_response": {response_json}}}'
                else:
                    error_details = response_json.get("errors", ["Unknown error"])
                    print(f"ERROR: Pushover API error: {error_details}")
                    print("="*80)
                    print("PUSH NOTIFICATION TOOL DEBUG END")
                    print("="*80)
                    return f'{{"error": "Pushover API error", "details": {error_details}}}'
            else:
                print(f"ERROR: HTTP error: {response.status_code}")
                print("="*80)
                print("PUSH NOTIFICATION TOOL DEBUG END") 
                print("="*80)
                return f'{{"error": "HTTP error", "status_code": {response.status_code}, "response": "{response.text}"}}'
                
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"ERROR: {error_msg}")
            print("="*80)
            print("PUSH NOTIFICATION TOOL DEBUG END")
            print("="*80)
            return f'{{"error": "{error_msg}"}}'
        
        

class TrendingCompany(BaseModel):
    """ A company that is in the news and attracting attention """
    name: str = Field(description="Company name")
    ticket: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason why this company is trending in the news")


class TrendingCompanyList(BaseModel):
    """ List of multiple trending companies that are in the news """
    companies: List[TrendingCompany] = Field(description="List of companies trending in the news")

class TrendingCompanyResearch(BaseModel):
    """ Detailed research on a company """
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential and suitability for investment")

class TrendingCompanyResearchList(BaseModel):
    """ A list of detailed research on all the companies """
    research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on all trending company research")


@CrewBase
class StockPickernew():
    """StockPickernew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'], tools=[SerperDevTool()])

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'], tools=[SerperDevTool()])
    
    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'], tools=[PushNotificationTool()], verbose=True)

    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'],
            output_pydantic=TrendingCompanyList
        )
    
    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'],
            output_pydantic=TrendingCompanyResearchList
        )
    
    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""

        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True
        )

        # short_term_memory = ShortTermMemory(
        #     storage = RAGStorage(
        #         embedder_config={
        #             "provider": "openai",
        #             "config": {
        #                 "model": "text-embedding-3-small"
        #             }
        #         },
        #         type="short_term",
        #         path="./memory/"
        #     )
        # )

        # long_term_memory = LongTermMemory(
        #     storage=LTMSQLiteStorage(
        #         db_path="./memory/long_term_memory_storage.db"
        #     )
        # )

        # entity_memory = EntityMemory(
        #     storage=RAGStorage(
        #         embedder_config={
        #             "provider": "openai",
        #             "config": {
        #                 "model": "text-embedding-3-small"
        #             }
        #         },
        #         type="short_term",
        #         path="./memory/"
        #     )
        # )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            # memory=True,
            # long_term_memory=long_term_memory,
            # short_term_memory=short_term_memory,
            # entity_memory=entity_memory
        )
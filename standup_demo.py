import os
from datetime import datetime, timedelta
from crewai import Agent, Task, Crew
from crewai_tools import MergeAgentHandlerTool

tools = MergeAgentHandlerTool.from_tool_pack(
    tool_pack_id=os.getenv("TOOL_PACK_ID"),
    registered_user_id=os.getenv("REGISTERED_USER_ID"),
    tool_names=["github__get_commits", "github__list_issues", "slack__post_message"]
)

stand_up_agent = Agent(
    role="GitHub Reporter",
    goal="Write honest daily standup updates",
    backstory="""You're a helpful assistant that checks a developer's 
    GitHub activity and writes authentic standup updates.""",
    tools=tools,
    verbose=True
)

yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

task = Task(
    description=f"""
    Check my GitHub activity from {yesterday}:
    1. Get all commits I made
    2. Check issues I worked on
    3. Write a standup: Yesterday, Today, Blockers
    4. Post to #daily-standup in Slack
    Keep it concise. 3-4 sentences max and be specific.
    """,
    agent=stand_up_agent,
    expected_output="Confirmation that standup was posted to Slack"
)

crew = Crew(
    agents=[stand_up_agent],
    tasks=[task],
)

task.crew.kickoff()
print("Standup posted to Slack!")

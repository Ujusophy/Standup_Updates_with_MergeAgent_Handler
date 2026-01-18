from datetime import datetime, timedelta
from crewai import Agent, Task, Crew
from crewai_tools import MergeAgentHandlerTool

tools = MergeAgentHandlerTool.from_tool_pack(
    tool_pack_id="",
    registered_user_id="",
    tool_names=["github__get_commits", "slack__post_message"],
    connect_to_mcp=True
)

stand_up_agent = Agent(
    role="GitHub Reporter",
    goal="Write honest daily standup updates",
    backstory="You're a helpful assistant that checks a developer's GitHub activity and writes authentic standup updates.",
    tools=tools,
    verbose=True
)

yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

github_task = Task(
    description=f"Write a standup update with commits owner 'Ujusophy' {yesterday} in the 'Standup-Updates-with-MergeAgent-Handler' repository",
    agent=stand_up_agent,
    expected_output="Standup commit update in the format: Yesterday, Today, Blockers",
)

slack_task = Task(
    description="Post a summary of the message to the #daily-standup channel.",
    agent=stand_up_agent,
    expected_output="Confirmation that the message was posted"
)
crew = Crew(
    agents=[stand_up_agent],
    tasks=[github_task, slack_task],
    verbose=True
)

result = crew.kickoff()
print("Standup posted to Slack!")

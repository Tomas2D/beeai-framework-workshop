import asyncio

from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend import ChatModel
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.tools.weather import OpenMeteoTool

# === Task Overview ===
# 1. Experiment with the built-in ReAct Agent (initialize, run, observe behavior)
# 2. Review problems_{a,b,c}.py to understand ReAct's limitations
# 3. Examine custom_requirement.py for custom agent requirements
# 4. Explore workflow.py for multi-agent orchestration


async def task_1() -> None:
    print("[Task 1] Explore ReActAgent with OpenMeteoTool and WikipediaTool...\n")
    agent = ReActAgent(
        llm=ChatModel.from_name("ollama:granite3.3:8b"),
        memory=UnconstrainedMemory(),
        tools=[OpenMeteoTool(), WikipediaTool()],
    )

    prompts = [
        "Tell me something about Las Vegas",
        "What's the current weather in there?",
    ]

    for prompt in prompts:
        print(f"➡️  Question: {prompt}")
        response = await agent.run(prompt).middleware(
            GlobalTrajectoryMiddleware(included=[Tool])  # Show only tool calls
        )
        print(f"\n⬅️  Response: {response.result.text}")
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(task_1())

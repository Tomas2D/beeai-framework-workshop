import asyncio
import json

from beeai_framework.adapters.watsonx import WatsonxChatModel
from beeai_framework.backend import (
    ChatModel,
    UserMessage,
    ChatModelNewTokenEvent,
    ChatModelParameters,
    ChatModelSuccessEvent,
)
from beeai_framework.emitter import EventMeta
from beeai_framework.tools import tool
from pydantic import BaseModel


async def task_1() -> None:
    """
    1. Initialize a chat model using the factory method and configure it.
    """
    print("[Task 1] Initializing model via factory method...")
    llm = ChatModel.from_name("ollama:granite3.3:8b")
    print(f"Model initialized: {llm}")


async def task_2() -> None:
    """
    2. Initialize a chat model using a concrete adapter and configure it.
    """
    print("[Task 2] Initializing WatsonxChatModel adapter...")
    llm = WatsonxChatModel(
        "ibm/granite-3-3-8b-instruct",
        api_key="YOUR_API_KEY",
        project_id="YOUR_PROJECT_ID",
        space_id="YOUR_SPACE_ID",
        region="us-south",
        parameters=ChatModelParameters(temperature=0.5),
    )
    print(f"Adapter initialized: {llm}")


async def task_3() -> None:
    """
    3. Perform non-streaming inference.
    """
    print("[Task 3] Non-streaming inference...")
    llm = ChatModel.from_name("ollama:granite3.3:8b")
    response = await llm.create(messages=[UserMessage("Tell me a joke.")])
    print("Response:", response.get_text_content())
    print("Tool Calls:", response.get_tool_calls())
    print("Usage:", response.usage)
    print("Finish Reason:", response.finish_reason)


async def task_4() -> None:
    """
    4. Perform streaming inference and handle new token events.
    """
    print("[Task 4] Streaming inference with event handling...")
    llm = ChatModel.from_name("ollama:granite3.3:8b")
    llm.parameters.stream = True

    def on_new_token(data: ChatModelNewTokenEvent, event: EventMeta) -> None:
        print(f"[Stream] {event.trace.run_id}: {data.value.get_text_content()}")

    # Attach to a concrete run
    response = await llm.create(
        messages=[UserMessage("Tell me a joke.")], stream=True
    ).on("new_token", on_new_token)
    print("Full response (A):", response.get_text_content())

    # Attach to the class emitter
    cleanup = llm.emitter.on("new_token", on_new_token)
    response = await llm.create(messages=[UserMessage("Tell me a joke.")], stream=True)
    print("Full response (B):", response.get_text_content())
    cleanup()

    # Consume stream events directly
    async for data, event in llm.create(
        messages=[UserMessage("Tell me a joke.")], stream=True
    ):
        if isinstance(data, ChatModelNewTokenEvent):
            print(f"[Stream] {event.trace.run_id}: {data.value.get_text_content()}")
        elif isinstance(data, ChatModelSuccessEvent):
            print("Full response (C):", data.value.get_text_content())


async def task_5() -> None:
    """
    5. Structured generation using a Pydantic schema.
    """
    print("[Task 5] Structured generation with Pydantic schema...")

    class Person(BaseModel):
        name: str
        age: int
        country: str
        hobby: str
        favorite_color: str

    llm = ChatModel.from_name("ollama:granite3.3:8b")
    response = await llm.create_structure(
        messages=[UserMessage("Generate profile of a person living in Europe")],
        schema=Person,
    )
    print("Generated Person Profile:")
    print(json.dumps(response.object, indent=2))


async def task_6() -> None:
    """
    6. Use LLMs with tools (function calling).
    """
    print("[Task 6] LLMs and tool usage...")

    @tool
    def get_current_weather(location: str) -> str:
        """
        Returns information about the current weather in the given location.
        """
        return f"In {location} the weather is sunny."

    llm = ChatModel.from_name("ollama:granite3.3:8b")
    response = await llm.create(
        messages=[UserMessage("What's the current weather in Boston?")],
        tools=[get_current_weather],
        tool_choice=get_current_weather,
    )
    print("LLM tool call:")
    tool_call = response.get_tool_calls()[0]
    print(f"Tool Name: {tool_call.tool_name}")
    print(f"Input Args: {tool_call.args}")


async def main() -> None:
    await task_1()
    await task_2()
    await task_3()
    await task_4()
    await task_5()
    await task_6()


if __name__ == "__main__":
    asyncio.run(main())

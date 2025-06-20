import asyncio

from beeai_framework.tools.weather import OpenMeteoTool, OpenMeteoToolInput
from pydantic import BaseModel

from beeai_framework.context import RunContext
from beeai_framework.emitter import Emitter
from beeai_framework.tools import JSONToolOutput, Tool, ToolRunOptions
from beeai_framework.tools.tool import TOutput, tool


async def task_1() -> None:
    """
    1. Play with built-in tools (init, run)
    """
    print("[Task 1] Using built-in OpenMeteoTool...")
    tool = OpenMeteoTool()
    response = await tool.run(OpenMeteoToolInput(location_name="New York"))
    print("Is Empty:", response.is_empty())
    print("Tool Response:", response.get_text_content())


async def task_2() -> None:
    """
    2. Create a tool using the decorator.
    """
    print("[Task 2] Creating a tool with the @tool decorator...")

    @tool
    def get_user() -> dict[str, str]:
        """
        Returns information about the current user.
        """
        return {"name": "John", "location": "Boston"}

    response = await get_user.run({})  # empty input
    print("Is Empty:", response.is_empty())
    print("Tool Response:", response.get_text_content())


async def task_3() -> None:
    """
    3. Create a tool using inheritance.
    """
    print("[Task 3] Creating a tool by inheritance...")

    class UserToolInput(BaseModel):
        id: str

    class UserTool(Tool[UserToolInput, JSONToolOutput]):
        name: str = "get_user"
        description: str = "Get current user by ID"

        @property
        def input_schema(self) -> type[UserToolInput]:
            return UserToolInput

        def _create_emitter(self) -> Emitter:
            return Emitter.root().child(namespace=["tool", "user"], creator=self)

        async def _run(
            self,
            input: UserToolInput,
            options: ToolRunOptions | None,
            context: RunContext,
        ) -> TOutput:
            await context.emitter.emit("my_event", {"key_a": 123, "key_b": 456})
            return JSONToolOutput({"id": input.id, "name": "John Doe"})

    tool = UserTool()
    response = await tool.run(UserToolInput(id="123")).on(
        "my_event",
        lambda data, event: print(data["key_a"], data["key_b"]),
    )
    print("Is Empty:", response.is_empty())
    print("Tool Response:", response.get_text_content())


async def main() -> None:
    await task_1()
    await task_2()
    await task_3()


if __name__ == "__main__":
    asyncio.run(main())

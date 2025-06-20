import asyncio

from pydantic import BaseModel

from beeai_framework.workflows import Workflow

# Tasks
# 1. Motivation
# 2. Create a simple workflow (sync/async steps)
# 3. State modification
# 4. Transitions
# 5. Observability


async def main() -> None:
    class State(BaseModel):
        counter: int

    def first(state: State) -> str:
        if state.counter <= 0:
            return Workflow.END

        print(f"Running first step with counter set to {state.counter}")
        state.counter -= 1
        return "second"  # optional

    async def second(state: State) -> str:
        print("Running second step!")
        state.counter -= 1
        await asyncio.sleep(0.5)
        return "third"  # optional

    async def third(state: State) -> str | None:
        print("Running third step!")
        state.counter -= 1
        await asyncio.sleep(0.5)
        return Workflow.START

    workflow = Workflow(State)
    workflow.add_step("first", first)
    workflow.add_step("second", second)
    workflow.add_step("third", third)
    response = await workflow.run(State(counter=5))
    print(f"Counter is set to {response.state.counter}")


if __name__ == "__main__":
    asyncio.run(main())

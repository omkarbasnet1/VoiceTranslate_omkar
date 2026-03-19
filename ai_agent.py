"""
AI agent for Sprint 3 - Room Booking
setup langchain agent with tools that can check room bookings
how the AI knows what the tool does- @tool
"""

from datetime import datetime
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from Room_booking_skills import (
    load_env,
    do_login,
    available_rooms,
    get_my_bookings,
    reserve_room,
    cancel_my_booking
)

# login first
config = load_env()
if config:
    HOST = config["server_host"]
    TOKEN = do_login(HOST, config["user_email"], config["user_password"])
else:
    HOST = None
    TOKEN = None


@tool
def get_datetime() -> str:
    """Returns the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %I:%M %p")


@tool
def check_available_rooms() -> list:
    """Returns a list of all currently available meeting rooms."""
    if not HOST or not TOKEN:
        return ["Error: Not logged in the server."]

    rooms = available_rooms(HOST, TOKEN)
    return rooms if rooms else []


@tool
def check_my_reservation() -> list:
    """Returns a list of all existing room reservation"""
    if not HOST or not TOKEN:
        return ["Error: Not logged in to the server"]

    bookings = get_my_bookings(HOST, TOKEN)
    return bookings if bookings else []


@tool
def book_meeting_room(room_id: int, iso_time: str) -> str:
    """Books a meeting room"""
    if not HOST or not TOKEN:
        return "Error: Not logged in to the server."

    result = reserve_room(HOST, TOKEN, room_id, iso_time)
    if result:
        return f"Successfully booked room {room_id}. Details:{result}"
    return f"Failed to book room {room_id}"


@tool
def cancel_meeting_reservation(booking_id: int) -> str:
    """Cancel an existing room reservation """
    if not HOST or not TOKEN:
        return "Error: Not logged in to the server."

    success, msg = cancel_my_booking(HOST, TOKEN, booking_id)
    if success:
        return f"Success: {msg}"
    return f"Failed: {msg}"


# ollama config
OLLAMA_MODEL = "granite4:1b"
OLLAMA_BASE_URL = "http://localhost:11434"

agent_tools = [get_datetime, check_available_rooms, check_my_reservation, book_meeting_room, cancel_meeting_reservation]


# create the langchain agent
def setup_agent():
    print(f"Ollama model: {OLLAMA_MODEL}")
    llm = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0
    )

    sys_prompt = (
        " You are a helpful assistant that manages meeting room reservations"
    )

    agent = create_agent(
        model=llm,
        tools=agent_tools,
        system_prompt=sys_prompt
    )
    print("Agent created successfully")
    return agent


# send a question to agent
def ask_agent(agent, prompt_text: str) -> str:
    user_input = {"messages": [HumanMessage(content=prompt_text)]}

    try:
        response = agent.invoke(user_input)
        messages = response.get("messages", [])
        if messages:
            return messages[-1].content  # last message in the list
        else:
            return "sorry could not process that request."

    except Exception as e:
        return f"Agent error: {e}"


# test the agent if its run file directly
if __name__ == "__main__":
    my_agent = setup_agent()
    test_question = "Do i have reservation for tomorrow?"
    print(f"\n User:{test_question}")
    answer = ask_agent(my_agent, test_question)
    print(f"AI: {answer}")

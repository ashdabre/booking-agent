# backend/agent_graph.py

from langgraph.graph import StateGraph, END
from backend.calendar_client import list_free_slots, book_event
import dateparser
from typing import TypedDict, List, Optional

# ----------------------------
# 1. Define the state schema
# ----------------------------

class AgentState(TypedDict, total=False):
    intent: str
    date_start: str
    date_end: str
    suggestions: List[str]
    chosen_start: str
    chosen_end: str
    summary: Optional[str]
    event: dict

# ----------------------------
# 2. Create graph with schema
# ----------------------------

g = StateGraph(AgentState)

# ----------------------------
# 3. Define your node handlers
# ----------------------------

def intent_handler(state: AgentState) -> dict:
    return {"intent": "booking"}

def entity_extraction_handler(state: AgentState) -> dict:
    # Dummy values – replace with actual NER logic
    return {
        "date_start": "tomorrow 10am",
        "date_end": "tomorrow 5pm"
    }

def check_availability(state: AgentState) -> dict:
    start = dateparser.parse(state["date_start"])
    end = dateparser.parse(state["date_end"])
    slots = list_free_slots(start, end)
    return {"suggestions": slots}

def confirm_booking(state):
    print("BOOKING STATE:", state)

    if "date_start" not in state or "date_end" not in state:
        raise ValueError("Missing required keys: 'date_start' or 'date_end'")

    start = dateparser.parse(state["date_start"])
    end = dateparser.parse(state["date_end"])
    event = book_event(start, end, state.get("summary", "Meeting"))
    return {"event": event}



# ----------------------------
# 4. Register nodes
# ----------------------------

g.add_node("intent_recognition", intent_handler)
g.add_node("entity_extraction", entity_extraction_handler)
g.add_node("availability_check", check_availability)
g.add_node("booking_action", confirm_booking)

# ----------------------------
# 5. Define edges
# ----------------------------

g.set_entry_point("intent_recognition")
g.add_edge("intent_recognition", "entity_extraction")
g.add_edge("entity_extraction", "availability_check")
g.add_edge("entity_extraction", "booking_action")
g.set_finish_point("booking_action")

# ----------------------------
# 6. Compile the graph
# ----------------------------

graph = g.compile()

# ----------------------------
# 7. Define runner function
# ----------------------------

def run_agent(user_message: str, context: dict):
    return graph.invoke(context)

from langgraph.graph import START, StateGraph, END
from state import agent_state
from nodes import pro_agent, con_agent, routing, fact_checker, judge

multi_agent_debator=StateGraph(agent_state)

multi_agent_debator.add_node("pro_agent", pro_agent)

multi_agent_debator.add_node("con_agent", con_agent)

multi_agent_debator.add_node("fact_checker", fact_checker)

multi_agent_debator.add_node("judge", judge)


multi_agent_debator.add_edge(START,"pro_agent")

multi_agent_debator.add_edge("pro_agent", "con_agent")


multi_agent_debator.add_conditional_edges(
    "con_agent",
    routing,
    {
        "pro_agent":"pro_agent",
        "con_agent":"con_agent",
        "exit":"fact_checker"
    })
multi_agent_debator.add_edge("fact_checker","judge")
multi_agent_debator.add_edge("judge",END)

debator_graph=multi_agent_debator.compile()


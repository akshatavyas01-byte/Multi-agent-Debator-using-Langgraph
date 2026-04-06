from  graph import debator_graph
from state import agent_state
import streamlit as st

st.header("Live Debator system")

topic=st.text_input("Enter the Topic for debate:")
if "history" not in st.session_state:
    st.session_state.history=[]

def stream(topic:str):    
    query_state:agent_state={
        "topic":topic,
        "deb_round":1
    }
    for step in debator_graph.stream(query_state, stream_mode="updates"):
        for node, state in step.items():
            if node=="pro_agent" and "pro_arguments" in state:
                latest=state["pro_arguments"][-1]
                st.session_state.history.append(f"PRO:{latest}")

            elif node=="con_agent" and "con_arguments" in state:
                latest=state["con_arguments"][-1]
                st.session_state.history.append(f"CON:{latest}")

            elif node=="judge" and "verdict" in state:
                latest=state["verdict"]
                st.session_state.history.append(f"VERDICT:{latest}")

st.button("Debate",on_click=stream, args=[topic,])

for lines in st.session_state.history:
    st.write(lines)
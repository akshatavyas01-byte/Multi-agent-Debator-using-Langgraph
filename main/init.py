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
    debate={
        "topic": topic,
        "pro":[],
        "con":[],
        "verdict":''
    }
    st.session_state.history.insert(0,debate)
    for step in debator_graph.stream(query_state, stream_mode="updates"):
        for node, state in step.items():
            if node=="pro_agent" and "pro_arguments" in state:
                latest=state["pro_arguments"][-1]
                debate["pro"].append(latest)

            elif node=="con_agent" and "con_arguments" in state:
                latest=state["con_arguments"][-1]
                debate["con"].append(latest)

            elif node=="judge" and "verdict" in state:
                latest=state["verdict"]
                debate["verdict"]=latest

st.button("Debate",on_click=stream, args=[topic,])

for debate in st.session_state.history:
    st.markdown(f'## {debate["topic"]}')

    pro_list=debate["pro"]
    con_list=debate["con"]
    
    for i in range(4):
        st.markdown(f"### Round {i}")
        if i<len(pro_list):
            st.markdown(f"**PRO:{pro_list[i]}**")
        if i<len(con_list):
            st.markdown(f"**CON:{con_list[i]}**")
    
    st.markdown(f'## VERDICT:{debate["verdict"]}')
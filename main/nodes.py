from state import agent_state
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from pydantic import SecretStr

from dotenv import load_dotenv
import os

load_dotenv()
groq_api=os.getenv("groq_api")
hf_api=os.getenv("hf_api")

pro_llm=HuggingFaceEndpoint(
    model="zai-org/GLM-5:novita",
    huggingfacehub_api_token=hf_api,
    temperature=0.1,
    top_k=1,
    top_p= 0.9
)
pro_model=ChatHuggingFace(llm=pro_llm)

con_model=ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=SecretStr(groq_api) if groq_api else None,
    temperature=0.1,
    model_kwargs={
        "top_k":1,
        "top_p":0.9
    }
)

def pro_agent(state:agent_state):
    query=state.get("topic")
    prompt0='''You are a professional debater arguing in FAVOR (PRO side).
    TOPIC:
    {topic}

    Instructions:
    - Give a strong opening line on the topic.
    - It should be 1-3 lines long statement in favour of the topic.
    - Do not explain debate or rounds.
    - Only provide the argument.
    '''
    prompt='''You are a professional debater arguing in FAVOR (PRO side).
    TOPIC:
        {topic}
    Opponent's (CON) argument:
        {con}

     Instructions:
    - Directly counter the opponent's argument
    - Strengthen your PRO position
    - Be logical and persuasive
    - It should be 1-3 lines long statement in favour of the topic.
    - Do not explain debate or rounds.
    - Only provide the argument.
    '''
    round=state.get("deb_round")
    pro_facts=state.get("pro_arguments",[])
    con_facts=state.get("con_arguments",[])
    if round and con_facts:
        round_no=int(round)
        fact=str(con_facts[round_no])
        prompt_temp=PromptTemplate(template=prompt, input_variables=["topic"], partial_variables={"con":fact})
        final_prompt=prompt_temp.format(topic=query)
        result=pro_model.invoke(final_prompt)
    else:
        prompt_temp=PromptTemplate(template=prompt0, input_variables=["topic"])
        final_prompt=prompt_temp.format(topic=query)
        result=pro_model.invoke(final_prompt)
    pro_facts.append(result.content)
    return {'pro_arguments':pro_facts}
        



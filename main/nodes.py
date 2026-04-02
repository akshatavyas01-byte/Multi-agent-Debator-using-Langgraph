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
    model="meta-llama/Llama-3.1-8B-Instruct",
    huggingfacehub_api_token=hf_api,
    temperature=0.1,
    top_k=1,
    top_p= 0.9
)
pro_model=ChatHuggingFace(llm=pro_llm)

con_model=ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=SecretStr(groq_api) if groq_api else None,
    temperature=0.1 
)

def pro_agent(state:agent_state):
    query=state.get("topic")
    prompt0='''You are a professional debater arguing in FAVOR (PRO side).
    TOPIC:
    {topic}

    Instructions:
    - Give a direct, practical argument (NOT a speech)
    - It should be 1-3 lines long statement in favour of the topic.
    - Do not explain debate or rounds.
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

    '''
    round=state.get("deb_round")
    pro_facts=state.get("pro_arguments",[])
    con_facts=state.get("con_arguments",[])
    if round and len(con_facts) >= round:
        fact=str(con_facts[round-1])
        prompt_temp=PromptTemplate(template=prompt, input_variables=["topic"], partial_variables={"con":fact})
        final_prompt=prompt_temp.format(topic=query)
        result=pro_model.invoke(final_prompt)
    else:
        prompt_temp=PromptTemplate(template=prompt0, input_variables=["topic"])
        final_prompt=prompt_temp.format(topic=query)
        result=pro_model.invoke(final_prompt)
    pro_facts.append(str(result.content))
    print(pro_facts)
    
    return {'pro_arguments':pro_facts}
        


def con_agent(state:agent_state):
    query=state.get("topic")
    con_facts=state.get("con_arguments",[])
    round=state.get("deb_round")
    pro_facts=state.get("pro_arguments")
    prompt=''' You are a professional debater arguing AGAINST the topic (CON side).
    Opponent's (PRO) statement:
    {pro}
    Topic:
    {topic}
     Instructions:
    - Directly counter the opponent's argument
    - Strengthen your CON position
    - Be logical and persuasive
    - It should be 1-3 lines long statement against the topic.
    - Do not explain debate or rounds.
    - Only provide the argument.
    '''
    if pro_facts and round:
         fact=str(pro_facts[round-1])
         prompt_temp=PromptTemplate(template=prompt, input_variables=["topic"], partial_variables={"pro":fact})
         final_prompt=prompt_temp.format(topic=query)
         result=con_model.invoke(final_prompt)
         con_facts.append(str(result.content))
        
    return {'con_arguments':con_facts}


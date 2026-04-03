from state import agent_state, Fact
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.output_parsers import JsonOutputParser

import wikipedia
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

retriever= WikipediaRetriever(wiki_client=wikipedia, top_k_results=2)

parser=JsonOutputParser(pydantic_object=Fact)

def pro_agent(state:agent_state):
    query=state.get("topic")
    prompt0='''You are a professional debater arguing in FAVOR (PRO side).
    TOPIC:
    {topic}

    Instructions:
    - Give a direct, practical argument (NOT a speech)
    - It should be 1 line long statement in favour of the topic.
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
    - It should be 1 line long statement in favour of the topic.
    - Do not explain debate or rounds.

    '''
    round=state.get("deb_round")
    pro_facts=state.get("pro_arguments",[])
    con_facts=state.get("con_arguments",[])
    if round and len(con_facts) == round:
        fact=str(con_facts[round-1])
        prompt_temp=PromptTemplate(template=prompt, input_variables=["topic"], partial_variables={"con":fact})
        final_prompt=prompt_temp.format(topic=query)
        result=pro_model.invoke(final_prompt)
        round+=1
    else:
        prompt_temp=PromptTemplate(template=prompt0, input_variables=["topic"])
        final_prompt=prompt_temp.format(topic=query)
        result=pro_model.invoke(final_prompt)
    pro_facts.append(str(result.content))
    return {'pro_arguments':pro_facts,"deb_round":round}
        


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
    - It should be 1 line long statement against the topic.
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


def routing(state:agent_state):
    round=state.get("deb_round")
    pro_facts=state.get("pro_arguments",[])
    con_facts=state.get("con_arguments",[])
    if round and round<=6:
        if len(pro_facts)> len(con_facts):
            return "con_agent"
        elif len(pro_facts)==len(con_facts):
            return "pro_agent"
    else:
        return "exit"
    
def fact_checker(state:agent_state):
    query=state.get("topic")
    pro_facts=state.get("pro_arguments",[])
    con_facts=state.get("con_arguments",[])
    if pro_facts and con_facts and query:
        docs=retriever.invoke(query)
        content= "\n".join([doc.page_content[:500] for doc in docs])
        arguments= pro_facts + con_facts
        prompt_temp=''' Your a professional factchecker that will check the given facts with the help of wikipedia content:
        Wikipedia content:
        {content}
        
        Arguments:
        {arguments}

        For each argument in the list of Arguments give a verdict in Literals True, False and Needs Verification
        Use the following instructions to generate Json for each argument:
        {instructions}
        Do Not:
        - Over explain yourself
        - Only follow the instructions
        - Do not add any code.
        '''
        prompt=PromptTemplate(template=prompt_temp, input_variables=["content","arguments"], partial_variables={"instructions": parser.get_format_instructions()})
        chain=prompt | pro_model| parser
        result=chain.invoke({"content":content,"arguments":arguments})
        return {"facts":result}

def judge(state:agent_state):
    query=state.get("topic")
    facts=state.get("facts")
    prompt=''' Your a professional Judge that will decide who wins the Debate.
    The desicion will be based on the results of factchecker agents verified facts.
    Topic:
    {topic}
    Fact Checker Result:
    {facts}
        
    You should return the answer on which side won "PRO" or "CON" and state a reson why the won.
    example:"PRO" Side won as most of their statements were true and they stated better facts than "CON" side.
    Do Not:
    - Over explain your reason.
    - Only 2 lines qat most for explaination.
    - Use a professional tone
    '''
    prompt_temp=PromptTemplate(template=prompt,input_variables=["topic","facts"])
    final_prompt=prompt_temp.format(topic=query, facts=facts)
    result=con_model.invoke(final_prompt)
    return {"verdict":result.content} 

        

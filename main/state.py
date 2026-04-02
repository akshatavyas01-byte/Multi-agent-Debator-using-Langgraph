from typing import TypedDict

class agent_state(TypedDict, total=False):
    topic:str
    pro_agruments:list[str]
    con_arguments:list[str]
    deb_round:int
    facts:list[dict]
    verdict:str

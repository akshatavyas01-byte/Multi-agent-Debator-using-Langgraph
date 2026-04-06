from typing import TypedDict, Literal
from pydantic import BaseModel, Field

class Fact(BaseModel):
    argument: str=Field(description="The argument that needs to be classified.")
    classification:Literal["True","False","Needs Verification"]=Field(description="The arguments need to be classified into literals 'True','False' and 'Needs Verification'.")

class agent_state(TypedDict, total=False):
    topic:str
    pro_arguments:list[str]
    con_arguments:list[str]
    deb_round:int
    facts:Fact
    verdict:str

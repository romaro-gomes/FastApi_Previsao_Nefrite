from pydantic import BaseModel
class Inflamation(BaseModel):
    temperature:float
    nausea:str
    lumbar_pain:str
    urine_pushing:str
    micturition_pain:str
    burning_urethra:str
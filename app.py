from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from inflamation_features import Inflamation

import pandas as pd
import pickle

app = FastAPI()

templates = Jinja2Templates(directory="templates")

model = pickle.load(open('model.pkl','rb'))
preprocessor=pickle.load(open('preprocessor.pkl','rb'))

def get_values(data):
    return [getattr(data, field) for field in data.__annotations__.keys()]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/predict")
async def predict(request: Request,
                    temperature: float = Form(...),
                    nausea: str = Form(...),
                    lumbar_pain: str = Form(...),
                    urine_pushing: str = Form(...),
                    micturition_pain: str = Form(...),
                    burning_urethra: str = Form(...)):
    if temperature < 35 or temperature > 42:
        raise HTTPException(status_code=400, detail="A temperatura deve estar entre 35 e 42 graus Celsius.")
    
    data = Inflamation(
        temperature=temperature,
        nausea=nausea,
        lumbar_pain=lumbar_pain,
        urine_pushing=urine_pushing,
        micturition_pain=micturition_pain,
        burning_urethra=burning_urethra
    )

    data_df = pd.DataFrame([get_values(data)], columns=data.__annotations__.keys())
    data_processed=preprocessor.transform(data_df)
    prediction = model.predict(data_processed)
    proba=model.predict_proba(data_processed)
    probability=f"{proba.tolist()[0][1]:.2f}% {proba.tolist()[0][0]:.2f}%"
    if prediction[0] == 0:
        pred='Negativo'
    else:
        pred='Positivo'
    return templates.TemplateResponse("predict.html", {"request": request, "prediction": pred, "probability":probability} )
                                      
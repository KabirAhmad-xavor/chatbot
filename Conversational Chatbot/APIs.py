# daily_life_activity_data_api.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
from fastapi import FastAPI, HTTPException
app = FastAPI(title="Daily Life Activity Data API")
from fastapi.responses import JSONResponse
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
df = pd.read_csv("activities.csv")

# Preprocess the data to get activity blocks with start and end times
def get_activity_blocks(data):
    data = data.copy()
    data['Activity_Group'] = (data['Activity'] != data['Activity'].shift()) | (data['Place'] != data['Place'].shift())
    data['Group_ID'] = data['Activity_Group'].cumsum()

    grouped_df = data.groupby('Group_ID').agg(
        id=('id', 'first'),
        Activity=('Activity', 'first'),
        Place=('Place', 'first'),
        Start_Time=('timestamp', 'first'),
        End_Time=('timestamp', 'last')
    ).reset_index(drop=True)

    return grouped_df

# Get preprocessed activity blocks
activity_blocks_df = get_activity_blocks(df)

@app.get("/")
def root():
    return {"message": "Welcome to Daily Life Activity Data API"}

@app.get("/activities/all")
def get_all_activity_blocks():
    return activity_blocks_df.to_dict(orient="records")

# @app.get("/activities/by-user/{user_id}")
# def get_activities_by_user(user_id: int):
#     filtered = df[df['id'] == user_id]
#     return filtered.to_dict(orient="records")

# @app.get("/activities/by-activity/{activity}")
# def get_by_activity(activity: str):
#     filtered = df[df['Activity'].str.lower() == activity.lower()]
#     return filtered.to_dict(orient="records")


#uvicorn activities_api:app --reload

df2 = pd.read_csv("report_data.csv")  # Make sure this path is correct

# Replace NaNs with None
df2 = df2.where(pd.notnull(df2), None)

# Convert each row into dictionary format (records list)
data_list = df2.to_dict(orient="records")

@app.get("/gait_data", response_class=JSONResponse)
def get_all_gait_data():
    return data_list
# @app.get("/data/{parameter}")
# def get_specific_data(parameter: str):
#     if parameter in data_dict2:
#         return {parameter: data_dict2[parameter]}
#     else:
#         raise HTTPException(status_code=404, detail="Parameter not found")

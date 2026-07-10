from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from feast import FeatureStore
import uvicorn

app = FastAPI(title="Census Income Prediction API")
store = FeatureStore(repo_path=".")


class PredictionRequest(BaseModel):
    user_id: int


class PredictionResponse(BaseModel):
    user_id: int
    age: int
    occupation: str
    education_num: int
    hours_per_week: int
    predicted_income: str


@app.get("/")
def read_root():
    return {"message": "Census Income Prediction API", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        features = store.get_online_features(
            features=[
                "census_features:age",
                "census_features:occupation",
                "census_features:education_num",
                "census_features:hours_per_week",
                "census_features:income"
            ],
            entity_rows=[{"user_id": request.user_id}]
        ).to_dict()

        return PredictionResponse(
            user_id=request.user_id,
            age=features["age"][0],
            occupation=features["occupation"][0],
            education_num=features["education_num"][0],
            hours_per_week=features["hours_per_week"][0],
            predicted_income=features["income"][0]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("Starting Feast Feature Server...")
    print("API Documentation: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
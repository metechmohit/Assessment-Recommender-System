from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class AssessmentResponse(BaseModel):
    url: str
    adaptive_support: str
    description: str
    duration: int
    remote_support: str
    test_type: list[str]

class RecommendationResponse(BaseModel):
    recommended_assessments: list[AssessmentResponse]

from pydantic import BaseModel, Field



class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=5)
    category_id: int



class QuestionResponse(BaseModel):
    id: int
    text: str
    model_config = {
        "from_attributes": True
    }

class MessageResponse(BaseModel):
    message: str


class CategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
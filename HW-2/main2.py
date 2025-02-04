from pydantic import BaseModel, EmailStr, field_validator, Field
import json


class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)



class User(BaseModel):
    name: str = Field(..., min_length=2, pattern=r'^[a-zA-Z ]+$')
    age: int = Field(..., gt=0, lt=120)
    email: EmailStr
    is_employed: bool
    address: Address


    @field_validator('is_employed')
    @classmethod
    def validate_is_employed(cls, is_employed, info):
        already_validate = info.data
        age = already_validate['age']
        if (age < 18 or age > 65) and is_employed:
            raise ValueError('age must be between 18 and 65')
        return is_employed

def check_data(data):
    user = User.model_validate_json(data)
    return user.model_dump_json()

if __name__ == '__main__':
    json_input = """{
        "name": "John Dow",
        "age": 65,
        "email": "john.doe@example.com",
        "is_employed": true,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""
    print(check_data(json_input))

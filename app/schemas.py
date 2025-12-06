from pydantic import BaseModel, Field, constr, field_validator


class Record(BaseModel):
    number: str
    address: str = Field(..., min_length=5, max_length=50)

    @field_validator("number")
    @classmethod
    def validate_number(cls, v):
        if not v.isdigit():
            raise ValueError("Номер должен содержать только цифры")
        if not (6 <= len(v) <= 11):
            raise ValueError("Номер должен содержать от 6 до 11 цифр")
        return v
from pydantic import BaseModel, Field, field_validator


class AddressCreate(BaseModel):
    name: str
    street: str
    city: str
    country: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @field_validator("name", "street", "city", "country")
    @classmethod
    def must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field must not be blank")
        return v.strip()


class AddressUpdate(BaseModel):
    name: str | None = None
    street: str | None = None
    city: str | None = None
    country: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class AddressOut(BaseModel):
    id: int
    name: str
    street: str
    city: str
    country: str
    latitude: float
    longitude: float

    model_config = {"from_attributes": True}

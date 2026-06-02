from pydantic import BaseModel, EmailStr, Field, field_validator


class AddressCreate(BaseModel):
    name: str
    street: str
    city: str
    country: str

    email: EmailStr
    phone: str

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @field_validator("name", "street", "city", "country")
    @classmethod
    def must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field must not be blank")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        phone = v.strip()

        if not phone.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(phone) != 10:
            raise ValueError("Phone number must be 10 digits")

        return phone


class AddressUpdate(BaseModel):
    name: str | None = None
    street: str | None = None
    city: str | None = None
    country: str | None = None

    email: EmailStr | None = None
    phone: str | None = None

    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return v

        if not v.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(v) != 10:
            raise ValueError("Phone number must be 10 digits")

        return v


class AddressOut(BaseModel):
    id: int
    name: str
    street: str
    city: str
    country: str
    email: str
    phone: str
    latitude: float
    longitude: float

    model_config = {"from_attributes": True}
from log import get_logger
from fastapi import APIRouter, Depends, HTTPException
from geopy.distance import geodesic
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Address
from schemas import AddressCreate, AddressOut, AddressUpdate

logger = get_logger(__name__)

router = APIRouter()


# Check whether the provided email or phone number
# already exists in the database.
# exclude_id is used during update operations to
# ignore the current record being updated.
async def check_duplicate_contact(
    db: AsyncSession,
    email: str | None,
    phone: str | None,
    exclude_id: int | None = None,
):
    conditions = []

    if email:
        conditions.append(Address.email == email)

    if phone:
        conditions.append(Address.phone == phone)

    if not conditions:
        return

    query = select(Address).where(or_(*conditions))

    if exclude_id is not None:
        query = query.where(Address.id != exclude_id)

    result = await db.execute(query)
    existing = result.scalar_one_or_none()

    if existing:
        if email and existing.email == email:
            raise HTTPException(
                status_code=400,
                detail=f"Email '{email}' already exists"
            )

        if phone and existing.phone == phone:
            raise HTTPException(
                status_code=400,
                detail=f"Phone '{phone}' already exists"
            )


# Create a new address record.
# Before inserting, validate that email and phone
# are unique across the table.
@router.post("/", response_model=AddressOut, status_code=201)
async def create_address(
    payload: AddressCreate,
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Creating address for '{payload.name}'")

    await check_duplicate_contact(
        db=db,
        email=payload.email,
        phone=payload.phone
    )

    address = Address(**payload.model_dump())

    db.add(address)
    await db.commit()
    await db.refresh(address)

    logger.info(f"Address created with id={address.id}")

    return address


# Fetch all address records from the database.
@router.get("/", response_model=list[AddressOut])
async def list_addresses(db: AsyncSession = Depends(get_db)):
    logger.info("Fetching all addresses")

    result = await db.execute(select(Address))

    return result.scalars().all()


# Fetch a single address using its primary key.
@router.get("/{address_id}", response_model=AddressOut)
async def get_address(
    address_id: int,
    db: AsyncSession = Depends(get_db)
):
    address = await db.get(Address, address_id)

    if not address:
        logger.warning(f"Address id={address_id} not found")
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    return address


# Partially update an existing address.
# Only fields provided by the client are updated.
@router.patch("/{address_id}", response_model=AddressOut)
async def update_address(
    address_id: int,
    payload: AddressUpdate,
    db: AsyncSession = Depends(get_db)
):
    address = await db.get(Address, address_id)

    if not address:
        logger.warning(
            f"Update failed — id={address_id} not found"
        )
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    # Extract only fields supplied in request body
    updates = payload.model_dump(exclude_unset=True)

    # Check whether updated email/phone
    # already belongs to another record.
    await check_duplicate_contact(
        db=db,
        email=updates.get("email"),
        phone=updates.get("phone"),
        exclude_id=address_id,
    )

    # Dynamically update fields
    for field, value in updates.items():
        setattr(address, field, value)

    await db.commit()
    await db.refresh(address)

    logger.info(f"Address id={address_id} updated")

    return address


# Delete an address by id.
@router.delete("/{address_id}", status_code=200)
async def delete_address(
    address_id: int,
    db: AsyncSession = Depends(get_db)
):
    address = await db.get(Address, address_id)

    if not address:
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    await db.delete(address)
    await db.commit()

    logger.info(f"Address id={address_id} deleted")

    return {
        "message": "Address deleted successfully"
    }


# Find all addresses within the specified radius
# from the given latitude and longitude.
@router.get("/nearby/search", response_model=list[AddressOut])
async def find_nearby(
    latitude: float,
    longitude: float,
    distance_km: float,
    db: AsyncSession = Depends(get_db),
):
    logger.info(
        f"Nearby search: lat={latitude}, "
        f"lon={longitude}, "
        f"within {distance_km}km"
    )

    result = await db.execute(select(Address))
    all_addresses = result.scalars().all()

    origin = (latitude, longitude)

    # Calculate geographical distance between
    # source coordinates and each saved address.
    nearby = [
        addr
        for addr in all_addresses
        if geodesic(
            origin,
            (addr.latitude, addr.longitude)
        ).km <= distance_km
    ]

    logger.info(
        f"Found {len(nearby)} addresses "
        f"within {distance_km}km"
    )

    return nearby
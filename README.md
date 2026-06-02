# Address Book API

A simple REST API to manage addresses with coordinates and proximity search.

## Setup

```bash
git clone https://github.com/chikkurs/AddressBook.git
cd AddressBook

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
```

## Run

```bash
uvicorn main:app --reload
```

Open http://localhost:8000/docs for the Swagger UI.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /addresses/ | Create an address |
| GET | /addresses/ | List all addresses |
| GET | /addresses/{id} | Get one address |
| PATCH | /addresses/{id} | Update an address |
| DELETE | /addresses/{id} | Delete an address |
| GET | /addresses/nearby/search | Find addresses within a distance |

## Nearby Search Example

```
GET /addresses/nearby/search?latitude=40.7128&longitude=-74.0060&distance_km=10
```

Returns all addresses within the given radius using real geodesic distance (not flat math).

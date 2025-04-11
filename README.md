---

# OfferWall Admin Panel

This is a Django 5.1.7 application built with Python 3.12 and Django REST Framework (DRF) to manage offer walls and associated offers. The project provides an API for retrieving offer walls, their assigned offers, and offer details. It includes Docker support for production and development environments.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Models](#models)
- [API Endpoints](#api-endpoints)
- [Docker Setup](#docker-setup)
- [Development](#development)
- [License](#license)

---

## Features
- Manage offer walls with UUID-based tokens and associated offers.
- Support for multiple offer types via `OfferChoices` enum.
- API endpoints to retrieve offer walls by token or URL, and list available offer names.
- Dockerized setup for production and development with Nginx and PostgreSQL.
- Automatic ordering of offers within an offer wall.

---

## Requirements
- Python 3.12
- Django 5.1.7
- Django REST Framework (DRF)
- Docker (optional, for containerized deployment)
- PostgreSQL

See `requirements.txt` for a full list of dependencies.

---

## Installation

### Manual Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by copying `.env.example` to `.env` and filling in the values:
   ```bash
   cp .env.example .env
   ```

5. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## Models

### `OfferChoices`
An enumeration of available offer types used in the `Offer` model.

- **Fields**: 34 predefined choices (e.g., `Loanplus`, `SgroshiCPA2`, `Moneyveo`, etc.).
- **Usage**: Provides a controlled list of offer names.

### `OfferWall`
Represents an offer wall with a unique token and associated offers.

- **Fields**:
  - `token`: UUID (Primary Key)
  - `name`: CharField (max_length=255, optional)
  - `url`: URLField (optional)
  - `description`: TextField (optional)
- **Methods**:
  - `add_offer(offer, order)`: Adds an offer to the wall with an optional order.
  - `reorder_offers(offer_order_list)`: Reorders offers based on a list of UUIDs.
  - `get_offers()`: Returns ordered list of assigned offers.

### `Offer`
Represents an individual offer with details like name, URL, and loan terms.

- **Fields**:
  - `uuid`: UUID (Primary Key)
  - `id`: IntegerField (non-primary key)
  - `url`: URLField (optional)
  - `is_active`: BooleanField (default=True)
  - `name`: CharField (choices from `OfferChoices`, unique)
  - `sum_to`: CharField (optional)
  - `term_to`: IntegerField (optional)
  - `percent_rate`: IntegerField (optional)

### `OfferWallOffer`
A junction table linking `OfferWall` and `Offer` with ordering.

- **Fields**:
  - `offer_wall`: ForeignKey to `OfferWall`
  - `offer`: ForeignKey to `Offer`
  - `order`: PositiveIntegerField (default=0)
- **Meta**:
  - Unique together constraint on `(offer_wall, offer)`.
  - Default ordering by `order`.

---

## API Endpoints

The API is built using DRF ViewSets and is accessible via the `/offerwalls/` base path.

### `OfferWallViewSet`
- **Authentication**: None (public access via `AllowAny`).
- **Permissions**: Publicly accessible.
- **Lookup Field**: `token`.

#### Endpoints:
1. **Retrieve OfferWall by Token**
   - **URL**: `/offerwalls/<token>/`
   - **Method**: GET
   - **Response**: Details of the offer wall, including assigned offers sorted by order.
   - **Example**:
     ```json
     {
       "token": "550e8400-e29b-41d4-a716-446655440000",
       "name": "Sample OfferWall",
       "url": "https://example.com",
       "description": "A sample offer wall",
       "offer_assignments": [
         {
           "offer": {
             "uuid": "123e4567-e89b-12d3-a456-426614174000",
             "id": 1,
             "url": "https://loanplus.com",
             "is_active": true,
             "name": "Loanplus",
             "sum_to": "10000",
             "term_to": 30,
             "percent_rate": 5
           }
         }
       ]
     }
     ```

2. **Retrieve OfferWall by URL**
   - **URL**: `/offerwalls/by_url/<url>/`
   - **Method**: GET
   - **Response**: Same as above, filtered by URL.

3. **Get Offer Names**
   - **URL**: `/offerwalls/get_offer_names/`
   - **Method**: GET
   - **Response**: List of available offer names from `OfferChoices`.
   - **Example**:
     ```json
     {
       "offer_names": ["Loanplus", "SgroshiCPA2", "Moneyveo"]
     }
     ```

---

## Docker Setup

### Production
1. Build and run the production stack:
   ```bash
   docker-compose up --build
   ```
2. Access the app at `http://localhost:8000` (or `https://localhost:443` if Nginx SSL is configured).

- **Services**:
  - `admin_panel`: Runs Django with Gunicorn.
  - `nginx`: Serves static files and proxies requests.

### Development
1. Use the development compose file:
   ```bash
   docker-compose -f docker-compose.dev.yaml up --build
   ```
2. Access the app at `http://localhost:8000`.

- **Services**:
  - `postgres`: PostgreSQL database.
  - `admin_panel`: Django with hot-reload.
  - `nginx`: Static file serving and proxy.

### Environment Variables
Copy `.env.example` to `.env` and configure:
```
DB_NAME=<database-name>
DB_USER=<database-user>
DB_PASSWORD=<database-password>
DB_HOST=<database-host>
DB_PORT=<database-port>
SECRET_KEY=<django-secret-key>
```

For development, additional variables are prefixed with `_DEV`.

---

## Development

### Running Locally
1. Ensure PostgreSQL is running or use SQLite for simplicity.
2. Apply migrations:
   ```bash
   python manage.py migrate
   ```
3. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Adding New Offers
- Update `OfferChoices` in `models.py` to include new offer types.
- Run migrations if model changes are made:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

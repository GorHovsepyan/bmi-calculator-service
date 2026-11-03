# BMI Calculator Service

A small HTTP service that calculates body mass index and returns a category.

## Endpoints

### GET /

Returns basic information about the service.

### GET /health

Returns the service status.

### POST /calculate

Request body:

```json
{
  "weight_kg": 70,
  "height_cm": 175
}
```

Response:

```json
{
  "bmi": 22.86,
  "category": "Normal weight"
}
```

## Run with Python

```bash
python app.py
```

The service will run at `http://localhost:8000`.

## Build and run with Docker

```bash
docker build -t bmi-calculator-service .
docker run --name bmi-service -p 8000:8000 bmi-calculator-service
```

Test it with curl:

```bash
curl -X POST http://localhost:8000/calculate -H "Content-Type: application/json" -d '{"weight_kg":70,"height_cm":175}'
```

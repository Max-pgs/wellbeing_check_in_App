# API Contract (API-lite via JsonResponse)

Base path: `/checkins/api/`

All endpoints require authentication.

---

## GET /progress/

Query parameters:
- `from` (optional, YYYY-MM-DD)
- `to` (optional, YYYY-MM-DD)

Response 200:

{
    "from": "2026-02-01",
    "to": "2026-02-28",
    "count": 1,
    "averages": {
        "energy": 10.0,
        "mood": 10.0,
        "activity": 10.0
    }
}

Error 400:

{ "error": "Invalid date format. Use YYYY-MM-DD for 'from' and 'to'." }

---

## GET /checkins/

Query parameters:
- `from` (optional, YYYY-MM-DD)
- `to` (optional, YYYY-MM-DD)

Response 200:

{
    "from": "2026-02-01",
    "to": "2026-02-28",
    "count": 1,
    "items": [
        {
            "id": 3,
            "checkin_date": "2026-02-24",
            "energy_score": 10,
            "mood_score": 10,
            "activity_score": 10,
            "notes": ""
        }
    ]
}

Error 400:

{ "error": "Invalid date format. Use YYYY-MM-DD for 'from' and 'to'." }
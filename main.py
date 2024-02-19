from fastapi import FastAPI

from utils import get_zipcode, get_location_ids_by_zipcode, next_available_appointment_at_location


app = FastAPI()


@app.get("/v1/soonest-available-appointment")
async def soonest_available_appointment(latitude: float, longitude: float) -> dict:
    # This could likely be rewritten to have all the API fetch requests in parallel
    appointments = [
        next_available_appointment_at_location(location_id)
        for location_id in get_location_ids_by_zipcode(get_zipcode(latitude, longitude))
    ]
    soonest = min(appointments, key=lambda x: x["epoch_time"])
    return {
        "location_id": soonest["location_id"],
        "appointment_time": soonest["epoch_time"]
    }

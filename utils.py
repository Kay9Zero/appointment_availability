import csv

import requests

import googlemaps

import settings


ZIP_TO_LOCATIONS_CACHE = {}

def get_zipcode(latitude: float, longitude: float) -> int:
    """
    :param latitude:
    :param longitude:
    :return: int, the zip code corresponding to the given latitude and longitude
    """
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
    return next(
        address_component["long_name"]
        for address_component in reverse_geocode_result[0]["address_components"]
        if "postal_code" in address_component["types"]
    )


def get_location_ids_by_zipcode(zipcode: int) -> set:
    """
    :param zipcode:
    :return: set, the set of all locations associated with a zipcode
    """
    if not ZIP_TO_LOCATIONS_CACHE:
        with open(settings.LOCATION_ZIP_CSVFILE, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                if line["zip_code"] not in ZIP_TO_LOCATIONS_CACHE:
                    ZIP_TO_LOCATIONS_CACHE[line["zip_code"]] = []
                ZIP_TO_LOCATIONS_CACHE[line["zip_code"]].append(line["location_id"])
    return set(ZIP_TO_LOCATIONS_CACHE.get(zipcode))


def next_available_appointment_at_location(location_id: str) -> dict:
    """
    :param location_id:
    :return: dict, the next available appointment
    """
    url = f"https://{settings.SOLV_HEALTH_API_HOST}/partner/next-available/py67ev"
    payload = requests.get(url=url).json()[0]
    payload["location_id"] = location_id
    return payload

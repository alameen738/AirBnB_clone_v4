#!/usr/bin/python3
"""New view for Places objects that handles all default Restful API actions"""
from flask import Flask, Blueprint, abort, jsonify, request
from models import storage, Place, State, City, Amenity

app = Flask(__name__)
app.url_map.strict_slashes = False
bp = Blueprint('places', __name__, url_prefix='/api/v1')


@bp.route('/places_search', methods=['POST'])
def places_search():
    """Search for places based on given criteria"""
    request_json = request.get_json()
    if not request_json:
        abort(400, description='Not a JSON')

    states_ids = request_json.get('states', [])
    cities_ids = request_json.get('cities', [])
    amenities_ids = request_json.get('amenities', [])

    # Retrieve all places if no criteria is provided
    if not (states_ids or cities_ids or amenities_ids):
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    # Filter places by states
    places = []
    for state_id in states_ids:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                places.extend(city.places)

    # Filter places by cities
    for city_id in cities_ids:
        city = storage.get(City, city_id)
        if city:
            places.extend(city.places)

    # Remove duplicate places
    places = list(set(places))

    # Filter places by amenities
    if amenities_ids:
        filtered_places = []
        for place in places:
            amenities = {amenity.id for amenity in place.amenities}
            if set(amenities_ids).issubset(amenities):
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])


# Register blueprint
app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

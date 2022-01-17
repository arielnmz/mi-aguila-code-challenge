import json
import requests

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse


@csrf_exempt
def reverse_geocode_postcodes_batch(request):
    if request.method == "POST":
        # Expect a JSON array in the POST body
        geolocations = json.loads(request.body)

        # Pass the geolocations object to the external API to get the result
        result = requests.post("http://api.postcodes.io/postcodes", json=geolocations)

        if result.ok:
            # Process each result and assert whether there was a result for the geolocation using a generator
            def _query_response_gen(data):
                for postcode_response in data:
                    query = postcode_response["query"]
                    reverse_geocoded = postcode_response["result"]

                    # Use a tuple representation of the lon, lat as id for the result
                    _id = ", ".join(map(str, (query["longitude"], query["latitude"])))

                    is_ok = reverse_geocoded is not None

                    if reverse_geocoded:
                        # Use the first result's postcode as the final result
                        geocoded = reverse_geocoded[0]["postcode"]
                    else:
                        geocoded = ""

                    yield {"id": _id, "ok": is_ok, "geocoded": geocoded}

            result_data = result.json()
            # Resolve the generator into a list
            geolocations = list(_query_response_gen(result_data["result"]))

            return JsonResponse({"ok": True, "geolocations": geolocations})

    return HttpResponse("Bad request", status=400)

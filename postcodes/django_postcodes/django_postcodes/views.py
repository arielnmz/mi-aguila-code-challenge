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

        return JsonResponse({"ok": True, "geolocations": result.json()})

    return HttpResponse("Bad request", status=400)

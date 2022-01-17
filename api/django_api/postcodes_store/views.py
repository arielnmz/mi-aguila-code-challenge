import csv
import requests
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from postcodes_store.api_tools import get_geolocations_gen
from django_api.forms import CsvUploadForm

# Cross-application model usage is discouraged but we aim for simplicity for now
from postcodes_store.models import Postcode

GEOCODE_CHUNK_SIZE = 10


@csrf_exempt
def request_postcodes_from_csv(request):
    if request.method == "POST":
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"]

            # Store file in a file REQ: Receive file and store it
            with Path("postcodes.csv").open("wb") as f:
                for chunk in csv_file.chunks():
                    f.write(chunk)

            # Read back from the created file to process the CSV
            with Path("postcodes.csv").open("r") as f:
                csv_reader = csv.reader(f)

                # Skip head
                next(csv_reader)

                # Process the contents of the CSV in chunks of GEOCODE_CHUNK_SIZE geolocations to improve efficiency

                # First create a generator that returns chunks of GEOCODE_CHUNK_SIZE geolocations
                _geolocations_gen = get_geolocations_gen(csv_reader, GEOCODE_CHUNK_SIZE)

                # Continuously take from the geolocations generator until the data source is exhausted
                while True:
                    geolocations = next(_geolocations_gen)

                    # End loop if the geolocations source is exhausted
                    if not geolocations:
                        break

                    # Generate a request object to pass to the postcodes microservice
                    payload = {
                        "geolocations": [
                            {"longitude": lon, "latitude": lat}
                            for lat, lon in geolocations
                        ]
                    }

                    result = requests.post(
                        f"{settings.POSTCODES_SERVICE_URL}/postcodes/reverse_geocode_postcodes_batch/",
                        json=payload,
                    )

                    if result.ok:
                        # Process resulting geolocations and store in the DB
                        postcodes_result = result.json()
                        for geolocation in postcodes_result["geolocations"]:
                            postcode = Postcode(
                                key=geolocation["id"],
                                ok=geolocation["ok"],
                                geocoded=geolocation["geocoded"],
                            )
                            postcode.save()

                    else:
                        return HttpResponse(
                            f"There were some errors during processing of the CSV. Code: {result.status_code}"
                        )

                return HttpResponse(
                    "Process finished, you can see the results in the database"
                )

    return HttpResponse("Bad request", status=400)

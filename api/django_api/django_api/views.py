import csv
from pathlib import Path

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django_api.forms import CsvUploadForm


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
                _ = 0
                # Skip head
                next(csv_reader)

                for row in csv_reader:
                    lat, lon = row
                    print(lat, lon)

                    _ += 1
                    if _ > 9:
                        break

                return HttpResponse("Hello, world. You're at the polls index.")

    return HttpResponse("Bad request", code=400)

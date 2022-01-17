import csv
from codecs import iterdecode
from pathlib import Path
from tempfile import TemporaryFile

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django_api.forms import CsvUploadForm


@csrf_exempt
def request_postcodes_from_csv(request):
    if request.method == "POST":
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"]
            csv_reader = csv.reader(iterdecode(csv_file, "utf-8"))
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

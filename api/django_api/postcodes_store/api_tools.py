from itertools import islice


def get_geolocations_gen(data_source, chunk_size=2):
    def _gen():
        rows = islice(data_source, chunk_size)
        while True:
            yield [(lat, lon) for lat, lon in rows]

    return _gen()

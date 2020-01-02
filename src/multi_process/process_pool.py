from os import environ
from multiprocessing import Pool

import googlemaps

client = googlemaps.Client(key=environ['GMAP_API_KEY'])

PLACES = (
    'Reykjavik', 'Vien', 'Zadar', 'Venice',
    'Wrokaw', 'Bolognia', 'Berlin', 'Tokyo',
    'New York', 'Dehli',
)

POOL_SIZE = 4


def present_result(geocoded):
    print(
        f"{geocoded['formatted_address']:>50s}, {geocoded['geometry']['location']['lat']:6.2f}, {geocoded['geometry']['location']['lng']:6.2f}")


def fetch_place(place):
    return client.geocode(place)[0]


def main():
    with Pool(POOL_SIZE) as pool:
        results = pool.map(fetch_place, PLACES)

    for result in results:
        present_result(result)


if __name__ == '__main__':
    main()

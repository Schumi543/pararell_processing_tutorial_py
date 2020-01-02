import time
from threading import Thread

import googlemaps
from os import environ

client = googlemaps.Client(key=environ['GMAP_API_KEY'])

PLACES = (
    'Reykjavik', 'Vien', 'Zadar', 'Venice',
    'Wrokaw', 'Bolognia', 'Berlin', 'Tokyo',
    'New York', 'Dehli',
)


def fetch_place(place):
    geocoded = client.geocode(place)[0]

    # from pprint import pprint
    # pprint(geocoded)

    print(
        f"{geocoded['formatted_address']:>50s}, {geocoded['geometry']['location']['lat']:6.2f}, {geocoded['geometry']['location']['lng']:6.2f}")


def main():
    threads = []
    for place in PLACES:
        thread = Thread(target=fetch_place, args=[place])
        thread.start()
        threads.append(thread)

    while threads:
        threads.pop().join()


if __name__ == '__main__':
    started = time.time()
    main()
    elapsed = time.time() - started

    print()
    print(f"time_elapsed:{elapsed:.2f}")

from queue import Queue, Empty
import time
from threading import Thread

import googlemaps
from os import environ

from throttle import Throttle

THREAD_POOL_SIZE = 8

client = googlemaps.Client(key=environ['GMAP_API_KEY'])

PLACES = (
    'Reykjavik', 'Vien', 'Zadar', 'Venice',
    'Wrokaw', 'Bolognia', 'Berlin', 'Tokyo',
    'New York', 'Dehli',
) * 5


def worker(work_queue, results_queue, throttle):
    while not work_queue.empty():
        try:
            item = work_queue.get(block=False)
        except Empty:
            break
        else:
            throttle.consume()  # default consume_amount = 1

            try:
                result = fetch_place(item)
            except Exception as err:
                results_queue.put(err)
            else:
                results_queue.put(result)
            finally:
                work_queue.task_done()


def present_result(geocoded):
    from pprint import pprint
    print(
        f"{geocoded['formatted_address']:>50s}, {geocoded['geometry']['location']['lat']:6.2f}, {geocoded['geometry']['location']['lng']:6.2f}")


def fetch_place(place):
    return client.geocode(place)[0]


def main():
    work_queue = Queue()
    results_queue = Queue()
    throttle = Throttle(10)

    for place in PLACES:
        work_queue.put(place)

    threads = [
        Thread(target=worker, args=(work_queue, results_queue, throttle))
        for _ in range(THREAD_POOL_SIZE)
    ]

    for thread in threads:
        thread.start()

    work_queue.join()

    while threads:
        threads.pop().join()

    while not results_queue.empty():
        present_result(results_queue.get())


if __name__ == '__main__':
    started = time.time()
    main()
    elapsed = time.time() - started

    print()
    print(f"time_elapsed:{elapsed:.2f}s")

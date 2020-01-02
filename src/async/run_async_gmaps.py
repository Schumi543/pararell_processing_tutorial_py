import asyncio
from asyncgmaps import geocode, session

PLACES = (
    'Reykjavik', 'Vien', 'Zadar', 'Venice',
    'Wrokaw', 'Bolognia', 'Berlin', 'Tokyo',
    'New York', 'Dehli',
)


async def present_result(result):
    geocoded = await result
    print(
        f"{geocoded['formatted_address']:>50s}, {geocoded['geometry']['location']['lat']:6.2f}, {geocoded['geometry']['location']['lng']:6.2f}")


async def fetch_place(place):
    return (await geocode(place))[0]


async def main():
    await asyncio.wait([
        present_result(fetch_place(place))
        for place in PLACES
    ])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    # ClientSessionが閉じられていないとaiohttpが例外を出すため sessionを明示的に閉じる
    loop.run_until_complete(session.close())
    loop.close()

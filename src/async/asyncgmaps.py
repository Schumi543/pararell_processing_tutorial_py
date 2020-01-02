from os import environ
import aiohttp

session = aiohttp.ClientSession()


async def geocode(place):
    params = {'address': place, 'key': environ['GMAP_API_KEY']}
    async with session.get(
            'https://maps.googleapis.com/maps/api/geocode/json',
            params=params
    ) as response:
        result = await response.json()
        return result['results']

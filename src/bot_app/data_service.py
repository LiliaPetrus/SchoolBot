import aiohttp
from . settings import SCHOOL_API_URL_SECTIONS, SCHOOL_API_URL_ENROLLMENT


async def get_sections_json():
    async with aiohttp.ClientSession() as session:
        async with session.get(SCHOOL_API_URL_SECTIONS) as response:
            return await response.json()


async def get_sections() -> list:
    sections_json = await get_sections_json()

    sections = []
    for section in sections_json:
        sections.append({"id": section.get('id'), "code": section.get('code'), "name": section.get('name'), \
                         "free_places": section.get('free_places')})

    return sections


async def post_enrollment(data) -> int:
    async with aiohttp.ClientSession() as session:
        headers = {'content-type': 'application/json'}
        async with session.post(url=SCHOOL_API_URL_ENROLLMENT, data=data, headers=headers) as response:
            return response.status

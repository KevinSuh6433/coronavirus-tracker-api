"""app.routers.v1.py"""
from fastapi import APIRouter

from ..services.location.jhu import get_category
from ..services.location import LocationService

V1 = APIRouter()


class OutputsAbstract():
    def showOutput(self):
        raise NotImplemented()


class Bridge(OutputsAbstract):
    def __init__(self) -> None:
        self.implemntation = None


class OutputAll(Bridge):
    def __init__(self, implementation: LocationService):
        self.implemntation = implementation

    @V1.get("/all")
    async def showOutput():
        """Get all the categories."""
        confirmed = await get_category("confirmed")
        deaths = await get_category("deaths")
        recovered = await get_category("recovered")

        return {
            # Data.
            "confirmed": confirmed,
            "deaths": deaths,
            "recovered": recovered,
            # Latest.
            "latest": {
                "confirmed": confirmed["latest"],
                "deaths": deaths["latest"],
                "recovered": recovered["latest"],
            },
        }


class OutputConfirmed(Bridge):
    def __init__(self, implementation: LocationService):
        self.implemntation = implementation

    @V1.get("/confirmed")
    async def showOutput():
        """Confirmed cases."""
        confirmed_data = await get_category("confirmed")

        return confirmed_data


class OutputDeaths(Bridge):
    def __init__(self, implementation: LocationService):
        self.implemntation = implementation

    @V1.get("/deaths")
    async def showOutput():
        """Total deaths."""
        deaths_data = await get_category("deaths")

        return deaths_data


class OutputRecovered(Bridge):
    def __init__(self, implementation: LocationService):
        self.implemntation = implementation

    @V1.get("/recovered")
    async def showOutput():
        """Recovered cases."""
        recovered_data = await get_category("recovered")

        return recovered_data

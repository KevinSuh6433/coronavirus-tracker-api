"""app.location"""
from datetime import time
from ..coordinates import Coordinates
from ..utils import countries
from ..utils.populations import country_population
from abc import ABCMeta, abstractmethod
import copy


class IProtoType(metaclass=ABCMeta):
    "interface with clone method"
    @staticmethod
    @abstractmethod
    def clone():
        """The clone, deep or shallow.
        It is up to you how you want to implement
        the details in your concrete class"""

# pylint: disable=redefined-builtin,invalid-name


class Location(IProtoType):  # pylint: disable=too-many-instance-attributes
    """
    A location in the world affected by the coronavirus.
    """

    def __init__(
        self, id, country, province, coordinates, last_updated, confirmed, deaths, recovered, timelines
    ):  # pylint: disable=too-many-arguments
        # General info.
        self.id = id
        self.country = country.strip()
        self.province = province.strip()
        self.coordinates = coordinates

        # Last update.
        self.last_updated = last_updated

        # Statistics.
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered

        # Set timelines.
        self.timelines = timelines

    def clone(self):
        " This clone method uses a shallow copy technique "
        return type(self)(
            copy.deepcopy(self.id),
            copy.deepcopy(self.country),
            copy.deepcopy(self.province),
            copy.deepcopy(self.coordinates),

            # Last update.
            copy.deepcopy(self.last_updated),

            # Statistics.
            copy.deepcopy(self.confirmed),
            copy.deepcopy(self.deaths),
            copy.deepcopy(self.recovered)
        )

    @property
    def country_code(self):
        """
        Gets the alpha-2 code represention of the country. Returns 'XX' if none is found.

        :returns: The country code.
        :rtype: str
        """
        return (countries.country_code(self.country) or countries.DEFAULT_COUNTRY_CODE).upper()

    @property
    def country_population(self):
        """
        Gets the population of this location.

        :returns: The population.
        :rtype: int
        """
        return country_population(self.country_code)

    def serialize(self):
        """
        Serializes the location into a dict.

        :returns: The serialized location.
        :rtype: dict
        """
        return {
            # General info.
            "id": self.id,
            "country": self.country,
            "country_code": self.country_code,
            "country_population": self.country_population,
            "province": self.province,
            # Coordinates.
            "coordinates": self.coordinates.serialize(),
            # Last updated.
            "last_updated": self.last_updated,
            # Latest data (statistics).
            "latest": {
                "confirmed": self.confirmed,
                "deaths": self.deaths,
                "recovered": self.recovered,
            },
            "timelines": {
                # Serialize all the timelines.
                key: value.serialize()
                for (key, value) in self.timelines.items()
            },
        }


location = Location()
timelinedLocation = location.clone()
timelinedLocation.confirmed = timelinedLocation.timelines.get("confirmed").latest
timelinedLocation.deaths = timelinedLocation.timelines.get("deaths").latest
timelinedLocation.recovered = timelinedLocation.timelines.get("recovered").latest

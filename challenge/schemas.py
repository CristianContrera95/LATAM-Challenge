from typing import List

from pydantic import BaseModel

from .exceptions import BadRequestException


class ColumnsSchema(BaseModel):
    OPERA : str
    TIPOVUELO : str
    MES : int

    @property
    def _airlines(self) -> List:
        return ['American Airlines', 'Air Canada', 'Air France', 'Aeromexico',
         'Aerolineas Argentinas', 'Austral', 'Avianca', 'Alitalia',
         'British Airways', 'Copa Air', 'Delta Air', 'Gol Trans', 'Iberia',
         'K.L.M.', 'Qantas Airways', 'United Airlines', 'Grupo LATAM',
         'Sky Airline', 'Latin American Wings', 'Plus Ultra Lineas Aereas',
         'JetSmart SPA', 'Oceanair Linhas Aereas', 'Lacsa']

    @property
    def _flight_types(self) -> List:
        return ['I', 'N']

    def validate_fields(self):
        if (self.OPERA not in self._airlines) or \
            (self.TIPOVUELO not in self._flight_types) or \
            (self.MES not in range(1, 13)):
            raise BadRequestException("Values has wrong values")

class PredictSchema(BaseModel):
    flights: List[ColumnsSchema]

    def validate_schema(self):
        for c in self.flights:
            c.validate_fields()

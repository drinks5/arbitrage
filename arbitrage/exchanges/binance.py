import typing
from .base import Exchange


class Binance(Exchange):
    def __init__(self, exchangeId: types.ExchangeId):
        self.id = exchangeId
        self.ws = None
        self.rest = None
        self.endpoint = {
            'private': cctx[exchangeId](privateKey),
            'ws': ws,
            'rest': rest
        }

    def getFee(self, rate: float) -> typing.List(float):
        return [rate * 0.1, rate * 0.05]

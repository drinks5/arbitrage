
# encoding: utf-8

class Rate(object):
    @staticmethod
    def convert(rateQuote: types.RateQuote) => int:
        amount = rateQuote.amount
        if rateQuote.side == 'buy':
            return amount / rateQuote.exchangeRate
        return amount * rateQuote.exchangeRate

    @staticmethod
    def convertAmount(price: int, cost: int, side: str) => int:
        if side == 'buy':
            return cost * price
        return cost / price

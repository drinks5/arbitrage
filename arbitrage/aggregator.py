class Aggregator(object):
    async def getMarkets(exchange: types.Exchange) -> types.Pairs:
        api = exchange.endpoint.public or exchange.endpoint.private
        if not api:
            return
        return api.loadMarkets()

    async def getAllTickers(exchange: types.Exchange,
                            extTickers: types.ExchangeTicker) -> types.Tickers:
        try:
            api = exchange.endpoint.public or exchange.endpoint.private
            if not api or not exchange.pairs:
                return
            return api.fetchTickers()
        except Exception:
            from traceback import format_exc
            logger.error('getAllTickers异常:\n%s' % format_exc())

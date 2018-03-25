import ccxt.async as ccxt


class Api(object):
    def __init__(self):
        pass

    async def getBalance(self, exchange: types.Exchange):
        api = exchange.endpoint.private
        if not api:
            return
        return await api.getBalance()

    async def getFreeAmount(self, exchange: types.Exchange, coin: types.Coin):
        balances = await this.getBalance(exchange)
        if not balances:
            return
        asset = balances[coin]
        if not asset:
            logger.debug(f'尚未持有币种{coin}')
            return
        return asset.free

    async def createOrder(self, exchange: types.Exchange, order: types.Order):
        api = exchange.endpoint.private
        if not api:
            return
        return await api.createOrder(order.symbol, order.type, order.side,
                                     order.amount, order.price)

    async def fetchOrder(self, exchange: types.Exchange, orderId: str,
                         symbol: str):
        api = exchange.endpoint.private
        if not api:
            return
        return await api.fetchOrder(orderId, symbol)

    async def fetchOrderStatus(self, exchange: types.Exchange, orderId: str,
                               symbol: str):
        api = exchange.endpoint.private
        if not api:
            return
        return await api.fetchOrder(orderId, symbol)

class Event(object):
    def __init__(self):
        pass

    async def onPlaceOrder(self, exchang: types.Exchange, cycle: types.Cycle):
        logger.debug('订单开始')
        await self.trading.placeOrder(exchang, cycle)
        logger.debug('订单结束')

    async def onUpdateArbitage(self, ranks: types.Rank):
        if not ranks:
            return
        return await self.trading.storage.rank.putRanks(ranks)

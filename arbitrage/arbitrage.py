import config
from .aggregator import Aggregator
from .engine import Engine
from .event import Event


class TriangularArbitrage(object):
    exchanges = {}

    worker = 0
    engineClass = Engine
    aggregatorClass = Aggregator

    def __init__(self):
        self.activeExchangeId = config.exchange.active
        self.engine = Engine()
        self.aggregator = self.aggregatorClass()

    async def start(activeExchangeId: types.ExchangeId):
        logger.debug('启动三角套利机器人[开始]')
        try:
            await this.initExchange(this.activeExchangeId)
            this.worker = this.estimate.bind(this,
                                             config.arbitrage.interval * 1000)
            logger.info('----- 机器人启动完成 -----')
        except Exception:
            from traceback import format_exc
            logger.error('机器人运行出错: \n%s' % format_exc())

    async def initExchange(self, exchangeId: types.ExchangeId):
        logger.debug('初始化交易所[启动]')
        markets = {}
        if self.exchanges.get(exchangeId):
            return
        try:
            exchange = Helper.getExchange(exchangeId)
            if not exchange:
                logger.debug(f'获取exchange失败, exchangeId: {exchangeId}')
                return
            api = exchange.endpoint.public or exchange.endpoint.private
            if api:
                exchange.pairs = await this.aggregator.getMarkets(exchange)
                if not exchange.pairs:
                    return
                baseCoins = Helper.getMarketCoines(exchange.pairs.keys())
                for baseCoin in baseCoins:
                    if not markets[baseCoin]:
                        markets[baseCoin] = []
                    pairKeys = filter(lambda x: baseCoin in x, exchange.pairs)
                    for key in pairKeys:
                        markets[baseCoin].append(exchange.pairs[key])
                    exchange.markets = markets
            self.exchanges.set(exchangeId, exchange)
            logger.debug('初始化交易所[终了]')
        except Exception:
            from traceback import format_exc
            logger.error('初始化交易所[异常]:\n%s' % format_exc())

    async def estimate(tickers: types.ExchangeTicker):
        logger.debug('监视行情[开始]')
        try:
            logger.info('----- 套利测算 -----')
            allTickers = await this.aggregator.getAllTickers(exchange, tickers)
            if not allTickers:
                return
            candidates = await this.engine.getCandidates(exchange, allTickers)
            if not candidates:
                return
            ranks = Helper.getRanks(exchange.id, candidates)
            if config.storage.tickRank and ranks:
                this.emit('updateArbitage', ranks)
            if ranks[0]:
                firstCandidate, profitRate = candidates[0].id, ranks[
                    0].profitRate[0]
                logger.info(
                    f'选出套利组合第一名：{firstCandidate}, 预测利率(扣除手续费): {profitRate}')
                this.emit('placeOrder', exchange, firstCandidate)

            output = candidates[:5]
            for candidate in output:
                clcRate = candidate.rate
                path = candidate.id
                logger.info(f'路径：{path} 利率: ${clcRate}')
            logger.debug('监视行情[终了]')
        except Exception:
            from traceback import format_exc
            logger.error('监视行情[异常]:\n%s' % format_exc())

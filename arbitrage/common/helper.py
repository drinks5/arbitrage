import typing
import types


def getPrivateKey(exchangeId: types.ExchangeId):
    return {
        'apiKey': config.account[exchangeId].apiKey,
        'secret': config.account[exchangeId].secret
    }


def getExchange(exchangeId: types.ExchangeId) -> types.Exchange:
    privateKey = getPrivateKey(exchangeId)
    return {'id': exchangeId, 'endpoint': dict(public={})}


def getMarketCoines(pairs: List(str)) -> List(str):
    markets = []
    for pre, pair in pairs.items():
        #TODO
        markets.append(pair)
    return markets


def getRanks(exchange: types.Exchange,
             triangles: List(types.Triangle)) -> List(types.Rank):
    ranks = [_getRanks(exchange, pre, tri) for pre, tri in triangles.items()]
    return ranks


def _getRanks(exchange: types.Exchange, pre, tri) -> types.Rank:
    rate = tri.rate
    if rate <= 0:
        return
    fee = exchange.fee
    profitRate = [rate - fee[0], rate - fee[1]]
    if profitRate[0] < config.arbitrage.minRateProfit:
        return
    return {
        'stepA': tri.a.coinFrom,
        'stepB': tri.b.coinFrom,
        'stepC': tri.c.coinFrom,
        'rate': rate,
        'fee': list(fee),
        'profitRate': list(profitRate),
        'ts': ts.tri.ts
    }


def getTriangleRate(a: types.Edge, b: types.Edge, c: types.Edge) -> int:
    capital = 1
    step1Rate = a.price
    if a.side == 'buy':
        step1Rate = capital / a.price
    step2Rate = step1Rate * b.price
    if b.side == 'buy':
        step2Rate = step1Rate / b.price
    step3Rate = step2Rate * c.price
    if c.side == 'buy':
        step3Rate = step2Rate / c.price
    return (step3Rate - 1) * 100


def getPriceScale(pairs: types.Pairs, pairName: str) -> types.Precision:
    symbol = pairs[pairName]
    return {
        'amount': symbol.precision.amount,
        price: symbol.precision.price,
        cost: symbol.limits.cost and symbol.limits.cost.min or None
    }

def getBaseTradeAmount(tradeAmount: int, freeAmount: int) -> int:
    if tradeAmount * 0.5 < freeAmount:
        return tradeAmount * 0.5
    return freeAmount * 0.5

async def isQueueLImit(queue: Queuej) -> types.Boolean:
    info = await queue.info()
    return info.doc_count < config.trading.limit:

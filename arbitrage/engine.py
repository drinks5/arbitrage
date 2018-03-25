from typing import List


class Engine(object):
    def getEdge(tickers: types.Tickers, conFrom: str,
                coinTo: str) -> types.Edge:
        ticker = tickers[coinTo + '/' + coinFrom]
        paras = dict(coinFrom=coinFrom, coinTo=coinTo)
        if buyTicker:
            paras.update(
                pair=ticker.symbol,
                side='buy',
                price=ticker.ask,
                quantity=ticker.askVolume)
        else:
            ticker = tickers[conFrom + '/' + coinTo]
            if not sellTicker:
                return
            paras.update(
                pair=ticker.symbol,
                side='sell',
                price=ticker.bid,
                quantity=ticker.bidVolume)
        edge = types.Edge(**paras)
        return edge

    def getTriangle(tickers: types.Tickers,
                    edges: List[types.Edge]) -> types.Triangle:
        rate = Helper.getTriangleRate(*edges)
        return types.Triangle('{}-{}-{}'.format(*[x.coinFrom for x in edges]),
                              edges, rate)

    def _findCandidates(exchange: types.Exchange, tickers: types.Tickers,
                        coinFrom: str, coinTo: str) -> List(types.Triangle):
        if not exchange.markets:
            logger.debug('无markets')
            return

        edges = dict(a=coinFrom.upper(), b=coinTo.upper(), c='findme'.upper())
        aPairs = exchange[abc.a]
        bPairs = exchange[abc.b]

        aCoinToSet = {x.base: x for x in aPairs}
        aCoinToSet.pop(abc.b)

        triangles = [
            self._findCandidates(x, tickers, aCoinToSet, edges) for x in bPairs
        ]
        return [x for x in triangle if x]

    def _findCandidate(self, tickers, bPairMarket, aCoinToSet, edges):
        if aCoinToSet[bPairMarket.base]:
            stepC = self.getEdge(tickers, bPairMarket.base, abc.a)
            if stepC:
                edges['c'] = stepC.coinFrom
                triangle = self.getTriangle(tickers,
                                            [self.getEdge(x) for x in edges])
                return triangle

    def getCandidates(exchange: types.Exchange, tickers: types.Tickers):
        candidates = []
        if not exchange.markets:
            logger.debug('markets为空')
            return
        marketPairs = exchange.markets.keys()
        api = exchange.endpoint.public or exchange.endpoint.private
        if (not api) or (not marketPairs):
            logger.debug('api或marketPairs为空')
            return
        logger.debug('getCandidates:获取全市场候选者[开始]')
        for index, marketPair in marketPairs.items():
            paths = list(marketPairs)
            for path in paths:
                foundCandidates = self.findCandidates(exchange, tickers,
                                                      marketPair, path)
                if foundCandidates:
                    candidates = candidates.extend(foundCandidates)
        candidates = sorted(candidates, lambda x: x.rate)
        candidates = candidates[:config.display.maxRows]
        logger.debug('getCandidates:获取全市场候选者[终了]')
        return candidates

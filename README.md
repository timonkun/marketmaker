# MarketMaker
做市商程序

# 模块划分     
exchange: 封装主流交易所，如bitfinex,binance,huobi，提供实时价格和交易手数等信息。   
market: 目标交易所，封装其交易接口。   
strategy: 做市商策略，如刷单、深度做市。   
statistics: 数据统计模块。   

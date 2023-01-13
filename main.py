###
# Algorithmic Trading Bot
###
import alpaca.common.exceptions

import AlpacaAPI
import TradingAlgorithm
import math

position_size_dollars = 5000

if __name__ == '__main__':
    tradeable_assets = AlpacaAPI.get_tradeable_assets()

    count = 0
    for asset in tradeable_assets:
        should_buy = TradingAlgorithm.should_buy(asset.symbol)
        if should_buy:
            # check for free buying power
            # TODO compare against buying power not cash
            account = AlpacaAPI.trading_client.get_account()
            if (5000 < float(account.cash)):
                # if we can buy fractionable shares
                # buy $position_share_dollars
                if asset.fractionable:
                    # TODO Dont buy if position already open
                    AlpacaAPI.buy_dollars(asset.symbol, position_size_dollars)
                # else calculate the maximum number of whole shares
                # we can buy for $position_share_dollars
                else:
                    quote = AlpacaAPI.get_latest_quote(asset.symbol)
                    shares = math.floor(position_size_dollars / quote)
                    AlpacaAPI.buy_shares(asset.symbol, shares)
        # if we don't want to buy, then we don't want to hold TODO make a hold vs sell algorithm
        # so close any open position we have open of symbol
        elif any(position.symbol == asset.symbol for position in AlpacaAPI.get_positions()):
            AlpacaAPI.close_position(asset.symbol)

import requests
import json

def get_fee(count, price):
    fee_per = 0.05
    return ((count * price) / 100) * fee_per

def pjson(jobj):
    print(json.dumps(jobj, indent=2))

if __name__ == "__main__":
    url = "https://api.upbit.com/v1/candles/days?market=KRW-XRP&count=10&to=2022-04-10T00:00:01Z"
    headers = {"Accept": "application/json"}
    response_text = requests.get(url, headers=headers).text
    response = json.loads(response_text)

    total_yield_val = 0
    total_yield_ratio = 1.0

    for i in range(0, len(response) - 1):
        print("------")
        today_candle = response[i]
        yesterday_candle = response[i + 1]

        '''
        pjson(today_candle)
        pjson(yesterday_candle)
        '''

        print("> today")
        print(today_candle["candle_date_time_kst"])
        print("> yesterday")
        print(yesterday_candle["candle_date_time_kst"])

        k = 0.5
        today_open = today_candle["opening_price"]
        yesterday_high = yesterday_candle["high_price"]
        yesterday_low = yesterday_candle["low_price"]
        target = ((yesterday_high - yesterday_low) * k) + today_open

        print("> target price")
        print(target)

        print("> buy price(target price + fee)")
        buy_price = target + get_fee(1, target)
        print(buy_price)

        today_high = today_candle["high_price"]

        buy = today_high > target

        if buy:
            print("> ***** buy *****")

            print("> close price")
            today_close = today_candle["trade_price"]
            print(today_close)
            
            print("> sell price")
            sell_price = today_close - get_fee(1, today_close)
            print(sell_price)
            
            print("> yield val")
            yield_val = sell_price - buy_price
            total_yield_val += yield_val
            print(yield_val)

            print("> yield ratio")
            yield_ratio = sell_price / buy_price
            total_yield_ratio *= yield_ratio
            print(yield_ratio)

    print("")
    print("> total yield val")
    print(total_yield_val)
    print("> total yield ratio")
    print(total_yield_ratio)

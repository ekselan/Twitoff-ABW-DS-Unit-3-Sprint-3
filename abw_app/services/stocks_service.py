
import requests 
import json

API_KEY = "abc123" #todo:set as env var

symbol = "AMZN" # input("Please enter a stock symbol")

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AMZN&interval=5min&apikey=abc123"

response = requests.get(request_url)

print(type(response))
#> class 'requests.models.Response'
print(response.status_code) #> 200
print(type(response.text)) #> string


parsed_response = json.loads(response.text)
print(type(parsed_response)) #> dict

breakpoint()

latest_close = parsed_response["Time Series (Daily)"]
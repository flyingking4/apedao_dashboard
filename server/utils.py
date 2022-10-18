import json
import jshelper as js
import requests as http

COIN_TYPE_USD  = "usd"
COIN_TYPE_IOTA = "iota"
COIN_TYPE_SMR  = "smr"

RET_CODE_SUCCESS               = 0
RET_CODE_FAILURE               = 1
RET_CODE_ARG_FAIL              = 2

RET_CODE_LIST = [
    "success.",
    "generic failure.",
    "problem with arguments"
]

def getKeyFromJson(js, key, defaultValue=None):
    retVal = defaultValue
    if key in js:
        retVal = js[key]
    return retVal

def getReturnStatusJson(retCode, jsonTail=None):
    retObject  = {}
    if RET_CODE_SUCCESS == retCode:
        retObject['status'] = 'success'
    else :
        retObject['status'] = 'failure'
    retObject['message'] = RET_CODE_LIST[retCode]
    # append extra json if provided
    if None != jsonTail :
        retObject = {**retObject, **jsonTail}
    return json.dumps(retObject)

def getTreasury():
  iotaWallets = "iota1qz3fjx6u6evpur39fw5lp5xjgelalhw0ckghwpcsf30su8nkermvy4v9066,iota1qpx492dh4c2a9ngtmt69vf6yf0tdj96qhvy3rn6573ajkck96d7kj6hkh0v,iota1qzja7syt4las56p0tv0u0fm74mxzgf0y3z0pjgtjj2a9hc8d6cf2568kw3m"
  smrWallets = "smr1qzh0kkkutk38ewdddr4vg3c7sl3l63yfctwhyyvm80cdjryptm86kdksmxu"
  # iota
  iotaBalance = 0
  retJson = js.getBalance("iota", iotaWallets)
  for w in iotaWallets.split(',') :
    iotaBalance = iotaBalance + retJson[w]
  # smr
  smrBalance = 0
  retJson = js.getBalance("smr", smrWallets)
  for w in smrWallets.split(',') :
    smrBalance = smrBalance + retJson[w]
  retJson = { "treasury" : { "iota" : iotaBalance, "smr" : smrBalance } }
  return retJson

def getPrice(coinType) :
  priceBuy = None
  ticker = 'tIOTUSD' if coinType == 'iota' else 'tSMRUSD'
  r = http.get(url = 'https://api-pub.bitfinex.com/v2/ticker/' + ticker, params = {})
  if (r.status_code == 200) :
    json = r.json()
    priceBuy = json[0]
  return priceBuy 

def getCollectionStats():
  retJson = {}
  r = http.get(url = 'https://api.labralords.com/collections/3e54e728-53bb-4892-aa13-2fc5c3172cf6/stats', params = {})
  if (r.status_code != 200) :
    return utils.getReturnStatusJson(utils.RET_CODE_FAILURE, {})
  json = r.json()
  retJson['listingCount'] = json['data']['listingCount']
  retJson['floorPrice'] = json['data']['floorPrice']
  retJson['uniqueHolders'] = json['data']['uniqueHolders']
  retJson['oneHourSales'] = json['data']['oneHourSales']
  retJson['oneDaySales'] = json['data']['oneDaySales']
  retJson['sevenDaySales'] = json['data']['sevenDaySales']
  # add last trade
  r = http.get(url = 'https://api.labralords.com/collections/3e54e728-53bb-4892-aa13-2fc5c3172cf6/trades?limit=1', params = {})
  if (r.status_code == 200) :
    json = r.json()
    json = json['data'][0] # we only have one entry
    print(json)
    lastSellJson = {}
    lastSellJson['name'] = json['name']
    lastSellJson['mediaUri'] = json['mediaUri']
    lastSellJson['token'] = json['token']
    lastSellJson['price'] = json['price']
    lastSellJson['rank'] = json['rank']
    lastSellJson['timestamp'] = json['timestamp']
    retJson['lastSell'] = lastSellJson
  return retJson

def getTickersStats():
  retJson = {}
  #bitforex
  rate_smr_bitforex_buy = rate_smr_bitforex_sell = 0.0
  r = http.get(url = 'https://api.bitforex.com/api/v1/market/ticker?symbol=coin-usdt-smr', params = {})
  if (r.status_code == 200) :
    json = r.json()
    rate_smr_bitforex_buy = json['data']['buy']
    rate_smr_bitforex_sell = json['data']['sell']
  retJson['rate_smr_iota_bitforex_buy'] = rate_smr_bitforex_buy
  retJson['rate_smr_iota_bitforex_sell'] = rate_smr_bitforex_sell
  #bitfinex
  rate_smr_bitfinex_buy = rate_smr_bitfinex_sell = 0.0
  r = http.get(url = 'https://api-pub.bitfinex.com/v2/ticker/tSMRUSD', params = {})
  if (r.status_code == 200) :
    json = r.json()
    rate_smr_bitfinex_buy = json[0]
    rate_smr_bitfinex_sell = json[2]
  retJson['rate_smr_iota_bitfinex_buy'] = rate_smr_bitfinex_buy
  retJson['rate_smr_iota_bitfinex_sell'] = rate_smr_bitfinex_sell
  #iota rate
  rate_iota_bitfinex_buy = 0
  r = http.get(url = 'https://api-pub.bitfinex.com/v2/ticker/tIOTUSD', params = {})
  if (r.status_code == 200) :
    json = r.json()
    rate_iota_bitfinex_buy = json[0]
  retJson['rate_iota_usd_bitfinex_buy'] = rate_iota_bitfinex_buy
  #iotabee
  rate_smr_iotabee_buy = rate_smr_iotabee_sell = 0.0
  amount_to_buy = 100
  slippage=0.01
  r = http.get(url = 'https://api.iotabee.com/public/pair?coin1=IOTA&coin2=SMR', params = {})
  if (r.status_code == 200) :
    json = r.json()
    _feeRate = json["data"]["fee_rate"]
    _iotaReserve = int(json["data"]["reserve1"])
    _smrReserve = int(json["data"]["reserve2"])
    _fee = _feeRate * amount_to_buy
    #iota to SMR
    _expIotaAmt = _iotaReserve - ((_iotaReserve * _smrReserve)/(amount_to_buy - _fee + _smrReserve))
    rate_smr_iotabee_buy = _expIotaAmt*(1-slippage)
    rate_smr_iotabee_buy = rate_smr_iotabee_buy / amount_to_buy # normalize
    #SMR to iota
    _expSmrAmt = _smrReserve - ((_iotaReserve * _smrReserve)/(amount_to_buy - _fee + _iotaReserve))
    rate_smr_iotabee_sell = _expSmrAmt*(1-slippage)
    rate_smr_iotabee_sell = rate_smr_iotabee_sell / amount_to_buy # normalize
  retJson['rate_smr_iota_iotabee_buy'] = rate_smr_iotabee_buy
  retJson['rate_smr_iota_iotabee_sell'] = rate_smr_iotabee_sell
  return retJson




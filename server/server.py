from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from waitress import serve
import threading

import utils

app = Flask(__name__)
CORS(app)

@app.route('/v1/say_hi', methods=['GET'])
def sayHi():
    print(request.args.get('a1'))
    print(request.args.get('b1'))
    return "hi"

# coinType : 'smr'/'iota'
# addrList : '
@app.route('/v1/get_balance', methods=['GET'])
def getBalance():
  coinType = utils.getKeyFromJson(request.args, "coinType", utils.COIN_TYPE_IOTA)
  addrList = utils.getKeyFromJson(request.args, "addrList", None)
  print(coinType, addrList)
  if (addrList == None) :
    return utils.getReturnStatusJson(utils.RET_CODE_ARG_FAIL, {})
  retJson = js.getBalance(coinType, addrList)
  return utils.getReturnStatusJson(utils.RET_CODE_SUCCESS, {"balances":retJson})

@app.route('/v1/get_treasury', methods=['GET'])
def getTreasury():
  retJson = utils.getTreasury()
  return utils.getReturnStatusJson(utils.RET_CODE_SUCCESS, retJson)

@app.route('/v1/get_collection_stats', methods=['GET'])
def getCollectionStats():
  retJson = utils.getCollectionStats()
  return utils.getReturnStatusJson(utils.RET_CODE_SUCCESS, {"collection_stats" : retJson})

@app.route('/v1/get_tickers_stats', methods=['GET'])
def getTickersStats():
  retJson = utils.getTickersStats()
  return utils.getReturnStatusJson(utils.RET_CODE_SUCCESS, {"tickers_stats" : retJson})

if __name__ == '__main__':
  #app.run(host='0.0.0.0', port=5000)
  serve(app, host="0.0.0.0", port=8050)

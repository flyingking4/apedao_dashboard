const {SingleNodeClient} = require("@iota/iota.js");
const {addressBalance} = require("@iota/iota.js");
const axios = require('axios')

async function getBalances(coinType, addrList) {
  ret = {}
  var smrNodeUrl = "https://shimmer-node.tanglebay.com";
  var iotaNodeUrl = "https://iota-node.tanglebay.com/api/v1/addresses/";
  const client = new SingleNodeClient(smrNodeUrl);
  for (let s = 0; s < addrList.length; s++) {
    addr = addrList[s];
    _balance = -1
    try {
      if(coinType == "iota") {
	_res = await axios.get(iotaNodeUrl + addr);
        _balance = _res.data['data']['balance']
      } else if(coinType == "smr") {
        _res = await addressBalance(client, addr);
        _balance = parseInt(_res['balance']['value'].toString())
      }
    } catch(err) { continue };
    if(_balance >= 0.0) ret[addr] = _balance
  }
  return ret;
}

(async () => {
  coinType = process.argv[2];
  addrList = process.argv[3].split(',');
  res = await getBalances(coinType, addrList);
  console.log(JSON.stringify(res))
  process.exit(1);
})()


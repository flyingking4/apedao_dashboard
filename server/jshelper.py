import subprocess

def getBalance(coinType, addrList):
  result = subprocess.run(['node', 'js/getBalances.js', coinType, addrList], stdout=subprocess.PIPE)
  retJson = eval(result.stdout.decode('utf-8'))
  return retJson




const Web3 = require("web3");
const quorumjs = require("quorum-js");
const web3 = new Web3("http://foodchain-node2.etherhost.org:22002");
const CONTRACT_ADDRESS = "0xA4fafbE0ea4823e262b4916EF93CC5A6306A5DBc"

const ACCOUNT_ADDRESS = '0x7CbEb723CA0788af6549110fb2a9816ED0BAa1a6';
const PRIVATE_KEY = '0xab09158d9a817633c28c74b6e6c1bf34c26ffadc1a961870beaeef38b0753495';



var fs = require("fs");
var CONTRACT_STR = fs.readFileSync('food3.abi', 'utf-8');
var CONTRACT_ABI = JSON.parse(CONTRACT_STR)

quorumjs.extend(web3);


const contract = new web3.eth.Contract(CONTRACT_ABI, CONTRACT_ADDRESS)


//contract.getPastEvents("FoodItem",
//	{
//		filter: { logno: '674' },
//		//filter : { logIndex: 1 },
//		fromBlock: 0,
//		//toBlock: 173096
//	}
//).then(events => console.log(events))

logno = parseInt(process.argv[2])
url = process.argv[3] 
filehash = process.argv[4]

var encoded_data = contract.methods.FoodLogImage(logno, url, filehash).encodeABI()

const accountNonce = '0x' + (web3.eth.getTransactionCount(ACCOUNT_ADDRESS) + 1).toString(16)
//解決error: nouce too low
var tx = {
    nouce: accountNonce,
    from: ACCOUNT_ADDRESS,
    to: CONTRACT_ADDRESS,
    gas: 238960,//隨便設定的，只要大於下限即可
    data: encoded_data,
}

web3.eth.accounts.signTransaction(tx, PRIVATE_KEY)
.then(signed => {
    web3.eth.sendSignedTransaction(signed.rawTransaction)
    .on('receipt', console.log)
    .catch((err) => console.error(err));
    })
.catch((err) => console.error(err));


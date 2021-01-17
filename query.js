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

Event = process.argv[2]
lognum = process.argv[3]
from = parseInt(process.argv[4])
to = parseInt(process.argv[5])

if (to > 0){
	contract.getPastEvents(Event,
		{
			filter: { logno: lognum },
			//filter : { logIndex: 1 },
			fromBlock: from,
			toBlock: to
		}
	).then(events => console.log(events))
}
else{
	contract.getPastEvents(Event,
		{
			filter: { logno: lognum },
			//filter : { logIndex: 1 },
			fromBlock: from,
		}
	).then(events => console.log(events))
	
}

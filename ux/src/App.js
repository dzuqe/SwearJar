import './App.css';
import * as Web3 from 'web3';
import * as Contract from 'web3-eth-contract';
import 'axios';
import {useState, useEffect} from 'react';

const web3 = new Web3("http://localhost:8545");
Contract.setProvider("http://localhost:8545");
console.log(web3);

const jar_abi=[{"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"address","name":"token","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"get","outputs":[{"components":[{"internalType":"string","name":"word","type":"string"},{"internalType":"uint256","name":"count","type":"uint256"},{"internalType":"uint256","name":"spent","type":"uint256"}],"internalType":"struct SwearJar.Swear[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"word","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"swear","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"swears","outputs":[{"internalType":"string","name":"word","type":"string"},{"internalType":"uint256","name":"count","type":"uint256"},{"internalType":"uint256","name":"spent","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address payable","name":"to","type":"address"}],"name":"trashDay","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"trashcan","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address payable","name":"swearer","type":"address"},{"internalType":"string","name":"word","type":"string"}],"name":"withdraw","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}];
const jar_address="0xf6f9c82e3c86a058e549a4c135df196011ce74cf";

const token_abi = [{"inputs":[{"internalType":"uint256","name":"initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]

const token_address = '0xf34e9bd70c9686c3023e25b23e5a9ea49f1f4b02';

function connectContract(jar_abi, jar_address, token_abi, token_address) {
    var jar_contract = new Contract(jar_abi, jar_address);
    var token_contract = new Contract(token_abi, token_address);
    return [jar_contract, token_contract];
}

const JAR_CONTRACT = 0
const TOKEN_CONTRACT = 1

var contracts = connectContract(jar_abi, jar_address, token_abi, token_address);

async function getSwearWords(contracts) {
    var result = await contracts[JAR_CONTRACT]
        .methods
        .get()
        .call({"from": "0x3e3ef0a4A1CEA03B2FF7Fb784971e5299a474fe0"})
    var results = [];
    for (var i = 0; i < result.length; i++) {
        var item = {
            "name": result[i][0],
            "count": result[i][1],
            "amount": result[i][2]/1e18,
        }
        results.push(item);
    }
    console.log(results);
    return results;
}

async function swear(contracts) {
    var result = await contracts[JAR_CONTRACT]
        .methods
        .swear("horseshit", web3.toWei(1, 'ether'))
        .transact({"from": "0x3e3ef0a4A1CEA03B2FF7Fb784971e5299a474fe0"})

}

function SwearWord(props) {
    return (
        <div className="swear-word">
            <p>{ props.word.name } : {props.word.count} : {props.word.amount} $SCARG</p>
        </div>
    );
}

function SwearWords(props) {
    return (
        <div className="swear-words">
            <p>Name : Count : Amount</p>
            {props.words.map((word) => <SwearWord word={word} />)}
        </div>
    );
}

function App() {
  const [words, setWords] = useState([]);

  return (
    <div className="App App-header">
      <div className="body">
        <p>
          <SwearWords words={words} />
          <button onClick={async () => {
              var data = await getSwearWords(contracts);
              setWords(data);
           }}>
            See your words
          </button>

          <form onClick={() => console.log("Swear")} className="swear-box">
              <input type="text" placeholder="swear word" />
              <input type="number" placeholder="amount" />
              <input type="submit" value="swear" />
          </form>


        </p>
      </div>
    </div>
  );
}

export default App;

# nft_merkle_airdrop

通过 Merkle proof 方式空投 NFT token


# address

rinkeby: 

- Annual
  -  AnnualNFT deployed at: 0xd4F972ACd0a7c105133B12eF114fD9237e66c6cE
  -  MerkleDrop deployed at: 0xCDc90b7520a9CA83F5889471998cA2Df30b1b11f

- Bug Hunter
  - BugHunterNFT deployed at: 0x39FEdaC5c03588Ef344ccb0e812C0b6271C954d9
  - MerkleDrop deployed at: 0x2Da8Ae80bDe0c63B7A6dACE1c4bfC76Db91F01d2

- Share
  - ShareNFT deployed at: 0x1B197F746043Fbd1b9FcE2bcEb8d6Fc1e2da9641
  - MerkleDrop deployed at: 0x9f6cE3817508E7275f93f8047C9b8555e243EF55

kovan：

- AnnualNFT deployed at: 0x4c5F9E586eD26044e9700b4B33c32939a8b7Fc5a
- MerkleDrop deployed at: 0x283Fa5502037720Fe97af6C1c964df0a05eAFc5A

# run server

server服务帮助前端生成空投地址的Merkle proof

```
python ./merkle_drop/server.py

* Serving Flask app "Merkle Airdrop Backend Server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

# 获取merkle proof

在airdrop.csv中的地址

# annaul
```
curl http://0.0.0.0:5000/merkle_proof/annual/0x83Da47Ed23F68042646A20fC844358d892FA2976

{"address":"0x83Da47Ed23F68042646A20fC844358d892FA2976","proof":["0x0762657ac9a2382ba6606e97d2d4d0d6afe0c861653f4e20dd5a0d3dfdc79d4b","0x92eea7c4429f2450ee65bb20fb6c72438efe5292e0168f61b60a8e2e0ada9d37","0x77b448f6981c9dcd0ca20c6afc93c110090ef43f2b87558bdff76cef328d5e37","0xafba83455e14402d3599e939af71aa5e7caca8fa6ac2ba7cf358f2aafa396e79"],"tokenURI":"QmXRVfBz9Zdv2h11RBgLPV6ia5Pz6QTdrPFMHsfo4bF5YM"}
```

# bug_hunter
```
curl http://0.0.0.0:5000/merkle_proof/bug_hunter/0x83Da47Ed23F68042646A20fC844358d892FA2976

{"address":"0x83Da47Ed23F68042646A20fC844358d892FA2976","proof":["0x0762657ac9a2382ba6606e97d2d4d0d6afe0c861653f4e20dd5a0d3dfdc79d4b","0x92eea7c4429f2450ee65bb20fb6c72438efe5292e0168f61b60a8e2e0ada9d37","0x77b448f6981c9dcd0ca20c6afc93c110090ef43f2b87558bdff76cef328d5e37","0xafba83455e14402d3599e939af71aa5e7caca8fa6ac2ba7cf358f2aafa396e79"],"tokenURI":"QmXRVfBz9Zdv2h11RBgLPV6ia5Pz6QTdrPFMHsfo4bF5YM"}
```

# share
```
curl http://0.0.0.0:5000/merkle_proof/share/0x83Da47Ed23F68042646A20fC844358d892FA2976

{"address":"0x83Da47Ed23F68042646A20fC844358d892FA2976","proof":["0x0762657ac9a2382ba6606e97d2d4d0d6afe0c861653f4e20dd5a0d3dfdc79d4b","0x92eea7c4429f2450ee65bb20fb6c72438efe5292e0168f61b60a8e2e0ada9d37","0x77b448f6981c9dcd0ca20c6afc93c110090ef43f2b87558bdff76cef328d5e37","0xafba83455e14402d3599e939af71aa5e7caca8fa6ac2ba7cf358f2aafa396e79"],"tokenURI":"QmXRVfBz9Zdv2h11RBgLPV6ia5Pz6QTdrPFMHsfo4bF5YM"}
```

不在airdrop.csv中的地址
```
curl http://0.0.0.0:5000/merkle_proof/share/0x4c5F9E586eD26044e9700b4B33c32939a8b7Fc5a

{"address":"0x4c5F9E586eD26044e9700b4B33c32939a8b7Fc5a","proof":[],"tokenURI":"0x0"}
```

# 领取 NFT 例子

参考 ./merkle_drop/withdraw.py 例子

# docker 

build

```
docker build -t me .
```

run 

```
docker run -p 5000:5000 me
```
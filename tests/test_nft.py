#!/usr/bin/python3
import brownie


def test_mint(nft, accounts):
    nft.mint("aa", {'from': accounts[0]})


def test_balance(nft, accounts, chain, web3):

    b = web3.eth.blockNumber
    chain.mine(50)
    b1 = web3.eth.blockNumber

    print(nft.balanceOf(accounts[0]))
    assert nft.balanceOf(accounts[0]) == 0
    assert b1-b == 50

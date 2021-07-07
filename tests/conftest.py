#!/usr/bin/python3

import pytest
from merkle_drop.load_csv import load_airdrop_file
from merkle_drop.merkle_tree import build_tree, compute_merkle_root, create_proof
from merkle_drop.airdrop import get_tokenURI, get_item, to_items


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def nft(AnnualNFT, accounts):
    return AnnualNFT.deploy("ME Annual NFT", "ME", "https://gateway.pinata.cloud/ipfs/", {'from': accounts[0]})


@pytest.fixture(scope="module")
def merkleRoot(web3):
    airdrop_data = load_airdrop_file(
        "/Users/shouhewu/devWorkspace/defiWorkspace/nft_merkle_aidrdrop/data/airdrop.csv")
    merkle_root = compute_merkle_root(to_items(airdrop_data))
    return web3.toHex(merkle_root)


@pytest.fixture(scope="module")
def merkleDrop(MerkleDrop, accounts, nft, merkleRoot):
    merkle = MerkleDrop.deploy(nft, merkleRoot, {'from': accounts[0]})
    nft.setMerkleDrop(merkle.address, {'from': accounts[0]})
    return merkle

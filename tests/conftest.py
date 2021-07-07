#!/usr/bin/python3

import pytest
from merkle_drop.load_csv import load_airdrop_file
from merkle_drop.merkle_tree import build_tree, compute_merkle_root, create_proof
from merkle_drop.airdrop import get_tokenURI, get_item, to_items
from merkle_drop.merkle_tree import Item, build_tree, create_proof, validate_proof


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


@pytest.fixture(scope="session")
def tree_data():
    # Ignore the first address, since it is used for the premint_token_owner
    airdrop_data = load_airdrop_file(
        "/Users/shouhewu/devWorkspace/defiWorkspace/nft_merkle_aidrdrop/data/airdrop.csv")
    return to_items(airdrop_data)

@pytest.fixture(scope="session")
def proofs_for_tree_data(tree_data):
    tree = build_tree(tree_data)
    proofs = [create_proof(item, tree) for item in tree_data]

    assert all(
        validate_proof(item, proof, tree.root.hash)
        for item, proof in zip(tree_data, proofs)
    )

    return proofs


@pytest.fixture(scope="session")
def eligible_address_0(tree_data):
    return tree_data[0].address


@pytest.fixture(scope="session")
def eligible_value_0(tree_data):
    return tree_data[0].value


@pytest.fixture(scope="session")
def proof_0(proofs_for_tree_data):
    return proofs_for_tree_data[0]

@pytest.fixture(scope="session")
def root_hash_for_tree_data(tree_data):
    tree = build_tree(tree_data)
    return tree.root.hash

@pytest.fixture(scope="module")
def merkleDrop(MerkleDrop, accounts, nft, merkleRoot):
    merkle = MerkleDrop.deploy(nft, merkleRoot, {'from': accounts[0]})
    nft.setMerkleDrop(merkle.address, {'from': accounts[0]})
    return merkle

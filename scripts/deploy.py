
from brownie import MerkleDrop, AnnualNFT, accounts, network, web3, config

from eth_utils import address, encode_hex, is_checksum_address, to_canonical_address
from merkle_drop.airdrop import get_tokenURI, get_item, to_items
from merkle_drop.load_csv import load_airdrop_file
from merkle_drop.merkle_tree import build_tree, compute_merkle_root, create_proof


def main():
    acct = accounts.add(
        config["wallets"]["from_key"]
    )

    nft = AnnualNFT.deploy(
        "ME Annual NFT", "ME", "https://gateway.pinata.cloud/ipfs/", {'from': acct})

    airdrop_data = load_airdrop_file(
        "/Users/shouhewu/devWorkspace/defiWorkspace/nft_merkle_aidrdrop/data/airdrop.csv")
    merkle_root = compute_merkle_root(to_items(airdrop_data))

    merkle_drop = MerkleDrop.deploy(
        nft.address, web3.toHex(merkle_root), {'from': acct})

    nft.setMerkleDrop(merkle_drop.address, {'from': acct})

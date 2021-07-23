import math

import eth_tester.exceptions
import pytest
from eth_utils import to_checksum_address, to_canonical_address
from web3.exceptions import BadFunctionCallOutput
from merkle_drop.merkle_tree import Item, build_tree, create_proof, validate_proof


@pytest.fixture
def other_data():
    return [Item(b"\xff" * 20, "QmXRVfBz9Zdv2h11RBgLPV6ia5Pz6QTdrPFMHsfo4bF5YM"), Item(b"\x00" * 20, "QmXRVfBz9Zdv2h11RBgLPV6ia5Pz6QTdrPFMHsfo4bF5YM")]


def test_proof_entitlement(merkleDrop, tree_data, proofs_for_tree_data):

    for i in range(len(proofs_for_tree_data)):
        canonical_addr = to_canonical_address(tree_data[i].address[:20])
        address = to_checksum_address(canonical_addr)
        value = tree_data[i].value
        proof = proofs_for_tree_data[i]
        assert merkleDrop.verifyEntitled(
            address, value, proof
        )


def test_incorrect_value_entitlement(
    merkleDrop, tree_data, proofs_for_tree_data
):
    canonical_addr = to_canonical_address(tree_data[0].address[:20])
    address = to_checksum_address(canonical_addr)
    incorrect_value = tree_data[0].value + "1234"
    proof = proofs_for_tree_data[0]

    assert (
        merkleDrop.verifyEntitled(
            address, incorrect_value, proof
        )
        is False
    )


def test_incorrect_proof_entitlement(
    merkleDrop, other_data, proofs_for_tree_data
):
    address = other_data[0].address
    value = other_data[0].value
    incorrect_proof = proofs_for_tree_data[0]

    assert (
        merkleDrop.verifyEntitled(
            address, value, incorrect_proof
        )
        is False
    )


def test_claim(
    merkleDrop, tree_data, proofs_for_tree_data
):
    for i in range(len(proofs_for_tree_data)):
        canonical_addr = to_canonical_address(tree_data[i].address[:20])
        address = to_checksum_address(canonical_addr)
        value = tree_data[i].value
        proof = proofs_for_tree_data[i]
        merkleDrop.claim(value, proof, {'from': address})


import pytest
from eth_utils import keccak

from merkle_drop.merkle_tree import (
    Item,
    build_tree,
    compute_leaf_hash,
    compute_merkle_root,
    compute_parent_hash,
    create_proof,
    in_tree,
    validate_proof,
)


@pytest.fixture
def tree_data():
    return [
        Item(b"\xaa" * 20, "QmXRVfBz9Zdv2h11RBgLPV6ia5Pz6QTdrPFMHsfo4bF5YM"),
        Item(b"\xbb" * 20, "QmXRVfBz9Zdv2h11RBgLPV6ia5Pz6QTdrPFMHsfo4bF5YM"),
        Item(b"\xcc" * 20, "QmXRVfBz9Zdv2h11RBgLPV6ia5Pz6QTdrPFMHsfo4bF5YM"),
        Item(b"\xdd" * 20, "QmXRVfBz9Zdv2h11RBgLPV6ia5Pz6QTdrPFMHsfo4bF5YM"),
        Item(b"\xee" * 20, "QmXRVfBz9Zdv2h11RBgLPV6ia5Pz6QTdrPFMHsfo4bF5YM"),
    ]


@pytest.fixture
def other_data():
    return [Item(b"\xff" * 20, "QmXRVfBz9Zdv2h11RBgLPV6ia5Pz6QTdrPFMHsfo4bF5YM"), Item(b"\x00" * 20, "QmXRVfBz9Zdv2h11RBgLPV6ia5Pz6QTdrPFMHsfo4bF5YM")]


def test_in_tree(tree_data):
    tree = build_tree(tree_data)

    assert all(in_tree(item, tree.root) for item in tree_data)


def test_not_in_tree(tree_data, other_data):
    tree = build_tree(tree_data)

    assert not any(in_tree(item, tree.root) for item in other_data)


def test_valid_proof(tree_data):
    tree = build_tree(tree_data)
    proofs = [create_proof(item, tree) for item in tree_data]

    assert all(
        validate_proof(item, proof, tree.root.hash)
        for item, proof in zip(tree_data, proofs)
    )


def test_invalid_proof(tree_data):
    tree = build_tree(tree_data)

    item = next(iter(tree_data))
    assert not validate_proof(item, [], tree.root.hash)


def test_wrong_proof(tree_data):
    tree = build_tree(tree_data)
    proofs = [create_proof(item, tree) for item in tree_data]

    item = next(iter(tree_data))
    assert not validate_proof(item, proofs[4], tree.root.hash)


def test_wrong_value(tree_data, other_data):
    tree = build_tree(tree_data)
    proofs = [create_proof(item, tree) for item in tree_data]

    item = next(iter(other_data))
    assert not validate_proof(item, proofs[0], tree.root.hash)


def test_can_not_create_proof_for_missing_item(tree_data, other_data):
    tree = build_tree(tree_data)
    with pytest.raises(ValueError):
        create_proof(other_data[0], tree)


def test_tree_is_sorted(tree_data):
    root = compute_merkle_root(tree_data)

    reversed_tree_data = list(reversed(tree_data))
    assert reversed_tree_data != tree_data
    reversed_root = compute_merkle_root(reversed_tree_data)

    assert reversed_root == root

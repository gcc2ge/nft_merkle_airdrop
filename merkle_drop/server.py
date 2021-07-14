import logging

from eth_utils import encode_hex, is_address, to_canonical_address, to_checksum_address
from flask import Flask, abort, jsonify
from flask_cors import CORS

from merkle_drop.airdrop import get_tokenURI, get_item, to_items
from merkle_drop.load_csv import load_airdrop_file
from merkle_drop.merkle_tree import build_tree, create_proof

app = Flask("Merkle Airdrop Backend Server")


airdrop_dict_name = {}
airdrop_tree_name = {}


def init_gunicorn_logging():
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def init_cors(**kwargs):
    CORS(app=app, **kwargs)


def init(
    file_dict
):
    global airdrop_dict_name
    global airdrop_tree_name

    for (k, v) in file_dict.items():
        app.logger.info(
            f"Initializing merkle tree from file {v}")
        airdrop_dict = load_airdrop_file(v)
        app.logger.info(
            f"Building merkle tree from {len(airdrop_dict)} entries")
        airdrop_tree = build_tree(to_items(airdrop_dict))
        airdrop_dict_name[k] = airdrop_dict
        airdrop_tree_name[k] = airdrop_tree


@app.errorhandler(404)
def not_found(e):
    return jsonify(error=404, message="Not found"), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=400, message=e.description), 400


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=500, message="There was an internal server error"), 500


@app.route("/merkle_proof/<string:nft_name>/<string:address>", methods=["GET"])
def get_proof_for(nft_name, address):
    if not is_address(address):
        abort(400, "The address is not in checksum-case or invalid")
    canonical_address = to_canonical_address(address)

    airdrop_dict = airdrop_dict_name[nft_name]
    airdrop_tree = airdrop_tree_name[nft_name]

    eligible_tokens = get_tokenURI(canonical_address, airdrop_dict)
    if eligible_tokens == "0x0":
        proof = []
    else:
        proof = create_proof(
            get_item(canonical_address, airdrop_dict), airdrop_tree)
    return jsonify(
        {
            "address": to_checksum_address(address),
            "tokenURI": eligible_tokens,
            "proof": [encode_hex(hash_) for hash_ in proof],
        }
    )


# Only for testing
if __name__ == "__main__":
    init_cors(origins="*")
    init({"annual": "../data/airdrop_annual.csv",
          "bug_hunter": "../data/airdrop_bug_hunter.csv", "share": "../data/airdrop_share.csv"})
    app.run(host="0.0.0.0", port=5000)

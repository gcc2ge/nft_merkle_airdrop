import logging
import math
import time

import pendulum
from eth_utils import encode_hex, is_address, to_canonical_address, to_checksum_address
from flask import Flask, abort, jsonify
from flask_cors import CORS

from merkle_drop.airdrop import get_tokenURI, get_item, to_items
from merkle_drop.load_csv import load_airdrop_file
from merkle_drop.merkle_tree import build_tree, create_proof

app = Flask("Merkle Airdrop Backend Server")

airdrop_dict = None
airdrop_tree = None


def init_gunicorn_logging():
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def init_cors(**kwargs):
    CORS(app=app, **kwargs)


def init(
    airdrop_filename: str,
):
    global airdrop_dict
    global airdrop_tree

    app.logger.info(f"Initializing merkle tree from file {airdrop_filename}")
    airdrop_dict = load_airdrop_file(airdrop_filename)
    app.logger.info(f"Building merkle tree from {len(airdrop_dict)} entries")
    airdrop_tree = build_tree(to_items(airdrop_dict))


@app.errorhandler(404)
def not_found(e):
    return jsonify(error=404, message="Not found"), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=400, message=e.description), 400


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=500, message="There was an internal server error"), 500


@app.route("/merkle_proof/<string:address>", methods=["GET"])
def get_proof_for(address):
    if not is_address(address):
        abort(400, "The address is not in checksum-case or invalid")
    canonical_address = to_canonical_address(address)

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
    init("../data/airdrop.csv")
    app.run()

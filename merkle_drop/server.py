import logging
import os

from eth_utils import encode_hex, is_address, to_canonical_address, to_checksum_address, to_bytes
from flask import Flask, abort, jsonify
from flask_cors import CORS

from merkle_drop.airdrop import get_tokenURI, get_item, to_items
from merkle_drop.load_csv import load_airdrop_file
from merkle_drop.merkle_tree import build_tree, create_proof
import yaml

app = Flask("Merkle Airdrop Backend Server")


airdrop_dict = None
airdrop_tree = None
config_dict = {}


def init_gunicorn_logging():
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def init_cors(**kwargs):
    CORS(app=app, **kwargs)


def init(
    airdrop_filename: str,
    config_filename: str,
):
    global airdrop_dict
    global airdrop_tree
    global config_dict

    app.logger.info(f"Initializing merkle tree from file {airdrop_filename}")
    airdrop_dict = load_airdrop_file(airdrop_filename)
    app.logger.info(f"Building merkle tree from {len(airdrop_dict)} entries")
    airdrop_tree = build_tree(to_items(airdrop_dict))

    with open(config_filename, "r") as stream:
        config_dict = yaml.safe_load(stream)


@app.errorhandler(404)
def not_found(e):
    return jsonify(error=404, message="Not found"), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=400, message=e.description), 400


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=500, message="There was an internal server error"), 500


@app.route("/merkle_proof/nft_type/<string:nft_name>", methods=["GET"])
def get_nft_type(nft_name):
    return config_dict[nft_name]


@app.route("/merkle_proof/<string:nft_name>/<string:address>", methods=["GET"])
def get_proof_for(nft_name, address):
    if not is_address(address):
        abort(400, "The address is not in checksum-case or invalid")
    canonical_address = to_canonical_address(address)

    tokenURI = config_dict[nft_name]
    eligible_tokens = get_tokenURI(
        canonical_address+to_bytes(text=tokenURI), airdrop_dict)
    if eligible_tokens == "0x0":
        proof = []
    else:
        proof = create_proof(
            get_item(canonical_address+to_bytes(text=tokenURI), airdrop_dict), airdrop_tree)
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
    THIS_DIR = os.path.abspath(os.path.dirname(__file__))
    airdrop_path = os.path.join(THIS_DIR, '../' 'data/airdrop.csv')
    token_type_path = os.path.join(THIS_DIR, '../' 'data/token_type.yaml')
    init(airdrop_path, token_type_path)
    app.run(host="0.0.0.0", port=5000)

/* Please read and review the Terms and Conditions governing this
   Merkle Drop by visiting the Trustlines Foundation homepage. Any
   interaction with this smart contract, including but not limited to
   claiming Trustlines Network Tokens, is subject to these Terms and
   Conditions.
 */

pragma solidity ^0.8.4;

import "./NFT.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "./IMerkleDistributor.sol";

contract MerkleDrop is IMerkleDistributor {
    address public immutable override token;
    bytes32 public immutable override merkleRoot;

    mapping(address => bool) public withdrawn;

    constructor(address token_, bytes32 merkleRoot_) public {
        token = token_;
        merkleRoot = merkleRoot_;
    }

    function isClaimed(address recipient) public view override returns (bool) {
        return withdrawn[recipient];
    }

    function claim(string calldata tokenURI, bytes32[] calldata proof)
        external
        override
    {
        require(
            !withdrawn[msg.sender],
            "You have already withdrawn your entitled token."
        );
        require(
            verifyEntitled(msg.sender, tokenURI, proof),
            "The proof could not be verified."
        );

        uint256 tokenId = AnnualNFT(token).mint(msg.sender, tokenURI);
        withdrawn[msg.sender] = true;
        emit Claimed(msg.sender, tokenId, tokenURI);
    }

    function verifyEntitled(
        address recipient,
        string memory tokenURI,
        bytes32[] memory proof
    ) public view returns (bool) {
        // We need to pack the 20 bytes address to the 32 bytes value
        // to match with the proof made with the python merkle-drop package
        bytes32 leaf = keccak256(abi.encodePacked(recipient, tokenURI));
        return verifyProof(leaf, proof);
    }

    function verifyProof(bytes32 leaf, bytes32[] memory proof)
        internal
        view
        returns (bool)
    {
        bytes32 currentHash = leaf;

        for (uint256 i = 0; i < proof.length; i += 1) {
            currentHash = parentHash(currentHash, proof[i]);
        }

        return currentHash == merkleRoot;
    }

    function parentHash(bytes32 a, bytes32 b) internal pure returns (bytes32) {
        if (a < b) {
            return keccak256(abi.encode(a, b));
        } else {
            return keccak256(abi.encode(b, a));
        }
    }
}

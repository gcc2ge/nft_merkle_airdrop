// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.3;

// Allows anyone to claim a token if they exist in a merkle root.
interface IMerkleDistributor {
    // Returns the address of the token distributed by this contract.
    function token() external view returns (address);

    // Returns the merkle root of the merkle tree containing account balances available to claim.
    function merkleRoot() external view returns (bytes32);

    // Returns true if the index has been marked claimed.
    function isClaimed(address recipient,string memory tokenURI) external view returns (bool);

    // Claim the given amount of the token to the given address. Reverts if the inputs are invalid.
    function claim(string calldata tokenURI, bytes32[] calldata merkleProof) external;

    // This event is triggered whenever a call to #claim succeeds.
    event Claimed(address account, uint256 tokenId, string tokenURI);
}

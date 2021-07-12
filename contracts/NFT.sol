pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MENFT is ERC721URIStorage,Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    string private _baseTokenURI;

    address private _merkle_drop_addr;

    constructor(
        string memory name,
        string memory symbol,
        string memory baseTokenURI
    ) public ERC721(name, symbol) {
        _baseTokenURI = baseTokenURI;
    }

    function setMerkleDrop(address merkle_drop_addr) external onlyOwner {
        _merkle_drop_addr = merkle_drop_addr;
    }

    modifier onlyMerkleDrop {
        require(msg.sender == _merkle_drop_addr);
        _;
    }

    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }

    function mint(address to, string memory tokenURI)
        external
        onlyMerkleDrop
        returns (uint256)
    {
        _tokenIds.increment();
        uint256 newItemId = _tokenIds.current();
        _mint(to, newItemId);
        _setTokenURI(newItemId, tokenURI);

        return newItemId;
    }
}

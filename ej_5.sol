// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Votacion {
    // Mapping que almacena los votos para cada dirección
    mapping(address => uint) public votos;

    // Función para emitir un voto
    function votar(address candidato) external {
        // Incrementa el contador de votos para el candidato en 1
        votos[candidato] += 1;
    }
}

# Cryptography algorithms

This repository was created as part of a university class project focusing on cryptography. 
It provides a comprehensive Python implementation of classic cryptographic systems, stream encryption algorithms, and the Merkle-Hellman Knapsack cryptosystem.

## Structure

The repository structure is as follows:

1. **lab1**
    - **_Caesar cipher_**: Contains the implementation of the Caesar cipher algorithm.
    - **_Vigenère cipher_**: Contains the implementation of the Vigenère cipher algorithm.
    - **Scytale cipher**: Contains the implementation of the Scytale cipher algorithm.
    - **_Railfence cipher_**: Contains the implementation of the Railfence cipher algorithm.
    - **_Console Menu_**: Provides a console-based menu for easy access to each implemented cipher.
2. **lab2**
   
    Lab 2 introduces a **_generic byte-sequence ciphering/deciphering stream cipher_** that accommodates various key generation algorithms.
    It implements the **_Solitaire algorithm_** and another pseudorandom sequence generator, **_Blum-Blum-Shub_**. 
    It also includes a client class that allows two client processes to communicate securely over a network using the stream encryptor.
    It requires a configuration.txt file specifying the desired algorithm - "solitaire" or other - and a key for it.

3. **lab3**
    
    Lab 3 focuses on implementing a secure communication system in Python based on the **_Merkle-Hellman Knapsack cryptosystem_** and the **_Solitaire algorithm_**.
    The system consists of two main entities:
    - **KeyServer**:
    Located at a publicly known address (localhost and a specified port), the KeyServer listens for client requests and responds accordingly. This communication is not 
    Clients can interact with the KeyServer in one of two ways:
      - Requesting their Knapsack public key by sending a client identifier (client_id).
      - Registering with the server by sending their ID and public key. If a client is already registered, its public key will be updated upon a new registration request.
        
    - **Clients**:
    At least two different Clients communicate with each other through the KeyServer. The communication process consists of two main steps:

      - Key exchange: Clients request each other's public keys from the KeyServer based on their client_id. They then agree on a shared key using the Merkle-Hellman Knapsack cryptosystem.
      - Encrypted communication: Using the shared key established in the previous step, clients communicate bidirectionally using the Solitaire symmetric cryptosystem.

    *Notes*:
      - Communication between clients and the KeyServer is not encrypted (KeyServer only acts as a publicly available "phone book" and only provides public keys).
      - The communication between clients is not through the KeyServer, but directly between each other ("peer-to-peer"). The port number of the other client is passed as an argument after the client's own port number.
      - In a setup where two clients are communicating with each other, a total of 3 different keys are used in the system: one is the public Knapsack key of client1 (for client2 -> client1 communication), the second is the public Knapsack key of client2 (for client1 -> client2 communication), and the third is the Solitaire symmetric system key.
      The first two keys are used by the clients for key exchange (they are requested from the KeyServer), the third one is agreed upon by the clients.



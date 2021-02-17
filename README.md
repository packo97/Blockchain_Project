# Blockchain_Project

## Theory
The below paragraphs expose all theoretical concepts in which our blockchain system is based.

### Assumptions
Our blockchain system is created with **didactic** purpose, and to simplify all things we
must have **strong assumptions**:

* Blockchain miners **MUST BE FULLY CONNECTED**. It is important because the spreading of transactions received
between miners and block mining notifications must be shared by all miners in **real time**.
This real time works well because the consensus protocol **Proof Of Lottery** is very fast.
The protocol Proof Of Lottery is not resource consuming because our project must be eco-friendly
and the mining doesn't brings any interest to miner that do it.
Mining game in our case is only useful to carry on blockchain.

* Another important assumption is **Tri da chiazza protocol**. This assumption is not a strong assumption,
but the system is designed to have **AT LEAST** three peers.
This protocol take the name from a simple italian dialect word.
When in typical calabresian town the people see three friends in group,
they often call it "i tri da chiazza".
This cominication protocol a part every joke is very simple and useful for a didactic purpose.
To avoid problem with p2p, such as nat, firewalls hole punching, and a lot of stuff...
We make a simple choice/requirement.
  * Every organization that want to use our blockchain **MUST HAVE** at least 3 hosts with static ip.
This 3 hosts are the main reference for all peers. This 3 hosts must be the main miners.
  * The infrustructure is easy scalable, but it must guarantee this 3 hosts.
  * This main 3 hosts are the reference for client and for miner

* As shown above, another important implicit assumption is thath **THIS BLOCKCHAIN DOESN'T USE A REAL P2P PROTOCOL**.
In fact this blockchain **IS DECENTRALIZED** very well, but it has not a real P2P. It doesn't use GOSSIP or other protocols.
As we say, it is based on the "friendship" by miners.
This aspect is not bad because we must consider that this blockchain has a didactic purpose and every organizzation
can have a blockchain in which can handle votes of events.
This blockchain is not designed to be a voting system of "american election", but it is more useful
as a voting system for "the new topic of a company".

* Every miner has it's own **LEDGER DATABASE**. This ledger database is a sqlite3 db (in the code you can see **ledger1.db**, ...).
It contains transactions and blocks.

**NOTE**: For more info, if you don't like python, docker and other nerdy stuffs, you can see the presentation (our "white paper").
It is the file **Whitepaper.pdf**


## Practice
The below paragraphs expose all practical concepts useful for running blockchain.
We can use 2 simple modalities, with **docker** and with **python and virtual environments**.
The first solution can be used in "production" and the second in "development".

### Run project

#### Run blockchain

##### Virtualenv and python
1. virtualenv -p /usr/bin/python-version ./blockchain/env **WE Suggest python 3.8**
2. source ./blockchain/env/bin/activate
3. pip install --upgrade pip **ONLY if you have a version of pip NOT greater than 9.0.1**
4. pip install -r ./blockchain/requirements.txt
5. You can run with 2 roles:

RUN AS CLIENT:
 * python ./blockchain/main.py client_conficuration_file.json {event} {vote}

RUN AS MINER:
  * python ./blockchain/main.py miner_conficuration_file.json

**NOTE**: you must set properly configuration in **config.json** before run

##### Docker
###### Single app - PURE DOCKER
**NOTE:** You can use pure docker, but in this project the "standard" is docker-compose.
But here you can find instruction to run single with docker.

You can build a custom network of miner instead of using docker links
* docker network create --driver=bridge --subnet={IP}/{MASK} blockchain-network

1. docker build ./blockchain/ -t blockchain-app:0.1
2. You can run with 2 roles:

RUN AS CLIENT:
 * docker run -it --name client --link miner_instance_name:client blockchain-app:0.1 python main.py client_conficuration_file.json {event} {vote}

RUN AS MINER:
  * docker run -it -p MINER_PORT:MINER_PORT --name miner_instance_name blockchain-app:0.1 python main.py miner_conficuration_file.json
    
###### Single app - DOCKER-COMPOSE
**NOTE**: You can customize our docker compose and adapt it to your needs. 
We have already done a docker compose with a basic configuration, and with running docker-compose instructions below
you can run a test environment

RUN ALL MINERS AND A SIMPLE CLIENT
* docker-compose up

RUN A SINGLE MINER
* docker-compose up miner1
* docker-compose up miner2
...

RUN A SINGLE BLOCKCHAIN VIEWER
* docker-compose up viewer1
* docker-compose up viewer2
...

RUN SIMPLE CLIENT
* docker-compose up client

**NOTE** Viewers and miners **MUST HAVE** a common value in test environment
because they must work on same ledger file!


### Generate genesis in ledger
Open your ledger db file with an editor and with following queries you can create the genesys blocks:

* INSERT INTO Block (hash, seed, miner_address, lottery_number, previous_hash, timestamp_block) 
VALUES ('656ffd143ab4f1d3074aa7db58feeb571a700824bd061f7f18d2b07b5be34f2c', 523139852477692024, 'rodolfo_pasquale', 4610, 'genesis', '01/01/0001,00:00:00')

* INSERT INTO "Transaction" (timestamp_transaction, event, vote, address, block_hash) 
VALUES ('01/01/0001,00:00:00', 'genesis_event', 42, 'rodolfo_pasquale', '656ffd143ab4f1d3074aa7db58feeb571a700824bd061f7f18d2b07b5be34f2c')


# WORK IN PROCESS

## Run frontend app

**NOTE:** The frontend is **WORK IN PROCESS**
1. docker build ./frontend -t blockchain_frontend:0.1
2. docker run -it -p 4200:4200 -v $(pwd)/frontend:/usr/src/frontend-app --name frontend blockchain_frontend:0.1
3. go to http://localhost:4200 and enjoy!

## Interaction with OTHER BLOCKCHAINS

**NOTE:** This functionality is **WORK IN PROCESS**.
We must add a field "extra" on our transaction and make the possibility to transaction with this "extra" field to have a different
validation.

Suppose that we want implement IOT. Iot must send in a transaction is content (for example *(WEIGHT;USER_ID)*) in extra field,
and as event and vote *(IOT_EVENT;0)*.

It apparently can go well, but it violate our first most important validation rule! (more votes for a singl event!)

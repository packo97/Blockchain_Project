# Blockchain_Project
## Brief info
We want to develop a voting system powered by blockchain.
In this voting system we will create:
* A from sctatch p2p infrastructure and blockchain write in pure python
* A comunication system relative to above point
* A frontend face with Angular

# Blockchain specification
## "Tri da chiazza" comunication protocol
This protocol take the name from a simple italian dialect word.
When in typical calabresian town the people see three friends in group,
they often call it "i tri da chiazza".

This cominication protocol part every joke is very simple and useful for a didactic purpose.
To avoid problem with p2p, such as nat, firewalls hole punching, and a lot of staff...
We make a simple choice/requirement.

* Every organization that want to use our blockchain **MUST HAVE** at least 3 hosts with static ip.
This 3 hosts are the main reference for all peers. This 3 hosts must be the main miners.
* The infrustructure is easy scalable, but it must guarantee this 3 hosts.


# Run projects (INDIVIDUALY for dev purposes)
## Run frontend
1. docker build ./frontend -t blockchain_frontend:0.1
2. docker run -it -p 4200:4200 -v $(pwd)/frontend:/usr/src/frontend-app --name frontend blockchain_frontend:0.1
3. go to http://localhost:4200 and enjoy!

### Run frontend **AFTER** installation
* docker start frontend --interactive

### Generate new angular component (USING DOCKER)
* docker exec -it frontend ng generate component component_name
**NOTE**: if you have Angular installed or you have VS Code tools for angular
you can make operations easier

### Install a dependencies for Angular
1. docker exec -it frontend npm install --save dependency_name
2. docker commit frontend blockchain_frontend:0.1 **IMPORTANT if you wan't rebuild image every time**


## Run blockchain
### Using virtualenv and python
1. virtualenv -p /usr/bin/python-version ./blockchain/env **WE Suggest python 3.8**
2. source ./blockchain/env/bin/activate
3. pip install --upgrade pip **ONLY if you have a version of pip NOT greater than 9.0.1**
4. pip install -r ./blockchain/requirements.txt
5. python ./blockchain/.. miner.py or client.py ...

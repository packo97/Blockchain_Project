# Blockchain_Project
## Brief info
We want to develop a voting system powered by blockchain.
In this voting system we will create:
* A from sctatch p2p infrastructure and blockchain write in pure python
* A comunication system relative to above point
* A frontend face with Angular

# Blockchain specification
## "Tri da chiazza" comunication protocol



# Run projects with docker (SINGLE CONTAINER)
## Run frontend
* docker build ./frontend -t blockchain_frontend:0.1
* docker run -it -p 4200:4200 -v $(pwd)/frontend:/usr/src/frontend-app --name frontend blockchain_frontend:0.1
* go to http://localhost:4200 and enjoy!

### Run frontend **AFTER** installation
* docker start frontend --interactive

### Generate new angular component (USING DOCKER)
* docker exec -it frontend ng generate component component_name
**NOTE**: if you have Angular installed or you have VS Code tools for angular
you can make operations easier

### Install a dependencies for Angular
* docker exec -it frontend npm install --save dependency_name
* docker commit frontend blockchain_frontend:0.1 **IMPORTANT if you wan't rebuild image every time**
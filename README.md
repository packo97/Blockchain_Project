# Blockchain_Project
We want to develop a voting system powered by blockchain 

# Run projects with docker separately
## Run frontend
* docker build ./frontend -t blockchain_frontend:0.1
* docker run -it -p 4200:4200 -v $(pwd)/frontend:/usr/src/frontend-app --name frontend blockchain_frontend:0.1
* go to http://localhost:4200 and enjoy!

### Run frontend **AFTER** installation
* docker start frontend --interactive

### Generate new angular component
* docker exec -it frontend ng generate component component_name

### Install a dependencies 
* docker exec -it frontend npm install --save dependency_name
* docker commit frontend blockchain_frontend:0.1 **IMPORTANT if you wan't rebuild image every time**

## Run backend
* docker build ./backend -t blockchain_backend:0.1
* docker run -it -p 3000:3000 -v $(pwd)/backend:/usr/src/backend-app --name backend blockchain_backend:0.1
* go to http://localhost:3000 and enjoy!

### Shell on backend
* docker exec -it backend bash

* **NOTE** to get container id use **docker ps -a**
# Blockchain_Project
We want to develop a voting system powered by blockchain 

# Run projects with docker separately
## Run frontend
* docker build ./frontend -t blockchain_frontend:0.1
* docker run -it -p 8080:8080 -v $(pwd)/frontend:/usr/src/frontend-app blockchain_frontend:0.1
* go to http://localhost:8080 and enjoy!

## Run backend
* docker build ./backend -t blockchain_backend:0.1
* docker run -it -p 3000:3000 -v $(pwd)/backend:/usr/src/backend-app blockchain_backend:0.1
* go to http://localhost:3000 and enjoy!

### Shell on backend
* docker exec -it (CONTAINER_ID) bash

* **NOTE** to get container id use **docker ps -a**
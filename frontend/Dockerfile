# Node js base image
FROM node:lts

# Create/change working directory in the container
WORKDIR /usr/src/frontend-app

# Copy package.json and install dependencies
COPY package*.json /usr/src/frontend-app/
RUN npm install

# Create two volumes (solve problem of node_modules directory)
VOLUME [ "/usr/src/frontend-app/node_modules", "/usr/src/frontend-app/" ]

# Expose port 4200
EXPOSE 4200

# Run server after image creation is done:
# DEVELOPMENT MODE
CMD [ "npm", "start" ]
# CMD [ "npm", "run", "build" ]

# Node js base image
FROM node:lts

# Create/change working directory in the container
WORKDIR /usr/src/backend-app

# Copy all files of the template
COPY . .

# Expose port 3000
EXPOSE 3000

# Symbol cli dependencies and typescript
RUN npm install --global symbol-cli \
    npm install --global typescript \
    sudo npm install --global ts-node


# Install express and nodemon (to don't execute run every time)
RUN npm install -g nodemon \
    npm install


# Run server after image creation is done:
# DEVELOPMENT MODE
CMD [ "npm", "run", "serve" ]
# CMD [ "npm", "run", "build" ]

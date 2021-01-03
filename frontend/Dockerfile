# Node js base image
FROM node:lts

# Create/change working directory in the container
WORKDIR /usr/src/frontend-app

# Copy all files of the template
COPY . .

# Expose port 8080
EXPOSE 8080

# Update vue cli and install theme
RUN npm i -g @vue/cli \
    npm install


# Run server after image creation is done:
# DEVELOPMENT MODE
CMD [ "npm", "run", "serve" ]
# CMD [ "npm", "run", "build" ]

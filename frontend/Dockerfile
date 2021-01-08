# Node js base image
FROM node:lts

# Create/change working directory in the container
WORKDIR /usr/src/frontend-app

# Copy all files of the template
COPY . .

# Expose port 4200
EXPOSE 4200

# Update vue cli and install theme
RUN npm install -g @angular/cli


# Run server after image creation is done:
# DEVELOPMENT MODE
CMD [ "npm", "start" ]
# CMD [ "npm", "run", "build" ]

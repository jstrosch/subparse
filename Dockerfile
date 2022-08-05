# Choose the Image which has Node installed already
FROM node:lts-alpine

# set working directory
WORKDIR /app

# install and cache app dependencies
COPY ./viewer/package.json .
COPY ./viewer .
RUN npm install

# start app
CMD ["npm", "run", "serve"]
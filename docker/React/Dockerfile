# pull the base image
FROM node:alpine AS builder

# set the working direction
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package*.json ./

RUN npm install

# add app
COPY . ./

RUN npm run build

# start app
#CMD ["npm", "start"]


FROM nginx:1.20

WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=builder /app/build .

ENTRYPOINT ["nginx", "-g", "daemon off;"]


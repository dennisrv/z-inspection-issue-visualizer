FROM node:16.4-alpine3.13

WORKDIR /app
COPY package*.json ./
RUN yarn install

COPY . .

CMD ["yarn", "serve"]
FROM node:16.4-alpine3.13

WORKDIR /app
COPY package*.json ./
ENV NODE_ENV dev
RUN yarn install

COPY . .

CMD ["yarn", "serve"]
FROM node:18.18-alpine3.17

WORKDIR /app/frontend/

COPY package*.json /app/frontend/

RUN npm install

COPY . /app/frontend/

CMD ["npm", "start"]
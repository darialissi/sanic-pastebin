FROM node:alpine

WORKDIR /app 

RUN npm install http-server 

COPY . .  

CMD ["npx", "http-server"]
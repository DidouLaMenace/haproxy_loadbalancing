FROM node:18

WORKDIR /app

COPY server1.js server2.js ./

CMD node server1.js & node server2.js && tail -f /dev/null

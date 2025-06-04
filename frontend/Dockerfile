FROM node:18-alpine
WORKDIR /app

COPY package*.json ./
RUN npm install --force

COPY . .

ARG VITE_API_URL=http://backend:8000
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

EXPOSE 4173
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "4173"]
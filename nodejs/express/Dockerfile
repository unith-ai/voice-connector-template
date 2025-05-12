FROM node:18-slim AS builder
RUN apt-get update && apt-get install -y curl nano
WORKDIR /connector

# Copy package.json and package-lock.json
COPY ./package.json ./package.json
COPY ./yarn.lock ./yarn.lock

# Install dependencies
RUN yarn install

# Copy the source code
COPY . .

# Expose the port
EXPOSE 8080

# Run the app
CMD ["node", "app.js"]

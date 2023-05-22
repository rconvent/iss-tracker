# Dockerfile for Nuxt.js app

# Use the official Node.js 14.x LTS image as the base
FROM node:14-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the app's source code
COPY . .

# Build the app
RUN npm run build


# Expose the container's port
EXPOSE 3000
ENV HOST=0.0.0.0
ENV PORT=3000


# Set the command to start the Nuxt.js app
CMD ["npm", "start"]

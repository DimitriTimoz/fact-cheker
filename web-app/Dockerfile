FROM node:22

# Set the working directory
WORKDIR /app

# Copy the package.json and lock files to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the Nuxt 3 application
RUN npm run build

# Expose the port the app runs on
EXPOSE 3000

# Command to start the application
# TODO: Change this to the correct command to start the application
CMD ["npm", "run", "preview"]

# ---- Base image ----
FROM node:20-alpine

# ---- Work directory ----
WORKDIR /app

# ---- Copy package files ----
COPY package*.json ./

# ---- Install deps ----
RUN npm install

# ---- Copy app ----
COPY . .

# ---- Expose Vite port ----
EXPOSE 5173

# ---- Run dev server ----
CMD ["npm", "run", "dev", "--", "--host"]

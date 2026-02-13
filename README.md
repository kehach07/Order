SV – Svelte Project

A modern Svelte project scaffolded using sv
.

This repository provides the essential setup to develop, build, and deploy a Svelte application efficiently.

🚀 Getting Started
Project Creation

This repository already contains a Svelte project created using sv.

For reference, you can create a new Svelte project using the following commands:

# Create a new project in the current directory
npx sv create

# Create a new project in a specific folder
npx sv create my-app

📦 Install Dependencies
npm install

🧑‍💻 Development Server

Start the local development server:

npm run dev


Open your browser and navigate to:

http://localhost:5173

🏗️ Build for Production
npm run build


Preview the production build locally:   

npm run preview

📁 Project Structure (Overview)
src/
├─ routes/        # Application routes
├─ lib/           # Reusable components & utilities
├─ app.html       # HTML template
└─ app.css        # Global styles
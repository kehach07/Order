# 🔐 Keycloak Authentication Integration – Order Menu

This project uses **Keycloak** as a centralized authentication and authorization server, integrated with a **Django REST Framework backend** and a **Svelte frontend** using **OAuth 2.0 / OpenID Connect (OIDC)**.

The goal is to securely handle **signup, signin, token validation, and protected APIs** without managing passwords manually in the backend.

---

## 🧠 Why Keycloak?

Keycloak provides:
- Centralized user management
- Secure JWT-based authentication
- OAuth 2.0 & OpenID Connect support
- Token lifecycle management (access & refresh tokens)
- Easy integration with frontend & backend apps

Backend trusts **only Keycloak-issued tokens**, not frontend requests.

---

## 🏗️ Architecture Overview

Frontend (Svelte)
|
| email + password
v
Backend (Django API)
|
| OAuth password grant
v
Keycloak (Auth Server)
|
| JWT access & refresh tokens
v
Backend validates token → serves APIs

yaml
Copy code

---

## 🐳 Keycloak Setup (Docker)

### 1️⃣ Pull Keycloak Image
```bash
docker pull quay.io/keycloak/keycloak:24.0.4
2️⃣ Run Keycloak
bash
Copy code
docker run -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:24.0.4 \
  start-dev
3️⃣ Admin Console
pgsql
Copy code
http://localhost:8080/admin
Username: admin
Password: admin
🌍 Realm Configuration
Realm Name
css
Copy code
order
A realm is an isolated space containing:

Users

Clients

Tokens

Roles

🧩 Clients Configuration
🔹 Backend Client (Required)
Field	Value
Client ID	order-backend
Protocol	OpenID Connect
Client authentication	❌ Off
Direct access grants	✅ On
Standard flow	❌ Off
Service accounts	❌ Off

Used by Django backend for:

Password login

Token validation

API security

🔹 Frontend Client (Optional)
Field	Value
Client ID	order-frontend
Purpose	Audience mapping / future UI auth

🧠 Why Mapper Is Required
❌ Problem
Backend rejected valid tokens with:

python
Copy code
Invalid or expired token
Root Cause
Token aud (audience) did not include order-backend.

🧩 Audience Mapper (Fix)
Path:

sql
Copy code
Clients → order-backend → Client scopes → Dedicated → Add mapper
Mapper Configuration
Field	Value
Name	order-backend-audience
Mapper Type	Audience
Included Client Audience	order-backend
Add to access token	✅ On
Add to ID token	❌ Off

Resulting Token Claim
json
Copy code
"aud": ["order-backend", "account"]
✅ Backend can now safely validate tokens.

👤 User Management Strategy
Admin-Created Users
Fully active by default

Login works immediately

API-Created Users (Signup)
We ensure:

enabled = true

temporary = false password

Email present in token

This fixes:

vbnet
Copy code
invalid_grant: Account is not fully set up
✍️ Signup Flow
bash
Copy code
POST /api/signup/
Steps
Create user in Django DB

Create user in Keycloak (Admin API)

Set permanent password

Enable user

Return success message

Signup does not return tokens (security best practice).

🔑 Signin Flow
bash
Copy code
POST /api/signin/
Payload
json
Copy code
{
  "email": "user@gmail.com",
  "password": "password"
}
Backend Actions
Validate user exists in DB

Request token from Keycloak:

sql
Copy code
/realms/order/protocol/openid-connect/token
Return:

json
Copy code
{
  "access": "<jwt>",
  "refresh": "<jwt>",
  "user": { ... }
}
🔐 Token Usage
Frontend sends:

http
Copy code
Authorization: Bearer <access_token>
Backend validates:

Signature (RS256)

Issuer

Audience (order-backend)

Email claim

🧾 Token Concepts (Important)
Claim	Meaning
aud	Who the token is intended for
azp	Client that requested the token
iss	Token issuer (Keycloak realm)
exp	Expiry time

⚙️ Environment Variables
env
Copy code
DEBUG=True
SECRET_KEY=django-insecure-super-secret-key

DB_NAME=ordermenu_db
DB_USER=ordermenu_user
DB_PASSWORD=strongpassword
DB_HOST=localhost
DB_PORT=5432

KEYCLOAK_SERVER_URL=http://localhost:8080
KEYCLOAK_REALM=order

KEYCLOAK_CLIENT_ID=order-backend
KEYCLOAK_CLIENT_SECRET=*****

KEYCLOAK_ADMIN_USERNAME=admin
KEYCLOAK_ADMIN_PASSWORD=admin

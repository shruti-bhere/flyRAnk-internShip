# Auth Protect API

A secure Node.js & Express REST API built with Supabase Authentication, JSON Web Tokens (JWT), Middleware protection, and interactive Swagger UI documentation.

## Features

- **User Authentication**: Sign Up and Log In handled via Supabase Auth.
- **JWT Protection**: Secure API endpoints using Bearer Tokens.
- **Custom Middleware**: Express middleware for token extraction and verification.
- **Session Termination**: Secure Logout handling.
- **API Documentation**: Interactive Swagger UI at `/docs`.

---

## Tech Stack

- **Runtime**: Node.js
- **Framework**: Express.js
- **Authentication**: Supabase Auth (`@supabase/supabase-js`)
- **API Docs**: Swagger UI (`swagger-ui-express`)

---

## Getting Started

### 1. Prerequisites
Ensure you have Node.js installed on your system.

### 2. Installation
Clone the repository and install the required dependencies:

```bash
git clone [https://github.com/YOUR_USERNAME/supabase-auth-api.git](https://github.com/YOUR_USERNAME/supabase-auth-api.git)
cd supabase-auth-api
npm install
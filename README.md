# LaunchDarkly Comic Character Full-Stack Demo

> **Note:** If you have trouble running the demo locally, a live version is available at:
> [http://launchdarklydemo-env.eba-k3kcg8hp.us-east-2.elasticbeanstalk.com/](http://launchdarklydemo-env.eba-k3kcg8hp.us-east-2.elasticbeanstalk.com/)

---

## Assumptions

- These instructions assume you are using [Homebrew](https://brew.sh/) to install system dependencies on macOS.
- Please ensure Homebrew is installed before proceeding with Node.js, Python, or other system-level dependencies.
- You will need to recreate the LaunchDarkly flags, segments, metrics, and AI config as shown in the screenshots in the "LD Configuration Pictures" folder and described in [LD OVERVIEW.md](./LD%20OVERVIEW.md).

---

This project demonstrates a full-stack application using LaunchDarkly feature flags, with a React + TypeScript frontend and a Flask backend. The app allows users to select comic characters, interact with feature-flag-driven UI, and integrates with OpenAI for dynamic responses.

---

## LaunchDarkly Overview

For a detailed explanation of the feature flags, segments, metrics, experimentation, and AI configuration used in this project, see [LD OVERVIEW.md](./LD%20OVERVIEW.md).

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Frontend Setup](#frontend-setup)
- [Backend Setup](#backend-setup)
- [API Integration](#api-integration)
- [Environment Variables](#environment-variables)
- [Customization](#customization)
- [Security](#security)

---

## Features

- Choose a random Marvel/DC comic character (hero or villain)
- Feature flag-driven UI (power bar, kill/save buttons, lightsaber, etc.)
- LaunchDarkly multi-context support and event tracking
- RESTful API endpoints (e.g., `/context` for multi-context payloads)
- OpenAI integration for dynamic responses
- Static file serving and modern, responsive UI
- Production-ready backend with Gunicorn and AWS Elastic Beanstalk support

---

## Architecture

- **Frontend:** React + TypeScript (Vite)
- **Backend:** Flask (Python), LaunchDarkly SDK, OpenAI API

---

## Frontend Setup

1. **Clone the repository and navigate to the frontend directory:**
   ```bash
   git clone <your-repo-url>
   cd launch-darkly-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure LaunchDarkly:**
   - Create a `.env` file in the project root with your LaunchDarkly client-side ID:
     ```
     VITE_LD_CLIENT_ID=your-client-side-id-here
     ```
   - (Optional) Adjust feature flag keys in the code to match your LaunchDarkly project.

4. **Run the development server:**
   ```bash
   npm run dev
   ```
   - The app will be available at [http://localhost:5173](http://localhost:5173) by default.

5. **Build for production:**
   ```bash
   npm run build
   ```
   - Output will be in the `dist/` folder.

---

## Backend Setup

1. **Clone the repository and navigate to the backend directory.**
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Copy the example environment file and fill in your secrets:**
   ```bash
   cp .env.example .env
   # Edit .env with your LaunchDarkly and OpenAI keys
   ```
5. **Run the app locally:**
   ```bash
   gunicorn app:app
   # Or for development:
   python app.py
   ```

---

## API Integration

- The frontend expects a `/context` API endpoint to POST user context and receive a response for display in the "The Voice" card.
- You can configure the API URL in `App.tsx` if needed.

---

## Environment Variables

- **Frontend:** `.env` with `VITE_LD_CLIENT_ID`
- **Backend:** `.env` with `LD_SDK_KEY` (LaunchDarkly SDK key), `OPENAI_API_KEY` (OpenAI API key)
- See `.env.example` in the backend for required keys.

---

## Customization

- Update comic character data in `src/types/ComicCharacter.ts` (frontend).
- Adjust feature flag keys and logic in `App.tsx` and components (frontend).
- Place static files in the backend's `static/` directory.

---

## Security

- Do **not** commit your `.env` files.
- Use environment variables for all secrets in production.

---

For more details, see comments in the code or ask for specific endpoint documentation.

---
# launch-darkly-demo

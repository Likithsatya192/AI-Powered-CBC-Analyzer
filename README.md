# Health AI Project

AI-powered medical analysis tool that processes medical documents (PDFs, Images, etc.) to provide insights, pattern recognition, Contextual analysis, Clinical synthesis and recommendations using advanced RAG (Retrieval-Augmented Generation) and LLMs.

## 🚀 Features

-   **Intelligent Document Analysis**: Upload medical reports (PDFs, Images, etc.) for automated analysis.
-   **RAG Chatbot**: Ask questions about your uploaded documents and get context-aware answers.
-   **Authentication**: Secure Google Sign-In and Email/Password authentication via Firebase.
-   **Modern UI**: Responsive, glassmorphism-styled frontend built with React and Tailwind CSS.
-   **Scalable Backend**: FastAPI-based backend with Pinecone vector database for efficient retrieval.
-   **Production Ready**: Dockerized application with CI/CD pipeline for AWS deployment.

## 🛠️ Tech Stack

-   **Frontend**: React, Vite, Tailwind CSS, Framer Motion, Firebase Auth
-   **Backend**: FastAPI, LangChain, Langgraph, Groq LLM
-   **Database**: Pinecone (Vector DB)
-   **Infrastructure**: Docker, Docker Compose, Nginx
-   **CI/CD**: GitHub Actions, AWS EC2

## ⚙️ Local Development Setup

### Prerequisites
-   Node.js (v18+)
-   Python (v3.10+)
-   Docker & Docker Compose

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd health_ai_project
```

### 2. Configure Environment Variables
Create a `.env` file in the `frontend` directory:
```bash
# frontend/.env
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

Create a `.env` file in the root directory for the backend (if running locally without Docker):
```bash
# .env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index_name
```

### 3. Run with Docker Compose
The easiest way to run the full stack:
```bash
docker-compose up --build
```
Access the application at `http://localhost`.

## 📦 AWS Deployment

This project is configured for automated deployment to AWS EC2 using GitHub Actions.

### 1. GitHub Secrets
You must configure the following Secrets in your GitHub Repository settings (**Settings > Secrets and variables > Actions**):

| Secret Name | Description |
| :--- | :--- |
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub access token/password |
| `EC2_HOST` | Public IP or DNS of your EC2 instance |
| `EC2_USER` | EC2 username (e.g., `ubuntu` or `ec2-user`) |
| `EC2_SSH_KEY` | Private SSH key for EC2 access |
| `GROQ_API_KEY` | API Key for Groq LLM |
| `VITE_FIREBASE_API_KEY` | Firebase API Key |
| `VITE_FIREBASE_AUTH_DOMAIN` | Firebase Auth Domain |
| `VITE_FIREBASE_PROJECT_ID` | Firebase Project ID |
| `VITE_FIREBASE_STORAGE_BUCKET` | Firebase Storage Bucket |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Firebase Messaging Sender ID |
| `VITE_FIREBASE_APP_ID` | Firebase App ID |
| `PINECONE_API_KEY` | API Key for Pinecone Vector DB |
| `PINECONE_INDEX_NAME` | Name of the Pinecone Index |

### 2. Deployment
Pushing to the `main` branch will automatically trigger the deployment workflow:
1.  Builds backend and frontend Docker images.
2.  Publishes images to Docker Hub.
3.  SSH into EC2, pulls new images, and restarts containers.

## 👨‍💻 Created By

**Likith Sagar**

-   **GitHub**: [Likithsatya192](https://github.com/Likithsatya192)
-   **Project**: Health AI - AI-Powered Medical Analysis Tool

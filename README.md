# Flask + MongoDB Kubernetes Deployment

## Project Overview
This project deploys a Flask application with MongoDB on Kubernetes. 
Endpoints:
- / : Welcome message with current time
- /data : POST to insert data, GET to retrieve data

## Folder Structure
flask-mongodb-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── .env
└── k8s/
    ├── namespace.yaml
    ├── mongo-secret.yaml
    ├── mongo-statefulset.yaml
    ├── mongo-service.yaml
    ├── flask-deployment.yaml
    ├── flask-service.yaml
    └── flask-hpa.yaml

## Local Setup
1. Setup virtual environment:
   python -m venv venv
   activate it (Windows: venv\Scripts\activate, Linux/Mac: source venv/bin/activate)
2. Install dependencies:
   pip install -r requirements.txt
3. Run MongoDB using Docker:
   docker pull mongo:latest
   docker run -d -p 27017:27017 --name mongodb mongo:latest
4. Set environment variable MONGODB_URI
5. Run Flask:
   flask run
6. Test API using curl or browser:
   curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://localhost:5000/data
   curl http://localhost:5000/data

## Kubernetes Deployment
1. Start Minikube:
   minikube start
2. Apply all YAML files:
   kubectl apply -f k8s/
3. Access Flask app:
   minikube service flask-service -n flask-mongo

## DNS Resolution
- Kubernetes automatically creates DNS entries for Services.
- Flask connects MongoDB using service name: mongodb://username:password@mongodb-service:27017/

## Resource Requests & Limits
- Requests: Minimum resources pod guaranteed
- Limits: Maximum resources pod can use
- Example:
  cpu: request 0.2, limit 0.5
  memory: request 250M, limit 500M

## Design Choices
- StatefulSet for MongoDB (data persistence)
- NodePort for Flask (local access)
- Secrets for MongoDB authentication
- HPA for autoscaling

## Testing Scenarios
1. API tests (POST/GET)
2. Scale replicas manually
3. Simulate high CPU load to test HPA
4. Verify MongoDB data persistence after pod restart

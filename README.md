# Iris API on Kubernetes

A small MLOps project: a classifier (Random Forest on the Iris dataset) exposed as a REST API with FastAPI, containerized with Docker, and deployed on Kubernetes (Minikube) with 3 replicas.

## Architecture

Client -> Service (NodePort) -> 3 `iris-api` Pods -> scikit-learn model

- The model is trained during the image build.
- A `readinessProbe` on `/health` ensures that traffic only reaches pods that are ready.
- The `servito_da` field in the response shows which pod handled the request, making load balancing visible.

## Getting started

```bash
minikube start
docker build -t iris-api:1.0 .
minikube image load iris-api:1.0
kubectl apply -f k8s.yaml
minikube service iris-api --url
```

## Testing

Replace `PORT` with the port returned by `minikube service`:

```bash
curl -X POST http://127.0.0.1:PORT/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":6.7,"sepal_width":3.0,"petal_length":5.2,"petal_width":2.3}'
```

Response: `{"specie":"virginica","servito_da":"iris-api-..."}`

## What it demonstrates

- Deployment with 3 replicas and self-healing (delete a pod and a new one replaces it)
- Service load balancing traffic across pods
- Immutable container: the model is baked into the image

## Stack

Python, scikit-learn, FastAPI, Docker, Kubernetes (Minikube)

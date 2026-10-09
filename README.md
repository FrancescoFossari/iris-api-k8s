# Iris API su Kubernetes

Piccolo progetto MLOps: un classificatore (Random Forest su dataset Iris) esposto come API REST con FastAPI, containerizzato con Docker e deployato su Kubernetes (Minikube) con 3 repliche.

## Architettura

Client -> Service (NodePort) -> 3 Pod `iris-api` -> modello scikit-learn

- Il modello viene addestrato durante il build dell'immagine.
- `readinessProbe` su `/health`: il traffico arriva solo ai pod pronti.
- Il campo `servito_da` nella risposta mostra il pod che ha risposto, così si vede il bilanciamento.

## Avvio

    minikube start
    docker build -t iris-api:1.0 .
    minikube image load iris-api:1.0
    kubectl apply -f k8s.yaml
    minikube service iris-api --url

## Test

    curl -X POST http://127.0.0.1:PORTA/predict \
      -H "Content-Type: application/json" \
      -d '{"sepal_length":6.7,"sepal_width":3.0,"petal_length":5.2,"petal_width":2.3}'

Risposta: `{"specie":"virginica","servito_da":"iris-api-..."}`

## Cosa dimostra

- Deployment con 3 repliche e self-healing (cancellando un pod ne nasce un altro)
- Service che bilancia il traffico tra i pod
- Container immutabile: il modello è dentro l'immagine

## Stack

Python, scikit-learn, FastAPI, Docker, Kubernetes (Minikube)

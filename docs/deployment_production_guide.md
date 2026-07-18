# HydroGrow AI Production & Kubernetes Deployment Guide

Complete enterprise production deployment instructions for Kubernetes and Cloud Platforms.

---

## 1. Kubernetes Cluster Deployment

### Prerequisites
- `kubectl` connected to your K8s cluster (EKS / GKE / AKS / Minikube)
- Ingress controller (Nginx Ingress Controller)

### Step-by-Step Deployment

1. **Create Secrets:**
   ```bash
   kubectl create secret generic hydrogrow-secrets \
     --from-literal=database-url="postgresql://user:pass@postgres-svc:5432/hydrogrow_db" \
     --from-literal=jwt-secret-key="production_jwt_key_here" \
     --from-literal=postgres-user="user" \
     --from-literal=postgres-password="pass"
   ```

2. **Deploy Manifests:**
   ```bash
   kubectl apply -f deployment/postgres-statefulset.yaml
   kubectl apply -f deployment/backend-deployment.yaml
   kubectl apply -f deployment/frontend-deployment.yaml
   kubectl apply -f deployment/ingress.yaml
   ```

3. **Verify Pod Readiness:**
   ```bash
   kubectl get pods -w
   ```

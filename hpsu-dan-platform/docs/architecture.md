# Architecture
## Stack
  Vue 3 + Three.js (Frontend)
  FastAPI (API Service)
  FastAPI (Inference Service)
  Adapter -> PyTorch (Algorithm)

## Principles
1. Algorithm isolated via adapter pattern
2. Dual-model (model1+model2) averaging
3. JWT + RBAC auth
4. Real + Demo inference modes
5. Auto-discovering research registry

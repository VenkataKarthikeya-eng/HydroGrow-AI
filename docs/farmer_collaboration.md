# HydroGrow AI Farmer Collaboration Ecosystem Guide

Guide detailing team invitations, role assignments, crop template publishing, and agricultural knowledge sharing.

---

## 1. Collaboration Workflows

1. **Team Invitations**: Farm owners invite members by email (`POST /api/farms/{farm_id}/members/add`) with assigned role (`MANAGER`, `WORKER`, `VIEWER`).
2. **Crop Marketplace**: Growers publish custom nutrient recipes (`POST /api/marketplace/templates/create`).
3. **Knowledge Base**: Diagnostic articles for water chemistry and nutrient lockout prevention.

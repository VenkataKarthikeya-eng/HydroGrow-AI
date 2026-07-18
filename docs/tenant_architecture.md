# HydroGrow AI Multi-Tenant Data Isolation Specification

Specification detailing tenant data isolation, authorization verification, and backward compatibility.

---

## 1. Multi-Tenant Authorization Rules

- Every API endpoint accepting `farm_id` verifies that the requesting `user_id` exists in `farm_members` for that farm.
- If a user attempts to access a farm where they lack membership, the backend returns HTTP 403 Forbidden.

---

## 2. Backward Compatibility for Existing Users

- Existing single-user accounts automatically provision a default farm ("My Smart Farm") on first login/access (`FarmManager.get_user_farms()`).
- No account re-creation or data loss occurs.

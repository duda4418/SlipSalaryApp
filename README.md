 # SlipSalaryApp Backend

Payroll reporting & distribution service providing secure generation and delivery of monthly salary CSV summaries and individual PDF salary slips. Implements manager‑triggered workflows, idempotent endpoints, auditing via archived files, and environment‑aware email sending.

---
## Table of Contents
1. Overview
2. Features
3. Architecture & Data Model
4. Environment & Configuration
5. Running Locally (Docker / Manual)
6. Authentication & Authorization
7. Report Generation & File Layout
8. Endpoints (Detailed)
9. Idempotency
10. Email Delivery (Dev vs Live)
11. Logging & Observability
12. Security Considerations
13. Common Usage Examples
14. Future Improvements

---
## 1. Overview
Managers can generate and send:
* A consolidated monthly CSV of subordinate employees (salary breakdown + vacation days).
* Individual, password‑protected PDF salary slips (password = employee CNP).
All sent files are archived for audit purposes.

## 2. Features
* Role‑based access (only `is_manager` users can trigger reporting endpoints).
* Idempotent report/email endpoints via `Idempotency-Key` header.
* Inline or disk file storage; archived copies maintained separately.
* Secure PDF generation with password protection (PyPDF2 + ReportLab).
* Development email isolation (MailHog) vs production SMTP safeguards.
* Structured request body models for clarity & OpenAPI documentation.
* Request logging middleware with per‑request correlation ID.

## 3. Architecture & Data Model
Core tables:
* `employees` – hierarchical (self `manager_id`), base salary, identity info.
* `salary_components` – monthly components (bonus / adjustment / base snapshot).
* `vacations` – monthly vacation days taken.
* `months` – reference working days per month (normalization & deterministic calc).
* `report_files` – metadata + optional binary content for CSV/PDF/ZIP.
* `idempotency_keys` – tracks endpoint signature, status, result path.
* `refresh_tokens` – secure refresh token rotation.

Repository layer has been modularized under `db/repositories/` (each entity separated for maintainability).

## 4. Environment & Configuration
Primary environment variables (see `core/settings.py`):
```
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_FROM=slipsalary@example.com
SMTP_TLS=False
SMTP_USERNAME=
SMTP_PASSWORD=
LOG_LEVEL=INFO
JWT_SECRET_KEY=changeme
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=1440
```
Production override example:
```
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_FROM=payroll@example.com
SMTP_TLS=True
SMTP_USERNAME=apikey
SMTP_PASSWORD=SG.xxxxxx
```

## 5. Running Locally
### Docker (recommended)
```
docker compose up -d
```
Services:
* Postgres (persistent volume `pgdata`).
* MailHog (SMTP @ 1025, UI @ http://localhost:8025).

### Manual
1. Ensure Postgres running & `.env` configured.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run app:
   ```
   python main.py
   ```

## 6. Authentication & Authorization
* `POST /api/auth/login` returns JWT access + refresh tokens.
* `POST /api/auth/refresh` rotates refresh token.
* Protected routers depend on `require_manager` ensuring `is_manager=True`.

## 7. Report Generation & File Layout
Generated paths:
```
reports/csv/<YYYY-MM>/<managerUuid>.csv
reports/pdf/<YYYY-MM>/<employeeUuid>.pdf
reports/archives/<YYYY-MM>/<managerUuid>_pdfs.zip
reports/archives/<YYYY-MM>/<managerUuid>.csv
reports/archives/<YYYY-MM>/pdfs/<employeeUuid>.pdf
```
Archive occurs only after send endpoints to match auditing requirement.

## 8. Endpoints (Detailed)
Prefix groups: `/api/reports_generation`, `/api/reports`, `/api/employees`.

### Reports Generation (JSON body models)
All require header `Idempotency-Key` (optional for idempotency) and manager role.

1. `POST /api/reports_generation/createAggregatedEmployeeData`
   Body:
   ```json
   {"manager_id":"<uuid>","year":2025,"month":11,"include_bonuses":true}
   ```
   Returns: `{"status":"generated","fileId", "filePath", "archived":false}` or cached.

2. `POST /api/reports_generation/sendAggregatedEmployeeData`
   Body same as above (include_bonuses ignored for sending; CSV regens with bonuses default True).
   Returns: sent or cached; archives CSV.

3. `POST /api/reports_generation/sendAggregatedEmployeeDataLive`
   Live SMTP variant; additional SMTP configuration validation.

4. `POST /api/reports_generation/createPdfForEmployees`
   Body:
   ```json
   {"manager_id":"<uuid>","year":2025,"month":11,"overwrite_existing":false}
   ```
   Generates PDFs (not archived yet).

5. `POST /api/reports_generation/sendPdfToEmployees`
   Body:
   ```json
   {"manager_id":"<uuid>","year":2025,"month":11,"regenerate_missing":false}
   ```
   Sends via dev SMTP (MailHog), archives each PDF + ZIP bundle.

6. `POST /api/reports_generation/sendPdfToEmployeesLive`
   Same body, production SMTP safeguards, returns `status: "sent_live"`.

### Reports CRUD
* `GET /api/reports` list report file metadata.
* `GET /api/reports/{report_id}` single metadata (supports `{uuid}.pdf` style via normalization).
* `GET /api/reports/{report_id}/download` raw content (inline DB bytes or disk fallback).
* `POST /api/reports` create metadata.
* `PUT /api/reports/{report_id}` update.
* `DELETE /api/reports/{report_id}` delete.

### Employees
* `GET /api/employees` all employees (manager restricted).
* `GET /api/employees/manager/{manager_id}` subordinates of manager.
* `GET /api/employees/{employee_id}` single employee.
* `POST /api/employees` create.
* `PUT /api/employees/{employee_id}` update.
* `DELETE /api/employees/{employee_id}` remove.

## 9. Idempotency
Provide `Idempotency-Key` header with a unique string per logical action. The backend:
* Stores `(key, endpoint signature, status)` row.
* On repeat call with same signature + `succeeded` returns cached response.
* If `started` in progress → 409 Conflict.
* Missing failure marking (future improvement: set `failed` on exception).

## 10. Email Delivery
Two code paths:
* Dev: `send_email_dev` (forces `localhost:1025`, ignores .env) to prevent accidental real sends.
* Live: `send_email` uses configured SMTP; live endpoints enforce non‑localhost & TLS/auth presence.
Attachments added as `application/octet-stream` for simplicity (can refine per MIME later).

## 11. Logging & Observability
`RequestLoggingMiddleware` logs: method, path, status, duration_ms, request_id. Response header `X-Request-ID` aids tracing. Additional domain logs inside email service & error paths.

## 12. Security Considerations
* JWT-auth; minimal claims (manager flag + email).
* PDF password = CNP (improvement: hash CNP at rest; derive password dynamically).
* Ensure least privilege on database roles externally.
* Path traversal risk mitigated by controlled generation paths (future: validate `report.path` prefix before download).

## 13. Usage Examples
Generate CSV:
```bash
curl -X POST http://localhost:8000/api/reports_generation/createAggregatedEmployeeData \
  -H "Authorization: Bearer <token>" \
  -H "Idempotency-Key: gen-csv-2025-11-mgr123" \
  -H "Content-Type: application/json" \
  -d '{"manager_id":"<uuid>","year":2025,"month":11,"include_bonuses":true}'
```
Send PDFs (dev):
```bash
curl -X POST http://localhost:8000/api/reports_generation/sendPdfToEmployees \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"manager_id":"<uuid>","year":2025,"month":11,"regenerate_missing":false}'
```

## 14. Future Improvements
| Area | Enhancement |
|------|-------------|
| Idempotency | Add failure status + cleanup of stale `started` keys |
| Security | Encrypt or hash CNP, remove from standard responses |
| Email | Rate limiting, bounce tracking, retry strategy |
| API | Pagination for large employee/report lists |
| Storage | External object storage (S3) for large files |
| PDFs | Styled templates (HTML → PDF) & localized formatting |
| Monitoring | Metrics (Prometheus) for generation/send timings |
| Tests | Expand unit/integration coverage for all services |

---
## License / Internal Use
Currently intended for internal academic/demo purposes. Add LICENSE if distributing publicly.

---
## Quick Reference Cheat Sheet
* Generate CSV → `createAggregatedEmployeeData`
* Send CSV (dev/live) → `sendAggregatedEmployeeData` / `sendAggregatedEmployeeDataLive`
* Generate PDFs → `createPdfForEmployees`
* Send PDFs (dev/live) → `sendPdfToEmployees` / `sendPdfToEmployeesLive`
* Download any file → `/api/reports/{id}/download` (supports `{id}.pdf` etc.)

Happy reporting! 🧾

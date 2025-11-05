# Reporting & Distribution Endpoints

## New Endpoints (prefix /api/reports_generation)

1. POST /api/reports_generation/createAggregatedEmployeeData
   Generate CSV for manager's subordinates for given year/month.
   Query Params: managerId, year, month, includeBonuses (optional)
   Response: { fileId, path, archived }

2. POST /api/reports_generation/sendAggregatedEmployeeData
   Generate (if needed) then email CSV to manager; marks archived.
   Query Params: managerId, year, month
   Response: { status, fileId, archived }

3. POST /api/reports_generation/createPdfForEmployees
   Generate password-protected PDFs for each subordinate employee.
   Query Params: managerId, year, month, overwriteExisting (optional)
   Response: { generated, fileIds }

4. POST /api/reports_generation/sendPdfToEmployees
   Email PDFs to each employee then archive them into a ZIP (dev/local SMTP, e.g. MailHog).
   Query Params: managerId, year, month, regenerateMissing (optional)
   Response: { sent, archiveZipId, archivePath }

5. POST /api/reports_generation/sendPdfToEmployeesLive
   Same behaviour as #4 but enforces production SMTP configuration (non-local host + TLS or auth).
   Query Params: managerId, year, month, regenerateMissing (optional)
   Response: { sent, archivedPdfs, archiveZipId, archiveZipPath, status: "sent_live" }

6. POST /api/reports_generation/sendAggregatedEmployeeDataLive
   Production variant of manager CSV sending (non-local SMTP safeguards).
   Query Params: managerId, year, month
   Response: { status: "sent_live", fileId, archived, archivePath }

## CSV Columns
employee_id, first_name, last_name, cnp, gross_salary_month, base_salary, bonus_total, adjustment_total, working_days, vacation_days

## PDF Password
Each PDF is protected using the employee's CNP.

## Files Layout
- reports/csv/<year-month>/<managerId>.csv
- reports/pdf/<year-month>/<employeeId>.pdf
- reports/archives/<year-month>/<managerId>_pdfs.zip

## Dependencies Added
reportlab, PyPDF2 for PDF generation.

## Future Improvements
- Production email hardening (rate limiting, bounce tracking) ⬅ next
- Role-based authorization for manager triggers
- Remove password_hash from public Employee responses
- Add tests for report generation

## Email Delivery (MailHog)

Emails are now sent via SMTP using MailHog for local development.

### Docker Service
MailHog service is defined in `docker-compose.yml` and exposes:
- SMTP: localhost:1025
- Web UI: http://localhost:8025

Start services:
```
docker compose up -d
```

Access the MailHog UI to view captured emails and attachments.

### Environment Variables
The following settings (with defaults) are defined in `core/settings.py`:
```
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_FROM=david.serban@endava.com
SMTP_TLS=False
SMTP_USERNAME=
SMTP_PASSWORD=
```
Override them in `.env` for production, e.g.:
```
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_FROM=payroll@example.com
SMTP_TLS=True
SMTP_USERNAME=apikey
SMTP_PASSWORD=SG.xxxxxx
```

### Attachment Notes
CSV, PDF, and ZIP files are attached using a generic `application/octet-stream` MIME type for simplicity.

### Error Handling
Failures when reading attachments or sending will be logged; endpoints still return success for unrelated attachments.

### Live Email Endpoint
Use `POST /api/reports_generation/sendPdfToEmployeesLive` only after configuring real SMTP. Safeguards:
- Rejects if SMTP_HOST is localhost / 127.0.0.1
- Requires TLS or username/password

### Production Reminder
Replace MailHog with a real provider (e.g., SES, SendGrid) and enable TLS/auth in production. Add rate limiting & auditing.

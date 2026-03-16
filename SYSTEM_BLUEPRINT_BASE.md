# 🏛️ Hostel ERP - Core Architecture (vFinal + UI/UX + WhatsApp)

## 1. Project Vision
A state-of-the-art Hostel Management System focused on financial integrity, operational control, and "Smart" occupancy tracking.
* **Target Start Date:** Data entry begins Jan 1, 2026.
* **Hosting:** Krystal Hosting (cPanel/Linux).
* **Tech Stack:** Python (Flask) + MySQL + React (Glassmorphism UI).

## 2. Governance & Security
* **Owner:** Full access + "Personal Withdrawal" Ledger + Audit Logs.
* **Manager:** Approval authority for Expenses, Move-outs, and Task Priority.
* **Admin:** Data Entry, Document Upload, Micro-Task Execution.
* **Audit Trail:** Immutable logs. "Soft Deletes" only. No financial record deletion without Manager approval.

## 3. Core Modules
### A. The "Smart" Onboarding Wizard (Manual Backfill)
* **Goal:** Replace CSV import with a structured entry form.
* **Required Fields:** Tenant Name (Eng/Urdu), CNIC, Phone, Emergency Contact, Room #, Bed Label, Rent Amount, Security Deposit.
* **Mandatory Uploads:** 1. ID Card (Front & Back). 2. Signed Tenancy Agreement. 3. Police Verification Form.
* **Status Flags:** Police Verification (Pending/Submitted/Verified), Agreement (Pending/Signed).

### B. Occupancy & Room Logic
* **Room Categories:** Small (Max 2), Medium (Max 3), Large (Max 5).
* **Ghost Slots:** If a Shared Room has capacity (e.g., 2 people in a 3-person room), the system must show "1 Vacant Bed" on the dashboard.
* **Rent Logic:** Per Head (Default) / Room Buyout (Fixed).
* **Billing Profile:** Individual rent amounts and due dates per tenant.

### C. Operational "Micro-Tasking"
* **Priority Meter:**
    * 🔴 **High:** Urgent Safety/Repairs.
    * 🟡 **Medium:** Daily Routine.
    * 🔵 **Low:** Service Queue (Carpenter/Plumber).
* **Task Proof:** Photo upload required for specific tasks.

### D. Financial Engine
* **Double-Entry Logic:** Business Expenses vs. Owner Personal Withdrawals.
* **Owner Personal Ledger:** Requires "Sub-Note" to explain usage.
* **Billing Cycle:** 1st of Month. Grace period till 5th.

## 4. UI/UX Design System ("Apple-Glass 2026")
* **Framework:** Tailwind CSS + Framer Motion.
* **Style Guide:** Glassmorphism (`backdrop-filter: blur(12px)`). Dark Mode default.
* **Responsiveness:** Mobile First (Thumb-Friendly buttons).

## 5. Connectivity & Automation
* **WhatsApp Bridge:** Alerts for Bills, Rent, Police Checks. Interactive "Mark Done" buttons for tasks.

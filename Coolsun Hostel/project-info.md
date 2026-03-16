# 🏨 COOLSUN HOSTEL ERP - MASTER HANDOVER (v1.2.0)
**Project State:** Feature Expansion Phase (Room Management & Parity Audit Complete)
**Design Era:** Apple-Glass 2026 (Glassmorphism)
**Year:** 2026

## 1. MISSION & ARCHITECTURE
This is a SaaS-level Hostel Management System designed to eliminate manual registers and provide "War Room" visibility for the Owner.

### Tech Stack:
- **Frontend:** React, Tailwind CSS, Framer Motion (Animations), Recharts (Analytics), Lucide-React (Icons).
- **Backend:** Flask (Python), SQLAlchemy ORM.
- **Database:** SQLite (`hostel.db`).
- **Styling:** Custom "Apple-Glass" (Void background $#020617$, Backdrop Blurs, 1px White/10 Borders).

---

## 2. CORE BUSINESS LOGIC (THE ALGORITHMS)

### A. The "15-Day Rule" (Pro-rata Billing)
- **Logic:** If a tenant joins on or before the 15th of the month, they pay for the remaining days of the current month + security deposit. 
- **Rule:** If they join after the 15th (16th onwards), the system **automatically** charges for (Remaining Days of Current Month) + (Full Next Month Rent) + (Security Deposit).
- **Formula:** `(Rent / 30 * DaysRemaining) + NextMonthRent + Deposit`.

### B. Compliance Aging Protocol
- **Logic:** New tenants have a 7-day grace period.
- **Traffic Lights:**
    - **GREEN:** Verified (Police form submitted).
    - **YELLOW:** Warning (Missing forms, but within 7-day grace).
    - **RED:** CRITICAL (Missing forms after 7 days OR expired CNIC).

### C. The Daily Closing (Shift Handover)
- **Mathematical Formula:** `Expected Cash = Opening Balance + Daily Collections - Daily Cash Expenses`.
- **Integrity:** The system flags a "Discrepancy" if physical cash does not match Expected Cash.

---

## 3. UI/UX BLUEPRINT (THE "GLASS" SPEC)

### A. Global Layout Structure
The UI uses a **Fixed Sidebar + Fluid Stage** grid system.
- **Sidebar:** `z-[105]`, `w-64`, fixed. High-contrast white/80 icons.
- **Main Stage:** `overflow-y-auto`, `max-w-[1600px]`, centered.
- **Background:** `bg-void` ($#020617$) with a fixed radial mesh gradient.

### B. Component Specifics
- **Glass Cards:** `bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl`.
- **Modals:** Must use `z-[110]` with a `backdrop-blur-md` overlay. Logic includes `document.body.style.overflow = 'hidden'` to prevent double-scrolling.
- **Typography:** `clamp(0.75rem, 1vw + 0.5rem, 1.125rem)` (Fluid typography for all display sizes).

---

## 4. DATABASE SCHEMA (MODELS)
- **Room:** Number, Type (Big/Small), Floor, Capacity, Base Rent.
- **Tenant:** Name, CNIC, Phone, Emergency Contact, Police Form Status, Bed ID, CNIC Expiry.
- **BillingProfile:** Rent Amount, Security Deposit, Due Date.
- **Expense:** Amount, Category (Utility/Repair/Personal), Paid From (Cash Drawer/Bank).
- **MaintenanceRequest:** Priority (Critical/Routine), Status (Open/Resolved), Cost.

---

## 5. NAVIGATION & ACCESS CONTROL
- **Role: MANAGER:** Access to Dashboard, Wizard, and Maintenance.
- **Role: OWNER:** Access to **Financial Ledger**, **Reports**, and **System Settings**.
- **Route Guarding:** ProtectedRoute logic prevents URL-guessing to bypass login.

---

## 6. RECENT FIXES & AUDIT LOG (IMPORTANT)
1. **The "Ghost Backdrop" Fix:** All modals now have a mandatory `onClick` safety-exit on the backdrop. 
2. **Z-Index Layering:** Corrected a conflict where the sidebar was being covered by invisible overlays.
3. **Sidebar Visibility:** Switched from Flex to a hard CSS Grid (`260px 1fr`) to ensure the menu never collapses to 0px.
4. **Room Management**: Implemented "Room Inventory" module with capacity guards and dynamic rent.
5. **Data Parity Audit**: Exposed partial payments, owner notes, and consolidated tenant fields (Bed Label, Compliance, Phone).

---

## 7. NEXT STEPS FOR ANTI-GRAVITY
1. **Backend Integration**: Verify/Flush migrations for `base_rent` and `emergency_contact`.
2. **Bulk WhatsApp Generator**: Implement the background task to send PDFs to all 45 tenants.
3. **Settings API**: Connect the Settings page to the database `HostelConfig` table.

---

## 8. STAFF OPERATIONS (ROMAN URDU SUMMARY)
*(For Anti-Gravity to use in voice-response or staff guidance)*
- **Onboarding:** Wizard use karein, photos upload karein, system ka "15-day rule" follow karein.
- **Finance:** Rent collect karte waqt "Cash" ya "Bank" choose karein.
- **Closing:** Raat 10 baje cash physical ginein aur system se match karein.
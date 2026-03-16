# 📱 Mobile Staff Guide - Coolsun Hostel ERP
*Copy and paste these instructions to your Managers via WhatsApp.*

## 🔐 1. How to Login
1.  Open the App Link (e.g., `http://localhost:3000/login`).
2.  Enter Username: `admin@coolsun.com`
3.  Enter Password: `password`
4.  Tap **Enter System**.

## 🚦 2. The War Room (Dashboard)
This is your home screen. It auto-refreshes every 15 minutes.
*   **Green/Yellow/Red Lights**: These show Compliance Health.
    *   **RED** means "Critical" (e.g., Missing Police Form for >30 days).
    *   *Action*: Click the Red light to see who is non-compliant.
*   **Issue Inbox**: Shows "Open Tickets".
    *   *Action*: Tap a ticket to "Resolve" it.
    *   *Costing*: If you pay for a repair, toggle **"Paid from Cash Drawer?"** to YES. This keeps your cash count accurate.

## 📝 3. Onboarding New Tenants (The Wizard)
1.  Go to **Menu > Wizard**.
2.  **Step 1**: Tap a Room (Green = Available).
3.  **Step 2**: Enter Tenant Name & Phone.
4.  **Step 3 (Money)**: Enter "Rent" and "Move-In Date".
    *   *Coolsun Calculator*: The system will tell you exactly how much to charge (Prorated Rent + Deposit).
    *   *Override*: If you take less money, turn on "Manager Override" and enter the amount. The rest becomes "Arrears".
5.  **Step 4 (Photos)**: Take 3 photos: ID Front, ID Back, Tenant Face.
6.  **Step 5**: Tap **Confirm**.

## 🌙 4. Daily Closing (End of Shift)
1.  Go to the Dashboard bottom card **"Daily Closing"**.
2.  Enter your **Opening Balance** (Cash you started with).
3.  The system calculates: `Opening + Collected - Expenses = Cash In Hand`.
4.  Count your physical cash. It MUST match "Cash In Hand".
5.  Tap **Submit Handover**.

---

### 📢 WhatsApp Broadcast Templates
*Use these templates for quick communication.*

**Template A: Daily Closing Report**
> 🌙 **Coolsun Daily Closing**
> 📅 Date: {{DATE}}
>
> 💵 **Cash Report**
> Opening: Rs. {{OPENING}}
> + Collected: Rs. {{COLLECTED}}
> - Expenses: Rs. {{EXPENSES}}
> = **Handover Cash: Rs. {{CLOSING}}**
>
> ⚠️ **Alerts**
> Critical Compliance: {{RED_COUNT}}
> Open Maintenance: {{OPEN_ISSUES}}
>
> *System Generated Report*

**Template B: Rent Reminder (Polite)**
> Assalam-o-Alaikum {{NAME}},
> This is a reminder from Coolsun Hostel. Your rent of Rs. {{AMOUNT}} is due.
> Please clear it by {{DATE}} to avoid late fees.
> Thank you!

**Template C: Maintenance Resolved**
> ✅ **Ticket Resolved**
> Issue: {{ISSUE_DESC}}
> Status: Fixed
> We hope you are comfortable!

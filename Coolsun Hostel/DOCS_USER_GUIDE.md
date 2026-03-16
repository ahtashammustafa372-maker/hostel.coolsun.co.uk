# 📘 Hostel ERP - Manager's User Guide (v1.0.0)

## 1. The Onboarding Wizard
The **Onboarding Wizard** is your primary tool for adding new tenants. It replaces the old CSV method with a secure, 5-step process.

### Step-by-Step Walkthrough
1.  **Select Room**:
    -   Click on a Room Card.
    -   **Green**: Available. **Red**: Full.
    -   *Note*: The grid shows "Ghost Slots" (Vacant Beds). If a room says "1 Bed Available," check the visual icons to confirm.
2.  **Tenant Details**:
    -   **Name**: Enter in English or Urdu.
    -   **Bed Label**: Be specific (e.g., "Window Side", "Bed A"). This helps in disputes.
    -   **CNIC Expiry**: Enter the date from the back of the card.
3.  **Financial Setup (The Coolsun Calculator)**:
    -   Enter **Rent** and **Move-In Date**.
    -   The system automatically calculates the **Initial Payment**.
    -   **Manager Override**: Toggle this if you need to accept a partial payment. The system will log the difference as "Pending Arrears."
4.  **Documents**:
    -   Upload **ID Front**, **ID Back**, and **Live Photo**.
    -   Ensure photos are clear and legible.
5.  **Review & Submit**:
    -   Verify all details.
    -   Click "Confirm" to save data and trigger the WhatsApp Welcome Message.

---

## 2. Financial Explainer: The 15-Day Rule
**Why does the system ask for more money after the 15th?**

To ensure secure cash flow and prevent small, annoying bills, we use the **15-Day Rule**:

*   **Scenario A: Move-in 1st – 15th**
    *   **Rule**: Pay Pro-rata for the remaining days of the current month.
    *   *Example*: Move in Jan 10th. Pay for Jan 10–31 (21 days). Next bill: Feb 1st.
*   **Scenario B: Move-in 16th – End of Month**
    *   **Rule**: Pay Pro-rata + **Full Next Month's Rent**.
    *   *Example*: Move in Jan 20th. Pay for Jan 20–31 (11 days) **PLUS** Full February Rent.
    *   *Why?* If we only charged for 11 days, we'd have to chase the tenant again on Feb 1st (just 10 days later). This collects it upfront.

---

## 3. Biometric & Document Standards
For the **Triple-Document Upload**, strictly follow these standards:

1.  **CNIC Front/Back**:
    -   **Lighting**: No glare or flash reflection on the text.
    -   **Frame**: All 4 corners of the card must be visible.
    -   **Clarity**: Text must be readable (zoom in to check).
2.  **Tenant Photo**:
    -   **Style**: Passport-style or clear selfie.
    -   **Background**: Neutral/Plain preferred.
    -   **Face**: No sunglasses or masks.

---

## 4. Error Handling & Troubleshooting
### "Ghost Slot" Error (Room Conflict)
*   **Message**: *"No vacancies in this room"* or *"Room just filled!"*
*   **Cause**: Another admin booked the last bed in that room while you were typing.
*   **Solution**:
    1.  Refresh the page.
    2.  Select a different room or bed.
    3.  Apologize to the tenant and explain the high demand!

### Upload Failures
*   **Issue**: Upload sticks at "99%" or fails.
*   **Cause**: Internet timeout or file too large (>5MB).
*   **Solution**:
    1.  Check file size. Compress if needed.
    2.  Retry. The system is "Atomic" – if it fails, **no data is saved**, so you won't create "duplicate" or "half" tenants. Just try again.

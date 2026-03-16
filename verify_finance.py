import requests
import time

BASE_URL = "http://127.0.0.1:5000/api"

def get_summary():
    r = requests.get(f"{BASE_URL}/dashboard/summary")
    return r.json()['financials']

print("--- Initial Summary ---")
initial = get_summary()
print(f"Collected: {initial['current_collected']}, Expenses: {initial['current_expenses']}, Net: {initial['net_cash']}")

print("\nAdding Rs. 3000 expense (Repair)...")
payload = {
    "category": "Repairs",
    "amount": 3000,
    "description": "Test Repair"
}
r_post = requests.post(f"{BASE_URL}/finance/expenses", json=payload)
if r_post.status_code == 201:
    print("Expense added successfully.")
else:
    print(f"Failed to add expense: {r_post.text}")
    exit(1)

print("\n--- Summary After Expense ---")
updated = get_summary()
print(f"Collected: {updated['current_collected']}, Expenses: {updated['current_expenses']}, Net: {updated['net_cash']}")

expected_net = updated['current_collected'] - updated['current_expenses']
if updated['net_cash'] == expected_net:
    print("\n✅ Verification Success: Net Cash is correctly calculated.")
else:
    print(f"\n❌ Verification Failed: Expected {expected_net}, got {updated['net_cash']}")

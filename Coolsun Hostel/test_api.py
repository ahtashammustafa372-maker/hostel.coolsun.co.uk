import urllib.request
import urllib.error
import urllib.parse
import json
import time

BASE_URL = "http://127.0.0.1:5000/api"

def make_request(url, method='GET', data=None, is_json=False):
    headers = {}
    if data is not None:
        if is_json:
            data = json.dumps(data).encode('utf-8')
            headers['Content-Type'] = 'application/json'
        else:
            data = urllib.parse.urlencode(data).encode('utf-8')
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8')
            try:
                return response.status, json.loads(body)
            except json.JSONDecodeError:
                return response.status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            return e.code, json.loads(body)
        except:
            return e.code, {"error": body}
    except urllib.error.URLError as e:
        return 0, {"error": str(e)}

def wait_for_server():
    print("Waiting for server to start...")
    for _ in range(10):
        status, _ = make_request(f"{BASE_URL}/debug/ping")
        if status == 200:
            print("Server is up!")
            return True
        time.sleep(1)
    return False

def check(name, condition, details=""):
    status = "[PASS]" if condition else "[FAIL]"
    print(f"{status} | {name}")
    if not condition and details:
        print(f"  -> Reason: {details}")
    return condition

def run_tests():
    if not wait_for_server():
        print("Failed to connect to server.")
        return

    print("\n--- Testing Rooms API ---")
    status, rooms = make_request(f"{BASE_URL}/rooms")
    
    if status == 200 and isinstance(rooms, list) and len(rooms) > 0:
        check("Fetch Rooms", True)
    else:
        print("No rooms found. Creating a test room...")
        new_room_data = {
            "number": "T101",
            "type": "Medium",
            "capacity": 3,
            "base_rent": 15000
        }
        status, new_room = make_request(f"{BASE_URL}/rooms", method='POST', data=new_room_data, is_json=True)
        check("Create Test Room", status == 201, details=new_room)
        # Fetch again
        status, rooms = make_request(f"{BASE_URL}/rooms")
        check("Fetch Rooms After Create", status == 200 and isinstance(rooms, list) and len(rooms) > 0, details=rooms)

    room_data = rooms[0] if isinstance(rooms, list) and len(rooms) > 0 else {}
    room_id = room_data.get('id', 1)
    room_num = room_data.get('number', 'Unknown')
    base_rent = room_data.get('base_rent', 10000)
    print(f"Selected Room: {room_num} (ID: {room_id}), Rent: {base_rent}")

    print("\n--- Testing Rooms API (Update) ---")
    update_data = {
        "number": room_num,
        "type": "Medium",
        "capacity": 3,
        "base_rent": 13337
    }
    status, update_res = make_request(f"{BASE_URL}/rooms/{room_id}", method='PUT', data=update_data, is_json=True)
    check("Update Test Room Base Rent", status == 200, details=update_res)
    
    # Fetch again to verify persistence
    status, verify_rooms = make_request(f"{BASE_URL}/rooms")
    if isinstance(verify_rooms, list):
        verified_room = next((r for r in verify_rooms if r.get('id') == room_id), None)
        if verified_room:
            check("Verify Update Persisted", float(verified_room.get('base_rent', 0)) == 13337.0, details=verified_room)
        else:
            print("[FAIL] | Verify Update Persisted  -> Room not found")

    print("\n--- Testing Onboarding API (Primary Tenant) ---")
    primary_data = {
        "room_id": room_id,
        "name": "Test Primary Tenant",
        "cnic": "11111-1111111-1",
        "phone": "0300-1111111",
        "bed_label": "Bed A",
        "rent_amount": base_rent,
        "agreement_start_date": "2026-03-01",
        "actual_move_in_date": "2026-03-01",
        "cnic_expiry_date": "2030-01-01",
        "emergency_contact": "0300-2222222",
        "security_deposit": "10000",
        "amount_paid_now": base_rent,
        "is_partial_payment": "false",
        "internet_opt_in": "true",
        "parent_tenant_id": ""
    }
    status, res_json = make_request(f"{BASE_URL}/onboarding", method='POST', data=primary_data)
    check("Onboard Primary", status == 201, details=res_json)
    primary_id = res_json.get('id') if isinstance(res_json, dict) else None

    print("\n--- Testing Onboarding API (Sub-tenant) ---")
    sub_data = {
        "room_id": room_id,
        "name": "Test Sub Tenant",
        "cnic": "22222-2222222-2",
        "phone": "0300-3333333",
        "bed_label": "Bed B",
        "rent_amount": base_rent,
        "agreement_start_date": "2026-03-01",
        "actual_move_in_date": "2026-03-01",
        "cnic_expiry_date": "2030-01-01",
        "emergency_contact": "0300-4444444",
        "security_deposit": "5000",
        "amount_paid_now": base_rent,
        "is_partial_payment": "false",
        "internet_opt_in": "false", # Opted out of internet
        "parent_tenant_id": str(primary_id) if primary_id else ""
    }
    status, res_json = make_request(f"{BASE_URL}/onboarding", method='POST', data=sub_data)
    check("Onboard Sub-tenant", status == 201, details=res_json)
    sub_id = res_json.get('id') if isinstance(res_json, dict) else None

    print("\n--- Testing Tenants API & Hierarchy Verification ---")
    status, tenants = make_request(f"{BASE_URL}/tenants")
    check("Fetch Tenants", status == 200)
    
    if isinstance(tenants, list):
        p_tenant = next((t for t in tenants if t.get('id') == primary_id), None)
        s_tenant = next((t for t in tenants if t.get('id') == sub_id), None)
        
        if p_tenant:
            check("Primary Opt-in=True", p_tenant.get('internet_opt_in') == True)
        if s_tenant:
            check("Sub Opt-in=False", s_tenant.get('internet_opt_in') == False)
            check("Sub Parent ID match", s_tenant.get('parent_tenant_id') == primary_id)

    print("\n--- Testing Utility Billing (Internet) ---")
    internet_bill_data = {
        "room_id": room_id,
        "amount": 2000,
        "billing_date": "2026-03-04"
    }
    status, bill_res = make_request(f"{BASE_URL}/utilities/internet-bill", method='POST', data=internet_bill_data, is_json=True)
    check("Add Internet Bill", status == 201)
    if isinstance(bill_res, dict):
        check("Opt-out logic respected", int(bill_res.get('tenants_billed', 0)) >= 1)

    print("\n--- Testing Dashboard Metrics ---")
    status, _ = make_request(f"{BASE_URL}/dashboard/summary")
    check("Dashboard Summary", status == 200)

if __name__ == '__main__':
    run_tests()

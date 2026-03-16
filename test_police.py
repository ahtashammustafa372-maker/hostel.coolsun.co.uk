import urllib.request
import urllib.error
import urllib.parse
import json

BASE_URL = "http://127.0.0.1:5000/api"

def make_request(url, method='GET', data=None, is_json=False, headers=None):
    if headers is None:
        headers = {}
    if data and is_json:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
        
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            try:
                return response.getcode(), json.loads(res_body)
            except json.JSONDecodeError:
                return response.getcode(), res_body
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        try:
            return e.code, json.loads(err_body)
        except json.JSONDecodeError:
            return e.code, err_body
    except urllib.error.URLError as e:
        return 0, str(e)

def check(name, condition, details=""):
    if condition:
        print(f"[PASS] | {name}")
    else:
        print(f"[FAIL] | {name}")
        print(f"  -> Reason: {details}")

print("\n--- Testing Police Verification API ---")

# 1. Fetch Records
status, records = make_request(f"{BASE_URL}/police/records")
check("Fetch Police Records (GET 200)", status == 200, records)

if status == 200 and isinstance(records, list) and len(records) > 0:
    target_tenant = records[0]
    t_id = target_tenant.get('id')
    print(f"Targeting Tenant ID {t_id} for tests")
    
    # 2. Update Record (Data Entry)
    update_data = {
        "father_name": "Test Father",
        "permanent_address": "123 Test Street",
        "police_station": "Central Station"
    }
    status, update_res = make_request(f"{BASE_URL}/police/records/{t_id}", method='PUT', data=update_data, is_json=True)
    check("Update Data Entry (PUT 200)", status == 200, update_res)
    
    # Verify Update
    status, verify_records = make_request(f"{BASE_URL}/police/records")
    target_verify = next((r for r in verify_records if r.get('id') == t_id), {})
    check("Data Entry Persisted", target_verify.get('father_name') == "Test Father", details="Father Name mismatch")
    
    # 3. Test Form Upload (Multipart Form Simulation)
    import io
    import uuid
    boundary = uuid.uuid4().hex
    body = io.BytesIO()
    
    # add file
    body.write(f"--{boundary}\r\n".encode('utf-8'))
    body.write(b"Content-Disposition: form-data; name=\"file\"; filename=\"test.pdf\"\r\n")
    body.write(b"Content-Type: application/pdf\r\n\r\n")
    body.write(b"%PDF-1.4 mock pdf content\r\n")
    body.write(f"--{boundary}--\r\n".encode('utf-8'))
    
    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': str(len(body.getvalue()))
    }
    
    status, upload_res = make_request(f"{BASE_URL}/police/upload/{t_id}", method='POST', data=body.getvalue(), headers=headers)
    check("Upload Signed Form (POST 201)", status == 201, upload_res)
    
    doc_id = None
    if status == 201 and isinstance(upload_res, dict):
        doc_id = upload_res.get('document_id')
        check("Upload returns Document ID", doc_id is not None)
        
        # Verify status automatically changed to Submitted
        status, check_status = make_request(f"{BASE_URL}/police/records")
        updated_tenant = next((r for r in check_status if r.get('id') == t_id), {})
        check("Status Auto-updated to Submitted", updated_tenant.get('police_status') == 'Submitted', updated_tenant.get('police_status'))
        check("Document URL Appended", updated_tenant.get('document_url') is not None, updated_tenant.get('document_url'))
        
        # 4. Test Form Delete
        if doc_id:
            status, del_res = make_request(f"{BASE_URL}/police/upload/{doc_id}", method='DELETE')
            check("Delete Uploaded Form (DELETE 200)", status == 200, del_res)
            
            # Verify status reverted to Pending
            status, check_status_revert = make_request(f"{BASE_URL}/police/records")
            revert_tenant = next((r for r in check_status_revert if r.get('id') == t_id), {})
            check("Status Reverted to Pending", revert_tenant.get('police_status') == 'Pending', revert_tenant.get('police_status'))

else:
    print("Cannot run deep tests - list is empty or API failed.")

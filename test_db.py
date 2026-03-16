from backend.app import create_app

app = create_app()
with app.test_client() as client:
    response = client.post('/api/rooms', json={
        "number": "101",
        "floor": 1,
        "type": "Small",
        "capacity": 2,
        "base_rent": 10000
    })
    print("STATUS:", response.status_code)
    try:
        print("JSON:", response.get_json())
    except:
        print("TEXT:", response.data.decode('utf-8'))

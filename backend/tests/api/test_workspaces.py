def test_create_workspace(client):
    response = client.post(
        "/api/v1/workspaces/",
        json={"name": "Test Workspace", "plan": "free"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Workspace"
    assert "id" in data

def test_get_workspaces(client):
    # Setup
    client.post("/api/v1/workspaces/", json={"name": "Test 1"})
    client.post("/api/v1/workspaces/", json={"name": "Test 2"})
    
    # Test
    response = client.get("/api/v1/workspaces/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert "Test 1" in [w["name"] for w in data]

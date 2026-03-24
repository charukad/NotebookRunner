import pytest

def test_create_project(client):
    # Need a workspace first
    ws_response = client.post("/api/v1/workspaces/", json={"name": "Parent WS"})
    ws_id = ws_response.json()["id"]
    
    response = client.post(
        "/api/v1/projects/",
        json={"name": "My AI Project", "workspace_id": ws_id}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My AI Project"
    assert data["workspace_id"] == ws_id
    assert "id" in data

def test_get_project_not_found(client):
    response = client.get("/api/v1/projects/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404

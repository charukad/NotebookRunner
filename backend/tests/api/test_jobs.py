def test_create_job(client):
    ws_response = client.post("/api/v1/workspaces/", json={"name": "WS 1", "plan": "pro"})
    ws_id = ws_response.json()["id"]
    
    proj_response = client.post("/api/v1/projects/", json={"name": "Proj 1", "workspace_id": ws_id})
    proj_id = proj_response.json()["id"]
    
    response = client.post(
        "/api/v1/jobs/",
        json={
            "project_id": proj_id,
            "notebook_version_id": "123e4567-e89b-12d3-a456-426614174000",
            "execution_backend": "colab",
            "requested_gpu": True
        }
    )

    assert response.status_code == 201
    assert response.json()["status"] == "queued"
    assert response.json()["requested_gpu"] is True

def test_get_job_not_found(client):
    response = client.get("/api/v1/jobs/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404

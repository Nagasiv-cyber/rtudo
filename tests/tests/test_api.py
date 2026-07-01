def test_health_check(client):
    """Test the health module."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy" 

def test_create_user(client):
    """Test user creation."""
    payload = {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "securepassword123"
    }
    response = client.post("/api/v1/users/", json=payload) 
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_duplicate_user(client):
    """Test that the Service Layer blocks duplicate emails."""
    payload = {
        "full_name": "Test User 2",
        "email": "test@example.com", # Same email as above
        "password": "password123"
    }
    # This should hit the global exception handler we built in Task 9
    response = client.post("/api/v1/users/", json=payload)
    
    assert response.status_code == 400
    assert response.json()["success"] is False
    assert "already exists" in response.json()["message"].lower()

def test_create_todo_validation_failure(client):
    """Test that Pydantic blocks bad requests (Missing title)."""
    payload = {
        "description": "I forgot my title",
        "user_id": "123e4567-e89b-12d3-a456-426614174000"
    }
    response = client.post("/api/v1/todos/", json=payload)
    
    assert response.status_code == 422
    assert response.json()["success"] is False
    assert response.json()["message"] == "Validation Error"
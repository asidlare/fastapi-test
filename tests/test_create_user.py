def test_create_user_happy_path(client):
    def check_response(response):
        assert response.json()["email"] == "test1@example.com"
        assert response.json()["first_name"] == "John"
        assert response.json()["last_name"] == "Doe"
        assert response.json()["date_of_birth"] == "2000-01-01"

    response = client.get("/v1/users/get-by-id/1")
    assert response.status_code == 404
    assert response.json() == {"message": "User not found"}

    response = client.post(
        "/v1/users/create",
        json={
            "email": "test1@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "2000-01-01"
        },
    )
    assert response.status_code == 201
    check_response(response)

    user_id = response.json()["user_id"]
    email = response.json()["email"]

    # get user by user_id
    response = client.get(f"/v1/users/get-by-id/{user_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id
    check_response(response)

    # get user by email
    response = client.get(f"/v1/users/get-by-email/{email}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id
    check_response(response)

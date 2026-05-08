from fastapi.testclient import TestClient

from app.main import app


# Create test client
client = TestClient(app)


def test_health_check():
    """
    Test root health endpoint.
    """

    response = client.get("/")

    # Validate status code
    assert response.status_code == 200

    # Validate response payload
    assert response.json()["status"] == "success"


def test_invalid_file_upload():
    """
    Ensure non-CSV uploads fail.
    """

    response = client.post(
        "/analyse",
        files={
            "file": (
                "sample.txt",
                b"invalid data",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
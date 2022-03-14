from pkg.main import app

def test_searching_faces_get():
    response = app.test_client().get("/search_faces/")
    assert response.status_code == 200
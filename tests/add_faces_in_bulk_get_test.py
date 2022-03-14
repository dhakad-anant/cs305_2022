from pkg.main import app

def test_add_faces_in_bulk_get():
    response = app.test_client().get("/add_faces_in_bulk/")
    assert response.status_code == 200
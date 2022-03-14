from pkg.main import app

def test_inserting_single_face_get():
    response = app.test_client().get("/add_face/")
    assert response.status_code == 200
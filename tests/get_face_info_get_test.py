from pkg.main import app

def test_searching_faces_get():
    response = app.test_client().get("/get_face_info/")
    assert response.status_code == 200
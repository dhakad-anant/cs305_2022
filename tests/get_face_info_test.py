from pkg.main import app

def test_get_face_info():

    data = {
        "image_id": 1
    }

    response = app.test_client().post("/get_face_info/", data=(data))
    
    assert response.status_code == 200
from pkg.main import app

def test_add_faces_in_bulk():

    file = open("tests/test_images/zip_for_test.zip", "rb")
    
    data = {
        "file": file
    }

    response = app.test_client().post("/add_faces_in_bulk/", data=(data))
    
    assert response.status_code == 200
from pkg.main import app

def test_inserting_single_face():

    file = open("tests/test_images/Ann_Veneman_0001.jpg", "rb")
    
    data = {
        "file": file
    }

    response = app.test_client().post("/add_face/", data=(data))
    assert response.status_code == 200
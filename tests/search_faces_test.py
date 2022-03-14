from pkg.main import app

def test_searching_faces():

    file = open("tests/test_images/Ann_Veneman_0001.jpg", "rb")
    
    data = {
        "file": file, 
        "k": 2,
        "confidence_level" : 0.5
    }

    response = app.test_client().post("/search_faces/", data=(data))
    
    assert response.status_code == 200
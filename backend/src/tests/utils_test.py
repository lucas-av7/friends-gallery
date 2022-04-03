from src.utils import response, random_file_name


def test_response():
    result, code = response("Created successfully", 200)
    assert result["status"] == "Success"
    assert result["message"] == "Created successfully"
    assert code == 200

    result, code = response("Error to create", 400, {"error": "Fields missing"})
    assert result["status"] == "Error"
    assert result["message"] == "Error to create"
    assert result["data"] == {"error": "Fields missing"}
    assert code == 400


def test_random_file_name():
    random_name = random_file_name(10, "py")

    assert len(random_name) == 13
    assert ".py" in random_name

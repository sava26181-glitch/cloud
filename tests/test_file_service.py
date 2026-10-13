from app.file_service import make_text_file, make_zip, safe_filename, read_upload

def test_safe_filename():
    assert safe_filename("../../hello.py") == "hello.py"

def test_text_file():
    name, data = make_text_file("hello.txt", "Привет")
    assert name == "hello.txt"
    assert data.decode("utf-8") == "Привет"

def test_zip():
    name, data = make_zip({"a.txt": "hello", "b.py": "print(1)"})
    assert name == "project.zip"
    assert data[:2] == b"PK"

def test_read_text():
    assert read_upload("x.txt", b"hello") == "hello"

from fastapi.testclient import TestClient
from app.main import app
import requests


client = TestClient(app)


host = "http://localhost:8000"
username = "admin"
password = "111"


response = requests.post(f"{host}/api/v1/user/login", json={"username": username, "password": password})
if response.status_code == 200:
    data = response.json()
    print(data["access_token"])


token = data["access_token"]
headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}


def test_category_get():
    response = client.get("/api/v1/category/", headers=headers)
    assert response.status_code == 200
    assert "category" in response.json()

def test_category_post():
    response = client.post("/api/v1/category/", headers=headers,  json={
        "title": "Aaa", 
        "index": 0, 
        "type":  0,
    })
    assert response.status_code == 200
    assert response.json() == {"message": "category added"}

def test_category_put():
    response = client.put("/api/v1/category/", headers=headers, json={
        "id":    1, 
        "title": "Aaa2", 
        "index": 0, 
        "type":  0,
    })
    assert response.status_code == 200
    assert response.json() == {"message": "category updated"}


###


def test_blog_get():
    response = client.get("/api/v1/blog/", headers=headers)
    assert response.status_code == 200
    assert "blog" in response.json()

def test_blog_post():
    response = client.post("/api/v1/blog/", headers=headers, json={
        "title": "Aaa", 
        "index": 0, 
        "cid":   1,
    })
    assert response.status_code == 200
    assert response.json() == {"message": "blog added"}

def test_blog_put():
    response = client.put("/api/v1/blog/", headers=headers, json={
        "id":    1, 
        "title": "Aaa2", 
        "index": 0, 
        "cid":   1,
    })
    assert response.status_code == 200
    assert response.json() == {"message": "blog updated"}


###


def test_content_get():
    response = client.get("/api/v1/content/1", headers=headers)
    assert response.status_code == 200
    assert "content" in response.json()

def test_content_post():
    response = client.post("/api/v1/content/", headers=headers, json={
        "title": "Aaaaaa", 
        "index": 0, 
        "bid":   1,
    })
    assert response.status_code == 200
    assert response.json() == {"message": "content added"}

def test_content_put():
    response = client.put("/api/v1/content/", headers=headers, json={
        "id":    1, 
        "title": "Aaaaaa2", 
        "index": 0, 
        "bid":   1,
    })
    assert response.status_code == 200
    assert response.json() == {"message": "content updated"}


###


def test_category_delete():
    response = client.delete("/api/v1/category/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "category deleted"}

def test_blog_delete():
    response = client.delete("/api/v1/blog/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "blog deleted"}

def test_content_delete():
    response = client.delete("/api/v1/content/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "content deleted"}
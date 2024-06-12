import requests
import pytest
import json
from time import sleep

class TestE2E:
    def make_new_user(self, username, password):
        register_data = {
            "username": username,
            "password": password
        }

        #Регистрация
        reg_response = requests.post("http://localhost:5005/register", json=register_data)

        assert reg_response.status_code in [200, 409]

        login_data = {
            "grant_type": "",
            "username": username,
            "password": password,
            "client_id": "",
            "client_secret": ""
        }

        #Login
        log_response = requests.post("http://localhost:5005/login", data=login_data)

        token = log_response.json()["access_token"]

        assert type(token) == str

        header = {
            "Authorization": "Bearer " + token
        }

        return header

    def test_posts(self):
        username = "test_user"
        password = "test_password"

        header = self.make_new_user(username, password)

        post_data = {
            "title": "test_post",
            "body": "test_post"
        }

        #попытка запроса без авторизации
        post_response_not_header = requests.post("http://localhost:5005/posts/new", json=post_data)

        assert post_response_not_header.status_code == 401

        #создание поста
        post_response = requests.post("http://localhost:5005/posts/new", json=post_data, headers=header)

        assert post_response.status_code == 201

        post_id = post_response.json()["message"].split('=')[1].strip()

        #просмотр поста
        get_post_response = requests.get(f"http://localhost:5005/posts/{post_id}", headers=header)

        assert get_post_response.status_code == 200

        post = get_post_response.json()["body"]

        assert post == post_data["body"]

        update_post_data = {
            "title": "update",
            "body": "update"
        }

        #обновление поста
        update_post_response = requests.put(f"http://localhost:5005/posts/{post_id}", headers=header, json=update_post_data)

        assert update_post_response.status_code == 200

        get_post_response = requests.get(f"http://localhost:5005/posts/{post_id}", headers=header)

        post = get_post_response.json()["title"]

        assert post == update_post_data["title"]

        data_to_all_posts = {
            "page_size": 5,
            "page_number": 1
        }

        # Получение всех постов
        get_all_post_response = requests.post(f"http://localhost:5005/posts/{username}", headers=header, json=data_to_all_posts)

        assert get_all_post_response.status_code == 200

        assert len(list(get_all_post_response.json()[1])) == 1

        # Удаление поста
        delete_post_response = requests.delete(f"http://localhost:5005/posts/{post_id}", headers=header)

        assert delete_post_response.status_code == 204

        get_all_post_response = requests.post(f"http://localhost:5005/posts/{username}", headers=header, json=data_to_all_posts)

        assert get_all_post_response.status_code == 200

        assert len(list(get_all_post_response.json())[1]) == 0


    def test_statistic(self):
        username = "test_user_2"
        password = "test_password_2"

        header = self.make_new_user(username, password)

        post_data = {
            "title": "test_post",
            "body": "test_post"
        }

        post_response = requests.post("http://localhost:5005/posts/new", json=post_data, headers=header)

        assert post_response.status_code == 201

        post_id = post_response.json()["message"].split('=')[1].strip()

        # Лайк, Просмотр

        like_response = requests.post(f"http://localhost:5005/action/like/{post_id}", headers=header)
        view_response = requests.post(f"http://localhost:5005/action/view/{post_id}", headers=header)

        statistic_response = requests.get(f"http://localhost:5005/action/statistic/post/{post_id}", headers=header)

        sleep(2)

        like, view = statistic_response.json()["likes"], statistic_response.json()["views"]

        assert int(like) == 1
        assert int(view) == 1

        # Топ пользователей

        top_users_response = requests.get(f"http://localhost:5005/action/statistic/top_users", headers=header)

        assert top_users_response.status_code == 200

        assert top_users_response.json()[0]["username"] == username

        # Топ постов

        top_posts_response = requests.get(f"http://localhost:5005/action/statistic/top_posts/{view}", headers=header)

        assert top_posts_response.status_code == 200

import requests
import json
import os
import random
from dotenv import load_dotenv
from pprint import pprint

def get_random_comics_number():

    response = requests.get("https://xkcd.com/info.0.json")
    response.raise_for_status()
    max_num = response.json()["num"]

    return random.randint(1, max_num)


def get_random_comics():

    random_num = get_random_comics_number()
    response = requests.get(f"https://xkcd.com/{random_num}/info.0.json")
    response.raise_for_status()
    comics = response.json()
    img_link = comics['img']
    comments = comics['alt']

    download_image(img_link)

    return comments


def download_image(img_link):

    response = requests.get(img_link)
    response.raise_for_status()

    with open("comics_image.png", "wb") as file:
        file.write(response.content)


def get_uri(url, client_id):

    params = {
            "client_id": client_id,
            "display": "page",
            "scope": "photos,groups,wall,offline",
            "response_type": "token",
            "revoke": "1",
    }
    response = requests.get(url, params)


def get_groups(access_token):

    url = "https://api.vk.com/method/groups.get/"
    params = {
            "access_token": access_token,
            "v": "5.131",
            "extended": "1"
    }
    response = requests.get(url, params)
    groups = response.json()["response"]["items"]


def get_upload_url(access_token, group_id):

    url = "https://api.vk.com/method/photos.getWallUploadServer/"
    params = {
            "group_id": group_id,
            "access_token": access_token,
            "v": "5.131"
    }

    response = requests.get(url, params)
    upload_url = response.json()["response"]["upload_url"]

    return upload_url


def upload_comics(access_token, group_id):

    with open("comics_image.png", "rb") as file:

        upload_url = get_upload_url(access_token, group_id)

        params = {
            "group_id": group_id,
            "access_token": access_token,
            "v": "5.131"
        }

        files = {
                "file1": file
        }

        response = requests.post(upload_url, params=params, files=files)
        response.raise_for_status()
        information = response.json()

    return information


def get_photo_id(access_token, group_id):

    url = "https://api.vk.com/method/photos.saveWallPhoto"
    information = upload_comics(access_token, group_id)

    params = {
            "group_id": group_id,
            "access_token": access_token,
            "v": "5.131",
            "photo": information['photo'],
            "server": information['server'],
            "hash": information['hash']
    }

    response = requests.post(url, params)
    photo = response.json()["response"]
    photo_id = photo[0]["id"]
    owner_id = photo[0]["owner_id"]

    return photo_id, owner_id


def upload_on_wall_comics(access_token, group_id):

    comments = get_comics_information()
    photo_id, owner_id = get_photo_id(access_token, group_id)
    url = "https://api.vk.com/method/wall.post"

    params = {
        "owner_id": f"-{group_id}",
        "access_token": access_token,
        "v": "5.131",
        "from_group": 1,
        "message": comments,
        "attachments": f"photo{owner_id}_{photo_id}"
    }

    response = requests.post(url, params)
    response.raise_for_status()

    os.remove("comics_image.png")


if __name__ == '__main__':
    load_dotenv()

    url = "https://oauth.vk.com/authorize"
    client_id = os.getenv("CLIENT_ID")
    access_token = os.getenv("ACCESS_TOKEN")
    group_id = os.getenv("GROUP_ID")
    owner_id = os.getenv("OWNER_ID")

    upload_on_wall_comics(access_token, group_id)

import requests
import json
import os
import random
from dotenv import load_dotenv


def check_status(response_details):
    if "error" in response_details:
        raise requests.exceptions.HTTPError(response_details['error'])


def get_random_comics_number():

    response = requests.get("https://xkcd.com/info.0.json")
    response.raise_for_status()
    max_num = response.json()["num"]

    return random.randint(1, max_num)


def get_random_comics(random_num):

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


def get_upload_url(access_token, group_id):

    url = "https://api.vk.com/method/photos.getWallUploadServer/"
    params = {
            "group_id": group_id,
            "access_token": access_token,
            "v": "5.131"
    }

    response = requests.get(url, params)
    response_details = response.json()
    response.raise_for_status()
    check_status(response_details)

    return response_details["response"]["upload_url"]


def upload_comics(access_token, group_id, upload_url):

    with open("comics_image.png", "rb") as file:

        params = {
            "group_id": group_id,
            "access_token": access_token,
            "v": "5.131"
        }

        files = {
                "file1": file
        }

        response = requests.post(upload_url, params=params, files=files)
        response_details = response.json()
        response.raise_for_status()
        check_status(response_details)

    return response_details


def get_ids(access_token, group_id, information):

    url = "https://api.vk.com/method/photos.saveWallPhoto"

    params = {
            "group_id": group_id,
            "access_token": access_token,
            "v": "5.131",
            "photo": information['photo'],
            "server": information['server'],
            "hash": information['hash']
    }

    response = requests.post(url, params)
    response_details = response.json()
    response.raise_for_status()
    check_status(response_details)
    
    photo = response_details["response"]
    photo_id = photo[0]["id"]
    owner_id = photo[0]["owner_id"]

    return photo_id, owner_id


def upload_on_wall_comics(access_token, group_id, comments, photo_id, owner_id):

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
    response_details = response.json()
    response.raise_for_status()
    check_status(response_details)


def main():
    load_dotenv()

    access_token = os.getenv("ACCESS_TOKEN")
    group_id = os.getenv("GROUP_ID")

    try:
        random_num = get_random_comics_number()
        comments = get_random_comics(random_num)
        upload_url = get_upload_url(access_token, group_id)
        information = upload_comics(access_token, group_id, upload_url)
        photo_id, owner_id = get_ids(access_token, group_id, information)

        upload_on_wall_comics(access_token, group_id, comments, photo_id, owner_id)
    finally:
        os.remove("comics_image.png")

if __name__ == '__main__':
    main()

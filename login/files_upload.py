import os
import shutil
import time

import dropbox


def empty_folder(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f"Deleted file: {item_path}")
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Deleted folder: {item_path}")


def test_dropbox_connection(access_token):
    try:
        dbx = dropbox.Dropbox(access_token)
        account_info = dbx.users_get_current_account()
        print("Connected to Dropbox as:", account_info.name.display_name)
        return dbx
    except dropbox.exceptions.AuthError as e:
        print("Error: Could not authenticate with Dropbox.")
        return None


def upload_folder_recursive(dbx, local_folder_path, dropbox_folder_path):
    for item in os.listdir(local_folder_path):
        item_path = os.path.join(local_folder_path, item)
        dropbox_item_path = os.path.join(dropbox_folder_path, item).replace("\\", "/")

        if os.path.isfile(item_path):
            with open(item_path, 'rb') as f:
                try:
                    dbx.files_upload(f.read(), dropbox_item_path)
                    print(f"Uploaded file: {item_path} -> {dropbox_item_path}")
                except dropbox.exceptions.ApiError as e:
                    print(f"Error uploading file {item_path}: {e}")
        elif os.path.isdir(item_path):
            try:
                dbx.files_create_folder_v2(dropbox_item_path)
                print(f"Created folder: {dropbox_item_path}")
                upload_folder_recursive(dbx, item_path, dropbox_item_path)
            except dropbox.exceptions.ApiError as e:
                print(f"Error creating folder {dropbox_item_path}: {e}")


def main():
    access_token = 'sl.BmDiGeavIOSQFn4jSCKrCPFl_vqXwW1rJK2Wv3Gvl-kqi5gUXtYCUOvhvUYYIv7CMuXN5U0LItttL68FCroLqAzqOnMF5lTNKgypLMuou_Kn-yLIO8eByFzSxLxQAb7Ge2aj6wdElTQb'
    # access_token = 'sl.Bk_hAGk47spbNBkS0iQ9CslBzk1XagIfbmKBjj0UJIcq8-4cbSuoBU164wA2OyUAJerQICMkOnyQcmxXWvZGl9djnU9fHiN65tCilerEPYh36rJy6o_jWfMnJNmIIil0QtenQFFMszVG'

    dbx = dropbox.Dropbox(
        app_key='o0ap9piuyzohkr1',
        app_secret='zhkru28citogbep',
        oauth2_refresh_token='SFlCTKKvCCsAAAAAAAAAAX1fkxdhmEdvD-Ptw0eCJiQLhTE4IuJcPhbiOWuNjsLI'
    )

    # dbx = dropbox.Dropbox(
    #     app_key= < APP_KEY >,
    # app_secret = < APP_SECRET >,
    # oauth2_refresh_token = < REFRESH_TOKEN >
    # )

    # dbx = test_dropbox_connection(access_token)
    if dbx:
        local_folder_path = 'upload_files'
        dropbox_folder_path = '/T6 Projects/Jobs 2023'
        upload_folder_recursive(dbx, local_folder_path, dropbox_folder_path)
    else:
        print("Connection to Dropbox failed.")

    if os.path.exists('upload_files'):
        folder_to_empty = 'upload_files'
        empty_folder(folder_to_empty)



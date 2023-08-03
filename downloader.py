


import instaloader
import re
import os
import threading



url = "<reels_link>"



def extract_username_and_media_code_from_url(url):
    pattern = r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/reels\/([a-zA-Z0-9_-]+)\/"
    match = re.match(pattern, url)
    if match:
        media_code = match.group(1)
        username = "instagram"  # Since the URL does not contain the username, use "instagram" as a default
        return username, media_code
    else:
        raise ValueError("Invalid Instagram Reel URL")

#222222222222222
#    if starts with /p/
#    pattern = r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/p\/([a-zA-Z0-9_-]+)\/"
#    match = re.match(pattern, url)
#    if match:
#        media_code = match.group(1)
#        username = "instagram"  # Since the URL does not contain the username, use "instagram" as a default
#        return username, media_code
#    else:
#        raise ValueError("Invalid Instagram Reel URL")


def download_reel():
    username, media_code = extract_username_and_media_code_from_url(url)
    def download_thread():
        loader = instaloader.Instaloader()
        try:
            post = instaloader.Post.from_shortcode(loader.context, media_code)
            loader.download_post(post, target=f"{username}_reels")
            delete_files(f"{username}_reels")
        except instaloader.exceptions.InstaloaderException:
            print("instaloader.exceptions.InstaloaderException")
    thread = threading.Thread(target=download_thread)
    thread.start()       

def delete_files(folder_path):
    extensions_to_delete = ['.txt', '.zip', '.jpg', '.jpeg', '.png', '.xz']
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension in extensions_to_delete:
                os.remove(file_path)
                print(f"Deleted: {file_path}")



download_reel()



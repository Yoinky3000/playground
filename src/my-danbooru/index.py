# image_paths = ["G:\My Drive\Stash\Fanbox\Deyui\August_2024\Aqua_On_Bed_August_2024_Microbikini.png"
            #    , "G:\\My Drive\\Stash\\Fanbox\\narukahana\\1PaTphM8SmkSXg3rpIiLaWkO.png"
            #    ]  # Ensure this path is correct


# upload

import requests

url = "http://localhost:3000/uploads.json?api_key=&login="
# api_key = ""
image_path = ""

# Prepare the files and data
# files = [
#     ("upload[source]", "https://google.com"),
#     ("upload[files][0]", open(image_path, 'rb')),
#     # ("upload[files][1]", open("another_image.jpg", 'rb')),  # Add more files as needed
# ]

files = {'upload[files][0]': open(image_path, 'rb')}
data = {
    'source': "aaaaaa",
}

# Make the POST request
response = requests.post(url, data=data, files=files)

# Check the response
if response.status_code == 200:
    print("Upload successful:", response.json())
else:
    print("Error:", response.status_code, response.text)


# auto tagger

# import requests

# # Define the URL and the image path
# url = "http://localhost:5000/evaluate"

# # Prepare the files and data
# files = [("file", open(image_path, 'rb')) for image_path in image_paths]
# data = {'format': 'json'}

# # Send the POST request
# response = requests.post(url, files=files, data=data)

# # Check the response
# if response.status_code == 200:
#     print("Response:", response.json())
# else:
#     print("Error:", response.status_code, response.text)

# wd tagger

# # # Define the URL and parameters
# import requests

# # Define the URL and parameters
# url = "http://127.0.0.1:5010/upload"
# params = {
#     'general_threshold': 0.35,
#     'character_threshold': 0.85
# }

# # Specify the image path

# image_path = ""  # Adjust this path as needed

# # Prepare the files for the request
# files = {
#     'file': (image_path, open(image_path, 'rb'), 'image/png')
# }

# # Send the POST request
# response = requests.post(url, params=params, headers={'accept': 'application/json'}, files=files)

# # Check the response
# if response.status_code == 200:
#     print("Response:", response.json())
# else:
#     print("Error:", response.status_code, response.text)

# # Close the file handle
# files['file'][1].close()


# import requests

# # Define the URL for creating a post
# url = "https://danbooru.donmai.us/posts.json"

# # Replace with your actual API key
# api_key = "YOUR_API_KEY"  # Use a valid API key

# # Prepare the data for the post
# data = {
#     'upload_media_asset_id': 'YOUR_MEDIA_ASSET_ID',  # Mandatory parameter
#     'tag_string': 'example_tag',  # Optional tags
#     'rating': 's',  # Optional rating: 'g', 's', 'q', 'e'
#     'parent_id': None,  # Optional parent post ID
#     'source': 'http://example.com',  # Optional source URL
#     'artist_commentary_title': 'Artist Commentary Title',  # Optional title
#     'artist_commentary_desc': 'Description of the commentary',  # Optional description
# }

# # Prepare the headers
# headers = {
#     'Authorization': f'Bearer {api_key}',
#     'Accept': 'application/json',
# }

# # Send the POST request
# response = requests.post(url, headers=headers, json=data)

# # Check the response
# if response.status_code == 201:  # Created
#     print("Post created successfully:", response.json())
# else:
#     print("Error creating post:", response.status_code, response.text)
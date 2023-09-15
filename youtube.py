import os
import google.oauth2.credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

__author__ = "Caleb Smith"
__credits__ = ["Caleb Smith"]
__version__ = "1.0"
__maintainer__ = "Caleb Smith"
__email__ = "me@calebmsmith.com"
__status__ = "Development"

# load .env
load_dotenv()


def authenticate_youtube():
    """
    Authenticates with the YouTube API using Service Account credentials.

    :return: None
    """
    # define the API credentials (Service Account)
    api_credentials_file = os.getenv('YOUTUBE_CREDENTIALS')

    # scopes
    scopes = ['https://www.googleapis.com/auth/youtube.upload']

    # load API credentials
    credentials = service_account.Credentials.from_service_account_file(api_credentials_file, scopes=scopes)

    # build the YouTube API client
    youtube = build('youtube', 'v3', credentials=credentials)

    return youtube


def upload_video(video_file_path, title, description, category_id):
    """
    Uploads a video to YouTube.

    :param video_file_path: Path to the video file to be uploaded.
    :param title: Title of the video.
    :param description: Description of the video.
    :param category_id: YouTube category ID for the video.
    :return: None
    """
    youtube = authenticate_youtube()

    try:
        # define the video properties
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': 'public'  # set the video privacy status (public, unlisted, or private)
            }
        }

        # upload the video file
        media_file = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part='snippet,status', body=body, media_body=media_file)
        response = None

        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f'Uploaded {int(status.progress() * 100)}%')

        print('Video uploaded successfully!')
        print(f'Video ID: {response["id"]}')

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
    except Exception as e:
        print(f'An error occurred: {str(e)}')


# video_file_path = 'path_to_your_video.mp4'  # Specify the path to your video file
# video_title = 'My Uploaded Video'  # Set the video title
# video_description = 'This is a test video uploaded using the YouTube Data API'  # Set the video description
# video_category_id = '22'  # Specify the YouTube category ID (e.g., '22' for Entertainment)
#
# upload_video(video_file_path, video_title, video_description, video_category_id)
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo


def upload(file: str, title: str, description: str, tags: list, category: str, status: str, thumbnail=None):
    # logon to the channel
    channel = Channel()
    channel.login("data_archive/client_secrets.json", "credentials.storage")

    # set up the video that is going to be uploaded
    video = LocalVideo(file_path=file)

    # create snippet
    video.set_title(title)
    video.set_description(description)
    video.set_tags(tags)
    video.set_category(category)
    video.set_default_language("en-US")

    # set status
    video.set_embeddable(True)
    video.set_license("creativeCommon")
    video.set_privacy_status(status)
    video.set_public_stats_viewable(True)

    # set thumbnail
    # video.set_thumbnail_path(thumbnail)

    # upload video and printing the results
    video = channel.upload_video(video)

    # like the video
    video.like()

    # return video id
    return video.id

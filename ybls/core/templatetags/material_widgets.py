import json
import logging
import re

import requests
from django import template

register = template.Library()

VIMEO_VIDEO_SOURCES_RE = '"progressive":\[(.*?)\]'
DESIRED_QUALITY = '540p'


@register.inclusion_tag('core/vimeo_widget.html')
def vimeo_widget(vimeo_link):
    video_id = vimeo_link.split('/')[-1]
    vimeo_url = f'https://player.vimeo.com/video/{video_id}'

    session = requests.Session()
    session.headers.update({'referer': 'https://new.iblschool.ru/'})
    response = session.get(vimeo_url)

    source_data = re.search(VIMEO_VIDEO_SOURCES_RE, response.text)
    matched = source_data.group(1)
    if not matched:
        logging.warning(f'Unable to detect sources for vimeo link: {vimeo_link}')
        return {}
    sources = json.loads(f'[{matched}]')
    source = next(source for source in sources if source['quality'] == DESIRED_QUALITY)

    return {
        'width': source['width'],
        'height': source['height'],
        'url': source['url'],
        'mime': source['mime'],
    }


@register.inclusion_tag('core/audio_widget.html')
def audio_widget(audio_file_data):
    return {
        'url': audio_file_data['fileUrl'],
        'mime': audio_file_data['mime'],
    }


@register.inclusion_tag('core/youtube_widget.html')
def youtube_widget(youtube_link):
    video_id = youtube_link.split('/')[-1]
    if not video_id:
        return {}
    return {'youtube_id': video_id}
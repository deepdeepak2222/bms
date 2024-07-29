"""
Utils
"""
from django.conf import settings
import logging

import requests

logger = logging.Logger(__name__)


def get_summary_from_external_endpoint(content):
    """
    Get summary of a content using transformers.pipeline package
    It is hosted on a separate microservice
    LLAMA is a huge model. Was facing issue while running locally.

    :param content:
    :return:
    """
    summary_server = settings.SUMMARY_SERVICE
    if not summary_server:
        logger.error("SUMMARY_SERVICE is not defined.")
        return content
    summary_ep = f"{summary_server}/book/summary"
    resp = requests.post(summary_ep, json={"content": content})
    ret_resp = content
    if resp.ok:
        ret_resp = resp.json().get("summary")
    return ret_resp

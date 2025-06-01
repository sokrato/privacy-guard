import os

import pytest


@pytest.mark.skip
def test_api():
    import requests
    from dotenv import load_dotenv

    load_dotenv()  # take environment variables from .env.
    # https://pastebin.com/doc_api
    url = "https://pastebin.com/api/api_post.php"
    resp = requests.post(
        url,
        data={
            "api_dev_key": os.environ["PASTEBIN_API_KEY"],
            "api_paste_code": "just some random text you :)",
            "api_option": "paste",
            # "api_paste_private": '0',
            # "api_paste_name": 'justmyfilename.php',
            "api_paste_expire_date": "10M",
        },
    )
    resp.raise_for_status()
    assert resp.text.startswith("https://pastebin.com/")
    assert len(resp.text) == 29

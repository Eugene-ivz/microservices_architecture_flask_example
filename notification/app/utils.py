import json


def file_ready(msg) -> str:
    """
    add here any functional to do with id of the text file
    like a emal notification
    
    currently just prints text_id to console

    """
    try:
        msg = json.loads(msg)
        text_id = msg["text_id"]
        print("ALL GOOD", f"{text_id =}")
    except Exception as e:
        e.add_note("can't get text_id from message")
        return e

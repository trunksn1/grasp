"""First API, local access only"""
import json

import hug # type: ignore
import hug.types as T # type: ignore

from kython.org import append_org_entry

from config import CAPTURE_PATH

def empty(s) -> bool:
    return s is None or len(s.strip()) == 0

def log(*things):
    # TODO proper logging
    print(*things)

# TODO allow to pass tags??
@hug.local()
@hug.post('/capture')
def capture(
        url: T.text,
        title: T.Nullable(T.text),
        selection: T.Nullable(T.text),
        comment: T.Nullable(T.text),
):
    log("capturing", url, title, selection, comment)

    heading = url
    parts = []

    if not empty(title):
        heading = title
        parts.append(url)

    # TODO not sure, maybe add as org quote?
    if not empty(selection):
        parts.extend([
            'Selection:',
            selection, # TODO tabulate?
        ])
    if not empty(comment):
        parts.extend([
            'Comment:',
            comment
        ])
    body = None if len(parts) == 0 else '\n'.join(parts)


    response = {
        'file': str(CAPTURE_PATH),
    }
    try:
        append_org_entry(
            CAPTURE_PATH,
            heading=heading,
            body=body,
            tags=['grasp'],
            todo=False,
        )
        response.update({
            'status': 'ok',
        })
    except Exception as e:
        log(str(e))
        response.update({
            'status': 'error',
            'error' : str(e),
        })

    return json.dumps(response).encode('utf8')

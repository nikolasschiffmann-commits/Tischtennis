def get_meetings(url):

    html = requests.get(url).text

    match = re.search(
        r'window\.__remixContext\s*=\s*({.*?});',
        html,
        re.DOTALL
    )

    if not match:
        raise Exception(
            f"__remixContext nicht gefunden: {url}"
        )

    data = json.loads(match.group(1))

    meetings = None

    def find_meetings(obj):
        nonlocal meetings

        if meetings:
            return

        if isinstance(obj, dict):
            for key, value in obj.items():

                if key == "meetings":
                    meetings = value
                    return

                find_meetings(value)

        elif isinstance(obj, list):
            for item in obj:
                find_meetings(item)

    find_meetings(data)

    return meetings

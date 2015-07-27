import json


def parse():
    """parse the json.

    1) convert `map` to `list`.
    2) fix url error.
    """
    with open('data.json', 'r') as f:
        companies = json.loads(f.read())['companies']
        for com in companies:
            com['job_types'] = [k for (k, v) in com['job_types'].items() if v]
            com['degrees'] = [k for (k, v) in com['degrees'].items() if v]
            com['authorizations'] = [k for (k, v) in com['authorizations'].items() if v]
            if com['website'].startswith("http://http://")\
                    or com['website'].startswith("http://https://"):
                com['website'] = com['website'][7:]

    with open('another.json', 'w') as f:
        f.write(json.dumps(companies))


if __name__ == '__main__':
    parse()

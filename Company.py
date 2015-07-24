import json


class Company(object):

    def __init__(self, id):
        self.id = id
        self.name = None
        self.url = None
        self.website = None
        self.industry = None
        self.overview = None
        self.days = []
        self.degrees = {'bachelor': False, 'master': False, 'phd': False}
        self.job_types = {'full-time': False, 'part-time': False, 'internship': False, 'co-op': False}
        self.job_titles = []
        self.authorizations = {
            'citizen': False,
            'f-1': False,
            'j-1': False,
            'citizen/perm': False,
            'h1-b': False,
            'tn': False
        }

    def to_json(self):
        return json.dumps(self.__dict__)


if __name__ == '__main__':
    c = Company(1)
    print c.to_json()

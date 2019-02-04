

class GitHostConnection:

    def __init__(self, api_data):
        self.host = api_data['host']
        self.username = api_data['username']


class WeevilUser:

    def __init__(self, api_data):
        self.id = api_data['uuid']
        self.connections = [GitHostConnection(conn) for conn in api_data['connected_to']]


class Repository:

    def __init__(self, api_data):
        self.repository_id = api_data['uuid']
        self.host = api_data['repo_host']
        self.owner = api_data['owner']['username']
        self.name = api_data['name']
        self.private = api_data['private']
        self.checked = api_data['checked']



class ApiModel:

    properties = ()

    def __init__(self, api_data):
        self._api_data = api_data.copy()
        for prop in self.properties:
            setattr(self, prop, self._api_data[prop])

    def as_dict(self):
        return {prop: getattr(self, prop) for prop in self.properties }


class GitHostConnection(ApiModel):
    properties = ('host', 'username')


class WeevilUser(ApiModel):
    properties = ('uuid',)

    def __init__(self, api_data):
        super().__init__(api_data)
        self.connections = [GitHostConnection(conn) for conn in api_data['connected_to']]

    def as_dict(self):
        data = super().as_dict()
        data['connections'] = [conn.as_dict() for conn in self.connections]
        return data


class Repository(ApiModel):
    properties = ('uuid', 'name', 'private', 'fork', 'checked')

    def __init__(self, api_data):
        super().__init__(api_data)
        self.owner = api_data['owner']['username']
        self.host = api_data['repo_host']

    def as_dict(self):
        data = super().as_dict()
        data['owner'] = self.owner
        data['host'] = self.host
        return data


class Check(ApiModel):
    properties = ('uuid', 'number', 'status', 'previous_number', 'previous_id', 'next_number')

import uuid


class URIGen:

    @staticmethod
    def uri_gen():
        uri = str(uuid.uuid4()).split("-")[0]
        return uri

"""
hubspot owners api
"""
from hubspot3.base import (
    BaseClient
)


OWNERS_API_VERSION = 'v2'


class OwnersClient(BaseClient):
    """allows access to the owners api"""
    def _get_path(self, subpath):
        return 'owners/{}/owners'.format(OWNERS_API_VERSION)

    def get_owners(self, **options):
        """*Only* returns the list of owners, does not include additional metadata"""
        return self._call('owners', **options)

    def get_owner_name_by_id(self, owner_id, **options):
        """given an id of an owner, return their name"""
        owner_name = 'value_missing'
        owners = self.get_owners()
        for owner in owners:
            if int(owner['ownerId']) == int(owner_id):
                owner_name = '{} {}'.format(owner['firstName'], owner['lastName'])
        return owner_name

    def get_owner_email_by_id(self, owner_id, **options):
        """given an id of an owner, return their email"""
        owner_email = 'value_missing'
        owners = self.get_owners()
        for owner in owners:
            if int(owner['ownerId']) == int(owner_id):
                owner_email = owner['email']
        return owner_email

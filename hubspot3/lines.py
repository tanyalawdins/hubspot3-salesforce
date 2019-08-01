"""
hubspot products api
"""
from hubspot3.associations import AssociationsClient
from hubspot3.base import BaseClient
from hubspot3.utils import get_log


LINES_API_VERSION = "1"


class LinesClient(BaseClient):

    def __init__(self, *args, **kwargs):
        super(LinesClient, self).__init__(*args, **kwargs)
        self.log = get_log("hubspot3.lines")

    def create(self, data=None, **options):
        return self._call(
            '',
            data=data,
            method='POST',
            **options,
        )

    def get(self, line_id, **options):
        """Retrieve a line by its id."""
        return self._call('{}'.format(line_id), **options)

    def link_line_item_to_deal(self, line_item_id, deal_id):
        """Link a line item to a deal."""
        associations_client = AssociationsClient(**self.credentials)
        return associations_client.link_line_item_to_deal(line_item_id, deal_id)

    def _get_path(self, subpath: str):
        return "crm-objects/v{}/objects/line_items/{}".format(
            self.options.get("version") or LINES_API_VERSION, subpath
        )

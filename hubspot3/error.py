"""
hubspot3 error helpers
"""
from hubspot3.utils import force_utf8


class EmptyResult(object):
    """
    Null Object pattern to prevent Null reference errors
    when there is no result
    """

    def __init__(self):
        self.status = 0
        self.body = ""
        self.msg = ""
        self.reason = ""

    def __bool__(self):
        return False


class HubspotError(ValueError):
    """Any problems get thrown as HubspotError exceptions with the relevant info inside"""

    as_str_template = """
---- request ----
{method} {host}{url}, [timeout={timeout}]

---- body ----
{body}

---- headers ----
{headers}

---- result ----
{result_status}

---- body -----
{result_body}

---- headers -----
{result_headers}

---- reason ----
{result_reason}

---- trigger error ----
{error}
        """

    def __contains__(self, item):
        """tests if the given item text is in the error text"""
        return item in self.__str__()

    def __bool__(self):
        return False

    def __init__(self, result, request, err=None):
        super(HubspotError, self).__init__(result and result.reason or "Unknown Reason")
        if result is None:
            self.result = EmptyResult()
        else:
            self.result = result
        if request is None:
            request = {}
        self.request = request
        self.err = err

    def __str__(self):
        return force_utf8(self.__unicode__())

    def __unicode__(self):
        params = {}
        request_keys = ("method", "host", "url", "data", "headers", "timeout", "body")
        result_attrs = ("status", "reason", "msg", "body", "headers")
        params["error"] = self.err
        for key in request_keys:
            params[key] = self.request.get(key)
        for attr in result_attrs:
            params["result_{}".format(attr)] = getattr(self.result, attr, "")

        params = self._dict_vals_to_unicode(params)
        return self.as_str_template.format(**params)

    def _dict_vals_to_unicode(self, data):
        unicode_data = {}
        for key, val in list(data.items()):
            if not val:
                unicode_data[key] = ""
            if isinstance(val, bytes):
                unicode_data[key] = force_utf8(val)
            elif isinstance(val, str):
                unicode_data[key] = force_utf8(val)
            else:
                unicode_data[key] = force_utf8(type(val))
        return unicode_data


# Create more specific error cases, to make filtering errors easier
class HubspotBadRequest(HubspotError):
    """Error wrapper for most 40X results and 501 results"""


class HubspotNotFound(HubspotError):
    """Error wrapper for 404 and 410 results"""


class HubspotTimeout(HubspotError):
    """Wrapper for socket timeouts, sslerror, and 504"""


class HubspotUnauthorized(HubspotError):
    """Wrapper for 401 Unauthorized errors"""


class HubspotServerError(HubspotError):
    """Wrapper for most 500 errors"""

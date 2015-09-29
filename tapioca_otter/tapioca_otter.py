# coding: utf-8

from tapioca import (
    TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin)
from urlparse import (
    urlsplit, parse_qs)
from urllib import urlencode

from resource_mapping import RESOURCE_MAPPING


class OtterClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'http://otter.topsy.com/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(OtterClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        if 'params' in params:
            params['params'].update({'apikey': api_params.get('apikey')})
        else:
            params['params'] = {'apikey': api_params.get('apikey')}

        return params

    def get_iterator_list(self, response_data):
        return response_data['response']['list']

    def get_iterator_next_request_kwargs(self,
            iterator_request_kwargs, response_data, response):
        if 'list' not in response_data['response'] or not response_data['response']['list']:
            return

        page = str(response_data['response']['page'] + 1)
        parsed = urlsplit(response.url)
        query = parse_qs(parsed.query)
        query['page'][0] = page
        next_page_url = parsed._replace(query=urlencode(query, True)).geturl()

        if next_page_url:
            return {'url': next_page_url}


Otter = generate_wrapper_from_adapter(OtterClientAdapter)

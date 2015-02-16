__author__ = 'cage'

import endpoints


WEB_CLIENT_ID = ''

rest_db_api = endpoints.api(name='restDB',
                            version='v1',
                            description='restdb',
                            allowed_client_ids=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
                            scopes=[endpoints.EMAIL_SCOPE])
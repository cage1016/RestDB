__author__ = 'cage'

import endpoints
from protorpc import messages


class ReturnJSON(messages.Message):
  msg = messages.StringField(1)


class RestDBCreateUpdateRequest(messages.Message):
  pk_column = messages.StringField(1)
  file = messages.StringField(2)


class RestDBQeuryRequest(messages.Message):
  key_name = messages.StringField(1)
  value = messages.StringField(2)


class RestDBGQLRequest(messages.Message):
  gql = messages.StringField(1)


RESTDB_GET_RESOURCE = endpoints.ResourceContainer(
  dataset=messages.StringField(1, required=True),
  table=messages.StringField(2, required=True),
  key_name=messages.StringField(3, required=True)
)

RESTDB_LIST_RESOURCE = endpoints.ResourceContainer(
  dataset=messages.StringField(1, required=True),
  table=messages.StringField(2, required=True)
)

RESTDB_QUERY_RESOURCE = endpoints.ResourceContainer(
  RestDBQeuryRequest,
  dataset=messages.StringField(2, required=True),
  table=messages.StringField(3, required=True),
  type=messages.StringField(4, required=True)
)

RESTDB_INSERT_OR_UPDATE_RESOURCE = endpoints.ResourceContainer(
  RestDBCreateUpdateRequest,
  dataset=messages.StringField(2, required=True),
  table=messages.StringField(3, required=True)
)

RESTDB_GQL_RESOURCE = endpoints.ResourceContainer(
  RestDBGQLRequest,
  dataset=messages.StringField(2, required=True),
  table=messages.StringField(3, required=True)
)

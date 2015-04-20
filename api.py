__author__ = 'cage'

import json

from protorpc import remote
from protorpc import message_types
from api_messages import *

from settings import rest_db_api
from google.appengine.ext import ndb
from google.appengine.ext.db import Error

from datastore_utils import datastore_utils


datastroe_util = datastore_utils()


@rest_db_api.api_class(resource_name='restdb')
class RestDBApi(remote.Service):
  """
  DynamicModels - https://code.djangoproject.com/wiki/DynamicModels

  Dynamic create Model Class

  class Person(models.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

  is functionlly equivalent to

  Person = type('Person', (models.Model,), {
    'first_name': ndb.StringProperty(),
    'last_name': ndb.StringProperty(),
  })

  """

  def render_response(self, result):

    if type(result) == list:
      resp = [o.to_dict() for o in result]
    else:
      resp = result.to_dict()

    return ReturnJSON(msg=json.dumps(resp))


  @endpoints.method(RESTDB_INSERT_OR_UPDATE_RESOURCE,
                    message_types.VoidMessage,
                    name='insert_or_update',
                    http_method='POST',
                    path='restdb/{dataset}/{table}')
  def insert_or_update(self, request):
    pk_column = request.pk_column
    files = json.loads(request.file)

    for index, file in enumerate(files):

      data = {}
      for key, value in file.items():
        data[key] = value

      datastroe_util.insert_datastroe(request.dataset,
                                      request.table,
                                      pk_column,
                                      index,
                                      data)

    return message_types.VoidMessage()


  @endpoints.method(RESTDB_GET_RESOURCE,
                    ReturnJSON,
                    name='get',
                    http_method='GET',
                    path='restdb/{dataset}/{table}/{key_name}')
  def get(self, request):

    try:
      result = datastroe_util.get_datastore_by_id(request.dataset,
                                                  request.table,
                                                  request.key_name)

      return self.render_response(result)

    except Error, error:
      return ReturnJSON(msg=json.dumps({'error': error.message}))


  @endpoints.method(RESTDB_LIST_RESOURCE,
                    ReturnJSON,
                    name='list',
                    http_method='GET',
                    path='restdb/{dataset}/{table}')
  def list(self, request):

    try:
      result = datastroe_util.list_datastore(request.dataset,
                                             request.table)

      return self.render_response(result)

    except Error, error:
      return ReturnJSON(msg=json.dumps({'error': error.message}))


  @endpoints.method(RESTDB_GET_RESOURCE,
                    ReturnJSON,
                    name='delete',
                    http_method='DELETE',
                    path='restdb/{dataset}/{table}/{key_name}')
  def delete(self, request):

    try:
      datastroe_util.delete_datastore_by_id(request.dataset,
                                            request.table,
                                            request.key_name)

      return ReturnJSON(msg=json.dumps({'status': 'done'}))

    except Error, error:
      return ReturnJSON(msg=json.dumps({'error': error.message}))


  @endpoints.method(RESTDB_QUERY_RESOURCE,
                    ReturnJSON,
                    name='query',
                    http_method='GET',
                    path='restdb/{dataset}/{table}/query/{type}')
  def query(self, request):

    try:
      result = datastroe_util.get_datastore_by_query(request.dataset,
                                            request.table,
                                            request.type,
                                            request.key_name,
                                            request.value)

      return self.render_response(result)

    except Error, error:
      return ReturnJSON(msg=json.dumps({'error': error.message}))


  @endpoints.method(RESTDB_GQL_RESOURCE,
                    ReturnJSON,
                    name='gql',
                    http_method='GET',
                    path='restdb/{dataset}/{table}/gql')
  def gql(self, request):

    try:
      result = datastroe_util.get_datastore_by_gql(request.dataset,
                                                   request.table,
                                                   request.gql)

      return self.render_response(result)

    except Error, error:
      return ReturnJSON(msg=json.dumps({'error': error.message}))
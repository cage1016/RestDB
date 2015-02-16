__author__ = 'cage'

import re
import logging

from google.appengine.ext import ndb
from google.appengine.ext.ndb import gql, FilterNode


class datastore_utils(object):
  def model(self, name, parent=None):
    dynamic_model = type(name.encode('utf-8'), (ndb.Expando,), {})

    if parent:
      return dynamic_model(parent=parent)
    else:
      return dynamic_model()


  def get_kind(self, dataset, table):
    return '%s_%s' % (dataset, table)


  def get_datastore_by_id(self, dataset, table, pk):
    return self.get_datastore(self.get_kind(dataset, table), pk=pk)


  def get_datastore_by_query(self, dataset, table, type, key_name, value):

    opsymbol = {
      'eq': '=',
      'gt': '>',
      'lt': '<'
    }

    filters = FilterNode(key_name, opsymbol[type], value)

    return self.get_datastore(self.get_kind(dataset, table), filters=filters)


  def get_datastore_by_gql(self, dataset, table, gql_string):

    # dynamic build kind model

    kind = self.get_kind(dataset, table)
    model = self.model(kind)

    logging.info('gql_string = %s' % gql_string)

    return gql(gql_string).fetch()


  def get_datastore(self, kind, pk=None, filters=None):

    # dynamic build kind model
    model = self.model(kind)

    if pk:
      query = ndb.Query(kind=kind, ancestor=ndb.Key('pk', pk))

    else:

      if not filters:
        query = ndb.Query(kind=kind)

      else:
        query = ndb.Query(kind=kind, filters=filters)

    return query.fetch()


  def list_datastore(self, dataset, table):
    return self.get_datastore(self.get_kind(dataset, table))


  def insert_datastroe(self, dataset, table, pk_name, i, data):

    if pk_name and data.has_key(pk_name):  # pkColumn
      row_id = str(data.get(pk_name))
      logging.info('Using RowId = ' + row_id)

      model = self.model(self.get_kind(dataset, table), ndb.Key('pk', row_id))
    elif pk_name and not pk_name:  # insert id
      pk_name = pk_name + ('-' + i) if i != -1 else ''
      logging.info('Using PkName = ' + pk_name)

      model = self.model(self.get_kind(dataset, table), ndb.Key('pk', pk_name))
    else:
      logging.Info('Autogenerate Id')
      model = self.model(self.get_kind(dataset, table))

    model.populate(**data)
    model.put()


  def delete_datastore_by_id(self, dataset, table, pk):
    self.delete_datastore(self.get_kind(dataset, table), pk)


  def delete_datastore(self, kind, pk=None):

    # dynamic build kind model
    model = self.model(kind)

    qo = ndb.QueryOptions(keys_only=True)
    if pk:
      query = ndb.Query(kind=kind, ancestor=ndb.Key('pk', pk), default_options=qo)

    else:
      query = ndb.Query(kind=kind, default_options=qo)

    if query:
      ndb.delete_multi(query.fetch())


RestDB - python version
==============

###Local API explorer


```sh
localhost:8080/_ah/api/explorer
```


###Insert or Update Data

- route: `/_ah/api/restDB/v1/restdb/{dataset}/{table}`
    - dataset: The data group name
    - table:
- method: __POST__
- body: json string includes following columns
    - pk_column: The column id of the document that must inside file column
        - type: string
    - file: The upload records that must have at least one column that config in pkColumn
        - type: JSON string
    
Request example
```sh
curl -sS -H 'Content-Type:application/json' -X POST http://localhost:8080/_ah/api/restDB/v1/restdb/mitac/user \
  -d '{ "pk_column": "id", "file": "[{\"id\":123,\"user\":\"simonsu\"},{\"id\":223,\"user\":\"jelly223\"}]"}'
```

###Get Data

- route: `/_ah/api/restDB/v1/restdb/{dataset}/{table}/{key_name}`
    - dataset: The data group name
    - table: The interactive table
    - key_name: The column
- method: __GET__

Reqeust Example
```sh
curl http://localhost:8080/_ah/api/restDB/v1/restdb/mitac/user/123 | json
```
###List Data

- route: `/_ah/api/restDB/v1/restdb/{dataset}/{table}`
    - dataset: The data group name
    - table: The interactive table
    - key_name: The column name
- method: __GET__

Request Example
```sh
curl http://localhost:8080/_ah/api/restDB/v1/restdb/mitac/user | json
```

### Get Data By Query

- route: `/_ah/api/restDB/v1/restdb/{dataset}/{table}/query/{type}`
    - dataset: The data group name
    - table: The interactive table
    - type: eq, gt, lt
    - body
        - key_name: the column name
        - value: column value
- method: __GET__

Request Example
```sh
curl -L -G -d "key_name=user&value=jelly223" http://localhost:8080/_ah/api/restDB/v1/restdb/mitac/user/query/eq | json
```

###Get Data By Gql

-  route:`/_ah/api/restDB/v1/restdb/{dataset}/{table}/gql`
    - dataset: The data group name
    - table The interactive table
    - method: __GET__

Request Example
```sh
curl http://localhost:8080/_ah/api/restDB/v1/restdb/mitac/user/gql?gql=select%20*%20from%20mitac_user
```

###Delete Data

- route: `/_ah/api/restDB/v1/restdb/{dataset}/{table}/{key_name}`
    - dataset: The data group name
    - table: The interactive table
    - key_name: the column name
- method: __DELETE__

Request Example
```sh
curl -sS -X DELETE http://localhost:8080/_ah/api/restDB/v1/restdb/mitac/user/123
```
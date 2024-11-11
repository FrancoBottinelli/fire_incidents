## Fire incidents challenge
This app servers fire incidents data retrieved from a selected data source. 
Data is stored in a PostgreSQL database

Both resources are Dockerized for compatibility and instantiation purposes

### How do I build resources locally?
First of all, Docker is required for the app to be able to deploy locally. 
Visit https://docs.docker.com/engine/install/ for install instructions

Once Docker is up and running, with root directory on this application, execute the following command
``` docker-compose up --build ```

This command should instanciate a _PostgreSQL database_ and a _Python app with a Flask server_

### How do I retrieve the data?
The first step is to trigger the data retirieval process in the Python application

For this action we will send a command to the Docker container to run a pre-built script that
will execute data retrieval actions for all configured data sources

``` docker exec -it python_app bash commands/retrieve_data.sh ```

Logs should show you the progress of the script

### How do I start querying the data?
The Python app is already running a Flask server that has an open endpoint for managed data query

The endpoint path is ``` http://localhost:5000/fire_incidents/aggregate ```

In this endpoint, you should send a POST request with a RAW JSON Payload with the following parameters

``` keys ``` -> Key columns the data should be grouped by. Expressed in a List object

``` aggregate ``` -> Aggregate columns the response should return. Expressed in a Dict object, 
keys being the aggregator and values being a list of the requested columns for the aggregator

``` filter_by ``` (optional) -> Filter conditions. Expressed in a List[Dict] object.
Each Dict should specify ```column, operator and value```

``` order_by ``` (optional) -> Order criteria for the response. Expressed in a Dict object,
keys being the column and values being the sort style

### Example payload
```
{
    "keys": ["incident_date"],
	"aggregate": {"count": ["id"], "sum": ["fire_fatalities", "fire_injuries"]},
	"filter_by": [
		{"column": "battalion", "operator": "IN", "value": ["B06", "B07"]},
		{"column": "city", "operator": "=", "value": "San Francisco"}
	],
	"order_by": {"incident_date": "ASC"}
}
```

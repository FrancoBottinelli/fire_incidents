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

Dataset columns are also specified in this endpoint!

``` http://localhost:5000/fire_incidents/table ```

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

### Findings and thought process
Navigating through the website of the dataset, I found two viable options for data retrieval,
through CSV or API. I've found the API path to be more suitable for the exercise, though CSV downloads
might be faster for larger amounts of data

I've found the data preety standarized and well layed out in general, so I gave a low priority to data
transformation and validation. Nevertheless, these concepts are a must in a production environment, so I
designed for added features in my code layout, having the flexibility for each data model to have its own
transformations and validations upon instantiation

A choice I made with data structure was to clean some of the columns of the dataset, I saw lots of 
columns that rarely had any relevant data, so my choice was to group all these details into a 
'incident_details' column, where columns that were not specified in the SQL model would be added to
this column if they had any relevant values, cleaning lots of empty registers in the process

For the reports, I opted for a managed Flask server where a potential B.I team could retrieve data
from the model through an API gateway and a set of limited attributes.
The choice here is tricky, it depends on the use case of the B.I team. This option allows for certain
flexibility in the team needs for data reports, but not unmanaged access (like opening an endpoint where they
could input a raw SQL query), or a more unflexible approach, opening a different gateway for each report that they
need. This is of course a group debate on what the team needs are, and a choice can be made depending on their
feedback. Having no such scenario, I opted for an all rounded soultion.

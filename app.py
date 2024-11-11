from flask import Flask, jsonify, request
from data_models.fire_incidents import FireIncidents

app = Flask(__name__)


@app.route('/fire_incidents/table', methods=['GET'])
def fire_incidents_table_columns():
	try:
		response = FireIncidents.get_table_columns()
	except Exception as error:
		response = str(error)
	
	return jsonify(data=response)


@app.route('/fire_incidents/aggregate', methods=['POST'])
def fire_incidents_aggregate_query():
	payload = request.json
	keys = payload.get('keys', [])
	aggregate = payload.get('aggregate', {})
	filter_by = payload.get('filter_by', [])
	order_by = payload.get('order_by', {})
	
	try:
		response = FireIncidents.execute_query(
			keys=keys,
			aggregate=aggregate,
			filter_by=filter_by,
			order_by=order_by,
		)
	except Exception as error:
		response = str(error)
	
	return jsonify(data=response)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)

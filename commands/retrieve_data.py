from constants import DATA_SOURCE_TO_MODEL_MAPPER
from logger import logger


def retrieve_data():
	for data_source_class, data_model in DATA_SOURCE_TO_MODEL_MAPPER.items():
		data_source_name = data_source_class.name()
		logger.info(f'Starting data retrieval from {data_source_name}')
		data_source = data_source_class()
		data_model.create_table()
		existing_rows = data_model.get_db_primary_key_values()
		try:
			for data_quote in data_source.yield_data():
				serialized_data_quote = []
				logger.info(f'Detected {len(data_quote)} registers from data source: {data_source_name}')
				for row in data_quote:
					row_instance = data_model.create_instance_from_dict(data=row)
					if row_instance.id not in existing_rows:
						existing_rows.add(row_instance.id)
						serialized_data_quote.append(row_instance)
				logger.info(f'Adding {len(serialized_data_quote)} registers to database: {data_source_name}')
				data_model.insert_data_into_table(data=serialized_data_quote)
		except Exception:
			raise

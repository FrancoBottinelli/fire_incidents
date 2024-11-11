import re
from typing import List, Dict, Set, Self, Any
from abc import abstractmethod
from db_manager import DBManager
import exceptions
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import text


@as_declarative()
class DataModel:
	__abstract__ = True
	
	@classmethod
	@declared_attr
	def __tablename__(cls):
		return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
	
	@classmethod
	def get_table_columns(cls) -> List:
		return [column.name for column in cls.__table__.columns]
	
	@classmethod
	@abstractmethod
	def create_instance_from_dict(cls, data: Dict) -> Self:
		""" Creation method. Defines how instances are created. Add validations and transformations here """
		...
	
	@classmethod
	def create_table(cls):
		connector = DBManager()
		cls.__table__.create(connector.engine, checkfirst=True)
		
	def to_dict(self, output_columns: List = None) -> Dict:
		output_columns = output_columns if output_columns else self.get_table_columns()
		return {field: value for field, value in self.__dict__.items() if field in output_columns}
		
	@classmethod
	def insert_data_into_table(cls, data: List[Self]):
		connector = DBManager()
		try:
			with connector.session as session:
				session.bulk_save_objects(data)
				session.commit()
		except Exception:
			raise
		
	@classmethod
	def get_db_primary_key_values(cls) -> Set:
		connector = DBManager()
		with connector.session as session:
			return set(pk[0] for pk in session.query(cls.id).all())
	
	@classmethod
	def execute_query(
		cls,
		keys: List,
		aggregate: Dict[str, List[str]],
		filter_by: List[Dict[str, Any]],
		order_by: Dict[str, str]
	) -> List:
		connector = DBManager()
		response = []
		if not keys:
			message = "Parameter required for query: 'keys'"
			raise exceptions.QueryParameterException(message)
		if not aggregate:
			message = "Parameter required for query: 'aggregate'"
			raise exceptions.QueryParameterException(message)
			
		try:
			aggregate_columns = []
			for aggregator, column_list in aggregate.items():
				for column in column_list:
					column_selector = f'{aggregator.upper()}({column}) AS {column}'
					aggregate_columns.append(column_selector)
			column_select = ', '.join(keys + aggregate_columns)
			
			filter_by_statement = ''
			if filter_by:
				filter_columns = []
				for filter_statement in filter_by:
					column = filter_statement['column']
					operator = filter_statement['operator']
					value = filter_statement['value']
					if isinstance(value, List):
						value_list = ', '.join(f"'{v}'" for v in value)
						value = f"({value_list})"
					else:
						value = f"'{value}'"
					
					filter_columns.append(f"{column} {operator} {value}")
				filter_by_statement = 'WHERE ' + ' AND '.join(filter_columns)
			
			order_by_statement = ''
			if order_by:
				order_columns = [f'{column} {order.upper()}' for column, order in order_by.items()]
				order_by_statement = 'ORDER BY ' + ', '.join(order_columns)
			
			query = f'''
				SELECT {column_select}
				FROM {cls.__tablename__}
				{filter_by_statement}
				GROUP BY {', '.join(keys)}
				{order_by_statement}
			'''
		except Exception as error:
			message = f'Query build encountered an unexpected error: {error}'
			raise exceptions.QueryBuildException(message)
		
		try:
			with connector.session as session:
				data = session.execute(text(query))
				columns = list(data.keys())
				for row in data:
					response.append({field: row[i] for i, field in enumerate(columns)})
			return response
		except Exception as error:
			message = f'Database encountered a query error: {error}'
			raise exceptions.DatabaseQueryException(message)

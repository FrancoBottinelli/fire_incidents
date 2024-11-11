import os
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker


class DBManager:
	_instance = None
	_engine = None
	
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance
	
	@staticmethod
	def get_database_engine() -> Engine:
		host = os.getenv('POSTGRES_HOST', 'localhost')
		database_name = os.getenv('POSTGRES_DB')
		user = os.getenv('POSTGRES_USER')
		password = os.getenv('POSTGRES_PASSWORD')
		uri = f'postgresql://{user}:{password}@{host}/{database_name}'
		return create_engine(uri)
	
	@property
	def engine(self) -> Engine:
		if not self._engine:
			self._engine = self.get_database_engine()
		return self._engine
	
	@property
	def session(self) -> Session:
		return sessionmaker(bind=self.engine)()

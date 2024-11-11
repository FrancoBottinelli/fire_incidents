from abc import ABC, abstractmethod
from typing import Dict, Generator


class DataSource(ABC):
	@abstractmethod
	def yield_data(self) -> Generator[Dict, None, None]: ...
	
	@classmethod
	def name(cls) -> str:
		return cls.__name__

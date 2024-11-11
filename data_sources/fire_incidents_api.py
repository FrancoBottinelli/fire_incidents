import requests
import exceptions
from data_sources.data_source import DataSource


class FireIncidentsAPI(DataSource):
	api_endpoint = 'https://data.sfgov.org/resource/wr8u-xric.json'
	row_limit = 50000
	
	def yield_data(self):
		i = 1
		while True:
			try:
				response = requests.get(
					self.api_endpoint,
					params={'$offset': i*self.row_limit, '$limit': self.row_limit}
				)
				response.raise_for_status()
				data = response.json()
				yield data
				if len(data) < self.row_limit:
					break
				i += 1
			except Exception as error:
				message = f'API communication encountered an unexpected error: {error}'
				raise exceptions.APIRequestException(message)

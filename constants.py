from typing import Dict, Type
from data_sources.data_source import DataSource
from data_sources.fire_incidents_api import FireIncidentsAPI
from data_models.data_model import DataModel
from data_models.fire_incidents import FireIncidents

DATA_SOURCE_TO_MODEL_MAPPER: Dict[Type[DataSource], Type[DataModel]] = {
	FireIncidentsAPI: FireIncidents,
}

from typing import Dict, Self
from sqlalchemy import Column, String, Integer, Date, DateTime, JSON
from data_models.data_model import DataModel


class FireIncidents(DataModel):
	id = Column(Integer, primary_key=True, nullable=False)
	incident_number = Column(Integer)
	exposure_number = Column(Integer)
	address = Column(String(200), nullable=True)
	incident_date = Column(Date)
	call_number = Column(Integer)
	alarm_dttm = Column(DateTime)
	arrival_dttm = Column(DateTime)
	close_dttm = Column(DateTime)
	data_as_of = Column(DateTime)
	data_loaded_at = Column(DateTime)
	city = Column(String(200), nullable=True)
	zipcode = Column(String(200), nullable=True)
	battalion = Column(String(200), nullable=True)
	station_area = Column(String(200), nullable=True)
	supervisor_district = Column(String(200), nullable=True)
	neighborhood_district = Column(String(200), nullable=True)
	box = Column(String(200), nullable=True)
	suppression_units = Column(Integer)
	suppression_personnel = Column(Integer)
	ems_units = Column(Integer)
	ems_personnel = Column(Integer)
	other_units = Column(Integer)
	other_personnel = Column(Integer)
	fire_fatalities = Column(Integer)
	fire_injuries = Column(Integer)
	civilian_fatalities = Column(Integer)
	civilian_injuries = Column(Integer)
	number_of_alarms = Column(Integer)
	incident_details = Column(JSON)
	
	@classmethod
	def create_instance_from_dict(cls, data: Dict) -> Self:
		table_columns = cls.get_table_columns()
		data_columns = list(data.keys())
		if 'incident_details' not in data.keys():
			data['incident_details'] = {}
		for field in data_columns:
			if field not in table_columns:
				value = data.pop(field)
				if value:
					data['incident_details'][field] = value
		data[FireIncidents.id.name] = int(data[FireIncidents.id.name])
		return cls(**data)

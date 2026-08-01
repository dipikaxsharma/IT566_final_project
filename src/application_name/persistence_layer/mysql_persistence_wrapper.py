"""Defines the MySQLPersistenceWrapper class."""

from application_name.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import (MySQLConnectionPool)
import inspect
import json

class MySQLPersistenceWrapper(ApplicationBase):
	"""Implements the MySQLPersistenceWrapper class."""

	def __init__(self, config:dict)->None:
		"""Initializes object. """
		self._config_dict = config
		self.META = config["meta"]
		self.DATABASE = config["database"]
		super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')

		# Database Configuration Constants
		self.DB_CONFIG = {}
		self.DB_CONFIG['database'] = \
			self.DATABASE["connection"]["config"]["database"]
		self.DB_CONFIG['user'] = self.DATABASE["connection"]["config"]["user"]
		self.DB_CONFIG['host'] = self.DATABASE["connection"]["config"]["host"]
		self.DB_CONFIG['port'] = self.DATABASE["connection"]["config"]["port"]
		self.DB_CONFIG['password'] = self.DATABASE["connection"]["config"]["password"]
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: DB Connection Config Dict: {self.DB_CONFIG}')

		# Database Connection
		self._connection_pool = \
			self._initialize_database_connection_pool(self.DB_CONFIG)
		

		# SQL String Constants





	# MySQLPersistenceWrapper Methods

	def get_all_campaigns(self)->list:
		"""Queries the campaign table and returns all rows as a list of dictionaries."""
		try:
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Fetching all campaigns...')
			connection = self._connection_pool.get_connection()
			cursor = connection.cursor(dictionary=True)
			cursor.execute('SELECT * FROM campaign;')
			rows = cursor.fetchall()
			cursor.close()
			connection.close()
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Retrieved {len(rows)} campaign(s).')
			return rows
		except connector.Error as err:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem fetching campaigns: {err}')
			return []
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem fetching campaigns: {e}')
			return []



	def get_all_channels(self)->list:
		"""Queries the channel table and returns all rows as a list of dictionaries."""
		try:
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Fetching all channels...')
			connection = self._connection_pool.get_connection()
			cursor = connection.cursor(dictionary=True)
			cursor.execute('SELECT * FROM channel;')
			rows = cursor.fetchall()
			cursor.close()
			connection.close()
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Retrieved {len(rows)} channel(s).')
			return rows
		except connector.Error as err:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem fetching channels: {err}')
			return []
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem fetching channels: {e}')
			return []

	def add_campaign(self, name:str, company:str, budget:float=0.0,
					status:str='active', start_date=None, end_date=None)->int:
		"""Inserts a new campaign row and returns the new campaign_id."""
		try:
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Adding campaign {name}...')
			connection = self._connection_pool.get_connection()
			cursor = connection.cursor()
			sql = ('INSERT INTO campaign (name, company, budget, status, start_date, end_date) '
				   'VALUES (%s, %s, %s, %s, %s, %s);')
			values = (name, company, budget, status, start_date, end_date)
			cursor.execute(sql, values)
			connection.commit()
			new_id = cursor.lastrowid
			cursor.close()
			connection.close()
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Added campaign_id {new_id}.')
			return new_id
		except connector.Error as err:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem adding campaign: {err}')
			return None
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem adding campaign: {e}')
			return None

	def add_channel(self, name:str, type:str='other', status:str='active')->int:
		"""Inserts a new channel row and returns the new channel_id."""
		try:
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Adding channel {name}...')
			connection = self._connection_pool.get_connection()
			cursor = connection.cursor()
			sql = 'INSERT INTO channel (name, type, status) VALUES (%s, %s, %s);'
			values = (name, type, status)
			cursor.execute(sql, values)
			connection.commit()
			new_id = cursor.lastrowid
			cursor.close()
			connection.close()
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Added channel_id {new_id}.')
			return new_id
		except connector.Error as err:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem adding channel: {err}')
			return None
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem adding channel: {e}')
			return None

	def link_channel_to_campaign(self, campaign_id:int, channel_id:int,
					spend:float=0.0, start_date=None)->int:
		"""Links a channel to a campaign via campaign_channel_xref, returns the new xref_id."""
		try:
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Linking campaign {campaign_id} to channel {channel_id}...')
			connection = self._connection_pool.get_connection()
			cursor = connection.cursor()
			sql = ('INSERT INTO campaign_channel_xref (campaign_id, channel_id, spend, start_date) '
				   'VALUES (%s, %s, %s, %s);')
			values = (campaign_id, channel_id, spend, start_date)
			cursor.execute(sql, values)
			connection.commit()
			new_id = cursor.lastrowid
			cursor.close()
			connection.close()
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Added xref_id {new_id}.')
			return new_id
		except connector.Error as err:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem linking channel to campaign: {err}')
			return None
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem linking channel to campaign: {e}')
			return None

	def update_campaign(self, campaign_id:int, name:str, company:str, budget:float,
					status:str, start_date=None, end_date=None)->bool:
		"""Updates an existing campaign row. Returns True on success."""
		try:
			connection = self._connection_pool.get_connection()
			cursor = connection.cursor()
			sql = ('UPDATE campaign SET name=%s, company=%s, budget=%s, status=%s, '
				   'start_date=%s, end_date=%s WHERE campaign_id=%s;')
			values = (name, company, budget, status, start_date, end_date, campaign_id)
			cursor.execute(sql, values)
			connection.commit()
			cursor.close()
			connection.close()
			return True
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')
			return False

	def delete_campaign(self, campaign_id:int)->bool:
		"""Deletes a campaign row. Returns True on success."""
		try:
			connection = self._connection_pool.get_connection()
			cursor = connection.cursor()
			cursor.execute('DELETE FROM campaign WHERE campaign_id=%s;', (campaign_id,))
			connection.commit()
			cursor.close()
			connection.close()
			return True
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')
			return False

	def update_channel(self, channel_id:int, name:str, type:str, status:str)->bool:
		"""Updates an existing channel row. Returns True on success."""
		try:
			connection = self._connection_pool.get_connection()
			cursor = connection.cursor()
			sql = 'UPDATE channel SET name=%s, type=%s, status=%s WHERE channel_id=%s;'
			cursor.execute(sql, (name, type, status, channel_id))
			connection.commit()
			cursor.close()
			connection.close()
			return True
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')
			return False

	def delete_channel(self, channel_id:int)->bool:
		"""Deletes a channel row. Returns True on success."""
		try:
			connection = self._connection_pool.get_connection()
			cursor = connection.cursor()
			cursor.execute('DELETE FROM channel WHERE channel_id=%s;', (channel_id,))
			connection.commit()
			cursor.close()
			connection.close()
			return True
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')
			return False

		##### Private Utility Methods #####

	def _initialize_database_connection_pool(self, config:dict)->MySQLConnectionPool:
		"""Initializes database connection pool."""
		try:
			self._logger.log_debug(f'Creating connection pool...')
			cnx_pool = \
				MySQLConnectionPool(pool_name = self.DATABASE["pool"]["name"],
					pool_size=self.DATABASE["pool"]["size"],
					pool_reset_session=self.DATABASE["pool"]["reset_session"],
					use_pure=self.DATABASE["pool"]["use_pure"],
					**config)
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Connection pool successfully created!')
			return cnx_pool
		except connector.Error as err:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem creating connection pool: {err}')
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Check DB cnfg:\n{json.dumps(self.DATABASE)}')
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:Problem creating connection pool: {e}')
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:Check DB conf:\n{json.dumps(self.DATABASE)}')

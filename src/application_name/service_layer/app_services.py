"""Implements AppServices Class."""

from application_name.application_base import ApplicationBase
from application_name.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
import inspect
from application_name.campaign import Campaign
from application_name.channel import Channel

class AppServices(ApplicationBase):
    """AppServices Class Definition."""
    def __init__(self, config:dict)->None:
        """Initializes object. """
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
        self.DB = MySQLPersistenceWrapper(config)
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')

    def get_campaigns(self)->list:
        """Retrieves all campaigns from the database as Campaign objects."""
        rows = self.DB.get_all_campaigns()
        campaigns = []
        for row in rows:
            c = Campaign(
                name=row['name'],
                company=row['company'],
                budget=float(row['budget']),
                status=row['status'],
                start_date=row['start_date'],
                end_date=row['end_date']
            )
            campaigns.append(c)
        return campaigns

    def get_channels(self)->list:
        """Retrieves all channels from the database as Channel objects."""
        rows = self.DB.get_all_channels()
        channels = []
        for row in rows:
            ch = Channel(
                name=row['name'],
                type=row['type'],
                status=row['status']
            )
            channels.append(ch)
        return channels

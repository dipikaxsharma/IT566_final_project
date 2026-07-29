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

    def create_campaign(self, name:str, company:str, budget:float=0.0,
                         status:str='active', start_date=None, end_date=None)->int:
        """Creates a new campaign in the database, returns the new campaign_id."""
        return self.DB.add_campaign(name, company, budget, status, start_date, end_date)

    def create_channel(self, name:str, type:str='other', status:str='active')->int:
        """Creates a new channel in the database, returns the new channel_id."""
        return self.DB.add_channel(name, type, status)

    def link_campaign_channel(self, campaign_id:int, channel_id:int,
                               spend:float=0.0, start_date=None)->int:
        """Links a channel to a campaign with an allocated spend, returns the new xref_id."""
        return self.DB.link_channel_to_campaign(campaign_id, channel_id, spend, start_date)

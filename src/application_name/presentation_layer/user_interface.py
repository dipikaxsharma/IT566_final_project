"""Implements the applicatin user interface."""

from application_name.application_base import ApplicationBase
from application_name.service_layer.app_services import AppServices
import inspect
import json
from datetime import date

class UserInterface(ApplicationBase):
    """UserInterface Class Definition."""
    def __init__(self, config:dict)->None:
        """Initializes object. """
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
        self.DB = AppServices(config)
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')




    def start(self):
        """Start main user interface."""
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User interface started!')
        while True:
            self.display_menu()
            self.process_menu_choice()

    def display_menu(self):
        """Display the main menu."""
        print('\n\t\tAd Campaigns and Channels\n')
        print('\t1. View Campaigns')
        print('\t2. Add Campaign')
        print('\t3. View Channels')
        print('\t4. Add Channel')
        print('\t5. Link Channel to Campaign')
        print('\t6. Update Campaign')
        print('\t7. Delete Campaign')
        print('\t8. Update Channel')
        print('\t9. Delete Channel')
        print('\t10. Exit')

    def process_menu_choice(self):
        """Read the user's menu choice and dispatch to the matching method."""
        user_input = input('\n\tEnter Command Number: ')
        if not user_input:
            print('\tNo input entered, try again.')
            return
        menu_choice = user_input.strip()
        match menu_choice:
            case '1':
                self.view_campaigns()
            case '2':
                self.add_campaign()
            case '3':
                self.view_channels()
            case '4':
                self.add_channel()
            case '5':
                self.link_channel_to_campaign()
            case '6':
                self.update_campaign_ui()
            case '7':
                self.delete_campaign_ui()
            case '8':
                self.update_channel_ui()
            case '9':
                self.delete_channel_ui()
            case '10':
                print('\n\tGoodbye!')
                exit()
            case _:
                print(f'\tInvalid choice: {menu_choice}. Try again.')

    def view_campaigns(self):
        """Display all campaigns."""
        campaigns = self.DB.get_campaigns()
        if not campaigns:
            print('\n\tNo campaigns found.')
            return
        print(f'\n\t--- Campaigns ({len(campaigns)}) ---')
        for c in campaigns:
            print(f'\t{c}')

    def add_campaign(self):
        """Prompt for and add a new campaign."""
        print('\n\t--- Add Campaign ---')
        name = input('\tCampaign name: ')
        company = input('\tCompany: ')
        try:
            budget = float(input('\tBudget: '))
        except Exception:
            print('\tInvalid budget entered, defaulting to 0.0.')
            budget = 0.0
        status = input('\tStatus (active/paused/ended) [active]: ') or 'active'
        start_date_str = input('\tStart date (YYYY-MM-DD), or leave blank: ')
        end_date_str = input('\tEnd date (YYYY-MM-DD), or leave blank: ')
        start_date = date.fromisoformat(start_date_str) if start_date_str else None
        end_date = date.fromisoformat(end_date_str) if end_date_str else None
        new_id = self.DB.create_campaign(name, company, budget, status, start_date, end_date)
        if new_id:
            print(f'\tCampaign added with campaign_id {new_id}.')
        else:
            print('\tSomething went wrong adding the campaign.')

    def view_channels(self):
        """Display all channels."""
        channels = self.DB.get_channels()
        if not channels:
            print('\n\tNo channels found.')
            return
        print(f'\n\t--- Channels ({len(channels)}) ---')
        for ch in channels:
            print(f'\t{ch}')

    def add_channel(self):
        """Prompt for and add a new channel."""
        print('\n\t--- Add Channel ---')
        name = input('\tChannel name: ')
        type = input('\tType (social/search/email/video) [other]: ') or 'other'
        status = input('\tStatus (active/inactive) [active]: ') or 'active'
        new_id = self.DB.create_channel(name, type, status)
        if new_id:
            print(f'\tChannel added with channel_id {new_id}.')
        else:
            print('\tSomething went wrong adding the channel.')

    def link_channel_to_campaign(self):
        """Link a channel to a campaign with a spend amount."""
        print('\n\t--- Link Channel to Campaign ---')
        rows = self.DB.get_campaign_summaries()
        if not rows:
            print('\tNo campaigns exist yet. Add a campaign first.')
            return
        print('\tAvailable campaigns:')
        for row in rows:
            print(f"\t  {row['campaign_id']}: {row['name']}")
        channel_rows = self.DB.get_channel_summaries()
        if not channel_rows:
            print('\tNo channels exist yet. Add a channel first.')
            return
        print('\tAvailable channels:')
        for row in channel_rows:
            print(f"\t  {row['channel_id']}: {row['name']}")
        try:
            campaign_id = int(input('\tCampaign ID: '))
            channel_id = int(input('\tChannel ID: '))
            spend = float(input('\tSpend allocated: '))
        except Exception:
            print('\tInvalid input entered, cancelling.')
            return
        start_date_str = input('\tStart date (YYYY-MM-DD), or leave blank: ')
        start_date = date.fromisoformat(start_date_str) if start_date_str else None
        new_id = self.DB.link_campaign_channel(campaign_id, channel_id, spend, start_date)
        if new_id:
            print(f'\tLinked successfully, xref_id {new_id}.')
        else:
            print('\tSomething went wrong linking the channel to the campaign.')

    def update_campaign_ui(self):
        """Prompt for and update an existing campaign."""
        for row in self.DB.get_campaign_summaries():
            print(f"\t  {row['campaign_id']}: {row['name']}")
        try:
            cid = int(input('\tCampaign ID to update: '))
            name = input('\tNew name: ')
            company = input('\tNew company: ')
            budget = float(input('\tNew budget: '))
            status = input('\tNew status: ')
        except Exception:
            print('\tInvalid input, cancelling.')
            return
        ok = self.DB.update_campaign(cid, name, company, budget, status)
        print('\tUpdated.' if ok else '\tSomething went wrong.')

    def delete_campaign_ui(self):
        """Prompt for and delete a campaign."""
        for row in self.DB.get_campaign_summaries():
            print(f"\t  {row['campaign_id']}: {row['name']}")
        try:
            cid = int(input('\tCampaign ID to delete: '))
        except Exception:
            print('\tInvalid input, cancelling.')
            return
        ok = self.DB.delete_campaign(cid)
        print('\tDeleted.' if ok else '\tSomething went wrong.')

    def update_channel_ui(self):
        """Prompt for and update an existing channel."""
        for row in self.DB.get_channel_summaries():
            print(f"\t  {row['channel_id']}: {row['name']}")
        try:
            chid = int(input('\tChannel ID to update: '))
            name = input('\tNew name: ')
            type = input('\tNew type: ')
            status = input('\tNew status: ')
        except Exception:
            print('\tInvalid input, cancelling.')
            return
        ok = self.DB.update_channel(chid, name, type, status)
        print('\tUpdated.' if ok else '\tSomething went wrong.')

    def delete_channel_ui(self):
        """Prompt for and delete a channel."""
        for row in self.DB.get_channel_summaries():
            print(f"\t  {row['channel_id']}: {row['name']}")
        try:
            chid = int(input('\tChannel ID to delete: '))
        except Exception:
            print('\tInvalid input, cancelling.')
            return
        ok = self.DB.delete_channel(chid)
        print('\tDeleted.' if ok else '\tSomething went wrong.')
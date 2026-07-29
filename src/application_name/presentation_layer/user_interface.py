"""Implements the applicatin user interface."""

from application_name.application_base import ApplicationBase
from application_name.service_layer.app_services import AppServices
import inspect
import json

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
        print('\t6. Exit')

    def process_menu_choice(self):
        """Read the user's menu choice and dispatch to the matching method."""
        user_input = input('\n\tEnter Command Number: ')
        if not user_input:
            print('\tNo input entered, try again.')
            return
        menu_choice = user_input[0]
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
        """Stub: will prompt for and add a new campaign."""
        print('add_campaign() called...')

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
        """Stub: will prompt for and add a new channel."""
        print('add_channel() called...')

    def link_channel_to_campaign(self):
        """Stub: will link a channel to a campaign with a spend amount."""
        print('link_channel_to_campaign() called...')

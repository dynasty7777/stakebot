from .promotion import setup as promotion_setup
from .demotion import setup as demotion_setup
from .dismissal import setup as dismissal_setup
from .curator_meetings import setup as curator_meetings_setup
from .hiring import setup as hiring_setup
from .restore import setup as restore_setup
from .dismissal_no_discord import setup as dismissal_no_discord_setup
from .hiring_no_discord import setup as hiring_no_discord_setup
from .reports import setup as report_setup
from .state_roles_message import setup as state_roles_message_setup

def setup_commands(bot):
    promotion_setup(bot)
    demotion_setup(bot)
    dismissal_setup(bot)
    curator_meetings_setup(bot)
    hiring_setup(bot)
    restore_setup(bot)
    dismissal_no_discord_setup(bot)
    hiring_no_discord_setup(bot)
    report_setup(bot)
    state_roles_message_setup(bot)
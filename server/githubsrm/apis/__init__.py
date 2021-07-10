from .models import Entry
from .checks_models import EntryCheck
from .utils import BotoService

service = BotoService()
open_entry = Entry()
open_entry_checks = EntryCheck()
"""Views for each MakenModel page"""

from makenmodel.views.index import show_index
from makenmodel.views.accounts import show_login
from makenmodel.views.accounts import show_create_account
from makenmodel.views.accounts import create_account
from makenmodel.views.accounts import logout
from makenmodel.views.accounts import login
from makenmodel.views.toolbox import show_toolbox
from makenmodel.views.toolbox import show_add_paints
from makenmodel.views.toolbox import show_your_paints
from makenmodel.views.api import get_brands
from makenmodel.views.toolbox import mark_getting_low
from makenmodel.views.toolbox import show_getting_low
from makenmodel.views.models import show_find_models
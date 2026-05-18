"""Tiferet Monday Version and Exports"""

# *** version
__version__ = '1.0.0b1'

# *** exports

# ** app
# Export the main application context and related modules.
# Use a try-except block to avoid import errors on build systems.
try:
    from .contexts.app import MondayApp
    from .contexts.board import BoardContext
    from .contexts.item import ItemContext
    from .contexts.user import UserContext
    from .repos.settings import MondayApiError
except ImportError:
    pass

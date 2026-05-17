"""Tiferet Monday Interfaces Settings"""

# *** imports

# ** core
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


# *** interfaces

# ** interface: monday_service
class MondayService(ABC):
    '''
    Base service interface for Monday.com API operations.
    All domain-specific services extend this contract.
    '''

    pass

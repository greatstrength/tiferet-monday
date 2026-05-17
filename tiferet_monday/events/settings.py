"""Tiferet Monday Events Settings"""

# *** imports

# ** core
from time import sleep
from typing import Any, Callable

# ** app
from ..assets import const


# *** events

# ** event: monday_event
class MondayEvent:
    '''
    Base class for Monday.com domain events.
    Provides complexity-budget retry handling for API rate limits.
    '''

    # * method: handle_with_retry
    @staticmethod
    def handle_with_retry(handler: Callable, max_retries: int = 3, **kwargs) -> Any:
        '''
        Execute a handler with automatic retry on complexity budget exhaustion.

        :param handler: The callable to execute.
        :type handler: Callable
        :param max_retries: Maximum number of retries.
        :type max_retries: int
        :param kwargs: Arguments to pass to the handler.
        :type kwargs: dict
        :return: The handler result.
        :rtype: Any
        '''

        # Track retry attempts.
        last_error = None

        for attempt in range(max_retries + 1):
            try:

                # Execute the handler.
                return handler(**kwargs)

            except Exception as e:

                # Check if this is a complexity budget error.
                error_code = getattr(e, 'error_code', None)
                if error_code != const.COMPLEXITY_BUDGET_EXHAUSTED_ID:
                    raise

                # Store the error for potential re-raise.
                last_error = e

                # Extract retry delay from error args.
                retry_seconds = 60
                if hasattr(e, 'args') and len(e.args) > 1:
                    try:
                        retry_seconds = int(e.args[1])
                    except (ValueError, TypeError):
                        pass

                # If we've exhausted retries, re-raise.
                if attempt >= max_retries:
                    raise

                # Wait and retry.
                sleep(retry_seconds)

        # Should not reach here, but raise last error if so.
        raise last_error

# *** configs

# ** config: errors
ERRORS = [
    dict(
        id='monday_api_error',
        name='Monday.com API Error',
        error_code='MONDAY_API_ERROR',
        description='An error occurred while interacting with the Monday.com API.',
        message=[
            dict(
                lang='en_US',
                text='A Monday.com API error occurred: {}',
            )
        ]
    )
]
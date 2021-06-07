class ResponseBuilder:
    def __call__(self, data=None, error=None, status_code=200):
        if (data is None) != (error is None):
            raise AssertionError("Response should be either data or an error.")
        if data:
            response = {
                'success': True,
                'data': data
            }
        else:
            message = [str(x) for x in error.args]
            status_code = error.status_code
            response = {
                'success': False,
                'error': {
                    'type': error.__class__.__name__,
                    'message': message
                }
            }
        return response, status_code

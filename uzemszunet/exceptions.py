
class DownloadError(Exception):

    def __init__(self, message, status_code=404, status_text=''):
        self.message = message
        self.status_code = status_code
        self.status_text = status_text

    def __str__(self):
        return 'DonwloadError: {0} {1}:{2}'.format(
            self.message,
            self.status_code,
            self.status_text
        )

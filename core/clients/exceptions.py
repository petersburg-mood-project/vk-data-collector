class VkApiException(Exception):
    def __init__(self, params: dict):
        super().__init__(f"{params['error_msg']}, error_code: {params['error_code']}")
        self.__dict__.update(params)

def error_handler(func):
    """ 
        Conceived as a global error handler
        It must send any code problem to me without stopping working
    """
    def wrapper():
        try:
            func()
        except Exception as e:
            print(e)
    return wrapper

def error_handler(func):
    """ 
        Conceived as a global error handler
        It must send any code problem to me without stopping working
    """

    def wrapper(self_arg):
        try:
            func(self_arg)
        except Exception as e:
            print("Error:", e)
    return wrapper

def incompleted(func):
    def wrapper(*args, **kwargs):
        print(f"This object \"{func}\" is incompleted. Using it may cause exceptions.")
        func(*args, **kwargs)

    return wrapper

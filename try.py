
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # 在原始函数执行前添加一些新的逻辑
        print("a")
        result = my_function(*args, **kwargs)
        print("b")
        # 在原始函数执行后添加一些新的逻辑
        return result
    return wrapper

@my_decorator
def my_function():
    print("Hello, decorator!")

my_function()
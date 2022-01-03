# 装饰器
from line_profiler import LineProfiler
from functools import wraps
import time

#查询接口中每行代码执行的时间
def func_line_time(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        func_return = f(*args, **kwargs)
        lp = LineProfiler()
        lp_wrap = lp(f)
        lp_wrap(*args, **kwargs) 
        lp.print_stats() 
        return func_return 
    return decorator 

def time_keep(func):
    
    def time_ke(*args, **kwargs):
        start_time = time.time()
        output = func(*args, **kwargs)
        end_time = time.time()
        print(f'{func.__name__}()耗时: {end_time-start_time}')
        return output
    return time_ke


if __name__ == "__main__":
    pass

import inspect
import logging
from functools import wraps


def logger(file, return_res=True, show_args=True):
    logging.basicConfig(filename=file, format='%(asctime)s :: %(levelname)s :: %(message)s', level=logging.DEBUG)

    def decorator(func, *args, **kwargs):
        import time
        @wraps(func)
        def wrapper(*args, **kwargs):
            parent_name = inspect.currentframe().f_back.f_code.co_name
            start = time.time()
            if show_args:
                logging.info(f'Function {func.__name__} started with arguments {args} and {kwargs} from {parent_name} ')
            else:
                logging.info(f'Function {func.__name__} started from {parent_name}')

            try:
                res = func(*args, **kwargs)
                finish = time.time()
                if return_res:
                    logging.info(f'Function {func.__name__} finished in {finish - start} sec with result {res}')
                else:
                    logging.info(f'Function {func.__name__} finished in {finish - start} sec')
            except Exception as exc:
                finish = time.time()
                logging.error(f'Function {func.__name__} crashed with Exception {exc} in {finish - start} sec')
                return ''


            return res

        return wrapper

    return decorator

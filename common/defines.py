class DataType():
    ''' Enums to identify data types '''
    IGNORE = 0
    NUMBER = 1
    SYMBOL = 2
    MIN_GOAL = 4
    MAX_GOAL = 8

def lst_join(arr):
    return ",".join([str(x) for x in arr])

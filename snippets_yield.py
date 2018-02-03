#code inspired from cpython tests
#https://github.com/python/cpython

def delegation_of_initial_next_to_subgenerator():
    """
    test delegation of initial next() call to subgenerator
    """

    trace = []
    def g1():
        trace.append("Starting g1")
        #yield g2()
        yield
        for y in g2():
            trace.append("Yielded {}".format(y))
        trace.append("Finishing g1")
    def g2():
        trace.append("Starting g2")
        yield 42
        trace.append("Finishing g2")
    for x in g1():
        trace.append("Yielded1 %s" % (x,))
    print trace
"""
    assertEqual(trace, [
        "Starting g1",
        "Starting g2",
        "Yielded 42",
        "Finishing g2",
        "Finishing g1",
    ])
"""

"""
yield is similar to return
yield turns an object into itrable. without yield
the for x in g1() statement will not work
the yield in g1 just returns control but no object
the yield in g2 returns the object with value 42
sequence of events: g1 starts to execute, "Starting g1"
is appended, yield return control and x gets None since
yield does not return any value with it, then g2 starts
to execute. "starting g2" is appended, yield returns
control and y gets 42 , "Finishing g2" gets appended 
and then "Finishing1 gets appended
"""

if __name__ == '__main__':
    delegation_of_initial_next_to_subgenerator()

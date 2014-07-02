

def dump_args(func):
    '''This decorator dumps (to STDOUT) the arguments passed to a function
    before calling the function itself.

    .. note::
       This decorator should not be used in production code and the logging
       module used instead.
    '''
    argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
    fname = func.func_name

    def echo_func(*args,**kw):
        spcr = "*" * 75
        print spcr
        print ":: called by [function] : " + fname + " ::"
        for arg, val in zip(argnames, args) + kw.items():
            if arg=="self":
                print arg, "=", type(val)
            else:
                print "%s=%r\t%s" % (arg, val, type(val))  # %r="raw"

        print spcr
        return func(*args, **kw)

    # forces the calling function's docstring for use in sphinx documentation
    echo_func.__doc__ = func.__doc__

    return echo_func

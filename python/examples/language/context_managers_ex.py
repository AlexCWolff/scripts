# Context managers allow you to allocate and release resources precisely when you want to.
# The most widely used example of context managers is the with statement.
# Suppose you have two related operations which you’d like to execute as a pair,
# with a block of code in between. Context managers allow you to do specifically that.

with open('some_file', 'w') as opened_file:
    opened_file.write('Hola!')
# The above code opens the file, writes some data to it and then closes it.
# If an error occurs while writing the data to the file, it tries to close it.
# The above code is equivalent to:

file = open('some_file', 'w')
try:
    file.write('Hola!')
finally:
    file.close()

# While comparing it to the first example we can see that a lot of boilerplate code is eliminated just by using with.
# The main advantage of using a with statement is that it makes sure our file is closed without paying attention
# to how the nested block exits.
# A common use case of context managers is locking and unlocking resources

# At the very least a context manager has an __enter__ and __exit__ methods defined.
# Let’s make our own file opening Context Manager and learn the basics.

class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, traceback):
        self.file_obj.close()
# Just by defining __enter__ and __exit__ methods we can use it in a with statement. Let’s try:

with File('demo.txt', 'w') as opened_file:
    opened_file.write('Hola!')

# Our __exit__ function accepts three arguments. They are required by every __exit__ method
# which is a part of a Context Manager class. Let’s talk about what happens under-the-hood.
# The with statement stores the __exit__ method of File class.
# It calls the __enter__ method of File class.
# __enter__ method opens the file and returns it.
# the opened file handle is passed to opened_file.
# we write to the file using .write()
# with statement calls the stored __exit__ method.
# the __exit__ method closes the file.

# We did not talk about the type, value and traceback arguments of the __exit__ method.
# Between the 4th and 6th step, if an exception occurs, Python passes the type, value and traceback
# of the exception to the __exit__ method. It allows the __exit__ method to decide how to
# close the file and if any further steps are required. In our case we are not paying any attention to them.
# What if our file object raises an exception?
# We might be trying to access a method on the file object which it does not supports.

with File('demo.txt', 'w') as opened_file:
    opened_file.undefined_function('Hola!')

# Let’s list down the steps which are taken by the with statement when an error is encountered.

# It passes the type, value and traceback of the error to the __exit__ method.
# It allows the __exit__ method to handle the exception.
# If __exit__ returns True then the exception was gracefully handled.
# If anything else than True is returned by the __exit__ method then an exception is raised by the with statement.
# In our case the __exit__ method returns None (when no return statement is encountered then the method returns None).
# Therefore, the with statement raises the exception.
# Let’s try handling the exception in the __exit__ method:

class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, traceback):
        print("Exception has been handled")
        self.file_obj.close()
        return True

with File('demo.txt', 'w') as opened_file:
    opened_file.undefined_function()

# Output: Exception has been handled
# Our __exit__ method returned True, therefore no exception was raised by the with statement.

# Instead of a class, we can implement a Context Manager using a generator function.
from contextlib import contextmanager

@contextmanager
def open_file(name):
    f = open(name, 'w')
    yield f
    f.close()
# This way of implementing Context Managers appears to be more intuitive and easy.
# However, this method requires some knowledge about generators, yield, and decorators.
# In this example we have not caught any exceptions which might occur.
# It works in mostly the same way as the previous method.
# Let’s dissect this method a little.
# Python encounters the yield keyword. Due to this it creates a generator instead of a normal function.
# Due to the decoration, contextmanager is called with the function name (open_file) as it’s argument.
# The contextmanager function returns the generator wrapped by the GeneratorContextManager object.
# The GeneratorContextManager is assigned to the open_file function.
# Therefore, when we later call open_file function, we are actually calling the GeneratorContextManager object.
# So now that we know all this, we can use the newly generated Context Manager like this:

with open_file('some_file') as f:
    f.write('hola!')

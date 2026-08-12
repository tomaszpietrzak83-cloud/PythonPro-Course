class MetaValidateMethods(type):
    def __new__(
        cls, name, bases, namespace
    ):  # Intercept class creation before the class is built.
        for (
            attr_name,
            attr_value,
        ) in namespace.items():  # Go through every attribute defined in the class body.
            if attr_name.startswith(
                "__"
            ):  # Ignore magic methods like __init__ or __str__.
                continue  # Skip this attribute and move to the next one.

            if isinstance(
                attr_value, staticmethod
            ):  # Check whether the attribute is a static method.
                function = (
                    attr_value.__func__
                )  # Extract the real function from the staticmethod wrapper.
            elif isinstance(
                attr_value, classmethod
            ):  # Check whether the attribute is a class method.
                function = (
                    attr_value.__func__
                )  # Extract the real function from the classmethod wrapper.
            elif callable(
                attr_value
            ):  # Check whether the attribute is a normal callable method.
                function = attr_value  # Use the function directly.
            else:  # Handle attributes that are not methods.
                continue  # Ignore non-method attributes.

            if (
                not function.__doc__ or not function.__doc__.strip()
            ):  # Check whether the method has a non-empty docstring.
                raise TypeError(
                    f"Method '{attr_name}' in class '{name}' must have a docstring."
                )  # Stop class creation with a clear error.

        return super().__new__(
            cls, name, bases, namespace
        )  # Create the class normally if all methods are documented.


class GoodExample(
    metaclass=MetaValidateMethods
):  # Create a class that uses the validating metaclass.
    def greet(self):  # Define a normal instance method.
        """Return a greeting message."""  # Add the required docstring.
        return "Hello!"  # Return a sample value.

    @staticmethod  # Define a static method to show that wrapped methods are checked too.
    def add(a, b):  # Define a method that adds two numbers.
        """Return the sum of two numbers."""  # Add the required docstring.
        return a + b  # Return the result.

    @classmethod  # Define a class method to show that this case is also supported.
    def class_name(cls):  # Define a method that returns the class name.
        """Return the name of the class."""  # Add the required docstring.
        return cls.__name__  # Return the name of the current class.


good = GoodExample()  # Create an object from the valid class.
print(good.greet())  # Call the documented instance method.
print(GoodExample.add(2, 3))  # Call the documented static method.
print(GoodExample.class_name())  # Call the documented class method.


try:  # Start a block that will catch the metaclass validation error.

    class BadExample(
        metaclass=MetaValidateMethods
    ):  # Try to create a class with a missing docstring.
        def documented(self):  # Define a correctly documented method.
            """This method is documented."""  # Add a proper docstring.
            return "OK"  # Return a sample value.

        def missing_docs(self):  # Define a method without a docstring.
            return "This will fail."  # Return a sample value, but the missing docstring is the real problem.
except TypeError as error:  # Catch the error raised during class creation.
    print(error)  # Print the validation message.

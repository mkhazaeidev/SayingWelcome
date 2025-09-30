"""
Functional Programming - Advanced Level
Enterprise-Grade Functional Patterns Without Classes or Lambdas

This module demonstrates the most advanced functional programming concepts
through sophisticated patterns and techniques. These solutions 
represent production-ready functional programming with advanced compositions
and category theory applications.

Key Concepts Demonstrated:
- Monadic compositions (Maybe, Either, IO) without classes
- Functional reactive programming patterns with streams
- Lens patterns for immutable updates
- Async functional programming
- Reader patterns for dependency injection
- Validation patterns for error accumulation
- Free monads and functional DSLs
- Property-based testing in functional style
- Kleisli composition and category theory

All implementations maintain:
- Pure functions without side effects
- Immutable data transformations
- Professional documentation

Author: Functional Programming Education Project
Version: 1.0
Date: 2025
"""

from typing import Callable, List, Dict, Any, Union, Tuple
from functools import reduce
from datetime import datetime
import asyncio
import re
import random
import string


# Solution 1: Monadic welcome system without classes
def maybe_just(value: Any) -> Tuple:
    """
    Creates a successful Maybe value.
    
    Represents a computation that successfully produced a value.
    In category theory, this is the unit operation for Maybe monad.
    
    Args:
        value: The successfully computed value.
        
    Returns:
        Maybe result tuple: (value, None)
        
    Examples:
        >>> maybe_just("hello")
        ('hello', None)
    """
    return (value, None)


def maybe_nothing() -> Tuple:
    """
    Creates an empty Maybe value.
    
    Represents a computation that produced no value.
    This is the zero element for Maybe monad.
    
    Returns:
        Empty Maybe tuple: (None, None)
        
    Examples:
        >>> maybe_nothing()
        (None, None)
    """
    return (None, None)


def maybe_is_just(maybe_result: Tuple) -> bool:
    """
    Checks if a Maybe result contains a value.
    
    Predicate function for Maybe pattern that determines
    if the computation was successful.
    
    Args:
        maybe_result: Maybe result to check.
        
    Returns:
        True if result contains a value, False otherwise.
        
    Examples:
        >>> maybe_is_just(maybe_just("hello"))
        True
        >>> maybe_is_just(maybe_nothing())
        False
    """
    value, _ = maybe_result
    return value is not None


def maybe_map(maybe_result: Tuple, transform_func: Callable) -> Tuple:
    """
    Applies function to Maybe value if present (Functor pattern).
    
    The map operation allows transforming values within a context
    without leaving that context. This preserves the Maybe structure.
    
    Args:
        maybe_result: Maybe result to transform.
        transform_func: Pure function to apply to the value.
        
    Returns:
        New Maybe with transformed value or nothing.
        
    Examples:
        >>> result = maybe_just("hello")
        >>> maybe_map(result, str.upper)
        ('HELLO', None)
        >>> maybe_map(maybe_nothing(), str.upper)
        (None, None)
    """
    value, _ = maybe_result
    if not maybe_is_just(maybe_result):
        return maybe_nothing()
    try:
        return maybe_just(transform_func(value))
    except Exception:
        return maybe_nothing()


def maybe_bind(maybe_result: Tuple, continuation_func: Callable) -> Tuple:
    """
    Chains Maybe computations (Monadic bind operation).
    
    Also known as flatMap, this operation sequences computations
    that each may fail. If any computation returns nothing,
    the entire chain returns nothing.
    
    Args:
        maybe_result: Result from previous computation.
        continuation_func: Function that takes value and returns Maybe.
        
    Returns:
        Result of continuation or nothing.
        
    Examples:
        >>> def validate_length(text):
        ...     if len(text) > 2:
        ...         return maybe_just(text.upper())
        ...     return maybe_nothing()
        >>> maybe_bind(maybe_just("hi"), validate_length)
        ('HI', None)
        >>> maybe_bind(maybe_just("a"), validate_length)
        (None, None)
    """
    value, _ = maybe_result
    if not maybe_is_just(maybe_result):
        return maybe_nothing()
    try:
        return continuation_func(value)
    except Exception:
        return maybe_nothing()


def read_name_io() -> Callable:
    """
    Creates IO action for reading user input.
    
    In functional programming, we represent side effects as
    values rather than executing them immediately. This IO
    action can be composed with other operations.
    
    Returns:
        IO action that when executed will read user input.
    """
    def io_action() -> str:
        return input("Enter your name: ")
    
    return io_action


def validate_name_monadic(name: str) -> Tuple:
    """
    Validates name using Maybe monad pattern.
    
    Demonstrates validation as a pure function that returns
    a Maybe type instead of raising exceptions.
    
    Args:
        name: User input name to validate.
        
    Returns:
        Maybe with validated name or nothing.
        
    Examples:
        >>> validate_name_monadic("Alice")
        ('Alice', None)
        >>> validate_name_monadic("")
        (None, None)
    """
    if not name or not name.strip():
        return maybe_nothing()
    
    clean_name = name.strip()
    if len(clean_name) < 2 or len(clean_name) > 50:
        return maybe_nothing()
    
    return maybe_just(clean_name.title())


def create_greeting_monadic(name: str) -> str:
    """
    Creates greeting message from validated name.
    
    Pure function that assumes input is valid. This separation
    allows for better composition and testing.
    
    Args:
        name: Validated and sanitized name.
        
    Returns:
        Personalized welcome message.
    """
    return f"Welcome, {name}!"


def monadic_welcome_system() -> Callable:
    """
    Complete monadic welcome system using IO and Maybe.
    
    Composes IO actions with Maybe computations to create
    a pure functional program that handles side effects
    and potential failures explicitly.
    
    Returns:
        IO action that when executed returns Maybe[String]
        
    Examples:
        >>> action = monadic_welcome_system()
        >>> result = action()  # Executes IO and returns Maybe
    """
    def composed_action() -> Tuple:
        name = read_name_io()()
        validated_name = validate_name_monadic(name)
        return maybe_map(validated_name, create_greeting_monadic)
    
    return composed_action


# Solution 2: Functional dependency injection without classes
def create_welcome_service(
    validator: Callable,
    greeter: Callable,
    logger: Callable = print
) -> Callable:
    """
    Creates welcome service with injected dependencies.
    
    Demonstrates functional dependency injection where
    dependencies are passed as functions rather than
    object constructors.
    
    Args:
        validator: Function that validates names and returns Maybe.
        greeter: Function that creates greeting messages.
        logger: Function for logging (defaults to print).
        
    Returns:
        Configured welcome service function.
        
    Examples:
        >>> service = create_welcome_service(validate_name_monadic, create_greeting_monadic)
        >>> result = service("Alice")
        >>> maybe_is_just(result)
        True
    """
    def welcome_service(name: str) -> Tuple:
        result = validator(name)
        
        # Logging as an observable side effect
        if maybe_is_just(result):
            value, _ = result
            logger(f"Greeting created for: {name}")
        else:
            logger(f"Failed to create greeting for: {name}")
        
        return maybe_map(result, greeter)
    
    return welcome_service


# Solution 3: Functional reactive programming with streams
def create_stream(values: List) -> Dict:
    """
    Creates a functional stream data structure.
    
    Streams represent potentially infinite sequences of values.
    This implementation uses dictionaries to represent streams
    without classes.
    
    Args:
        values: Initial values for the stream.
        
    Returns:
        Stream representation as a dictionary.
        
    Examples:
        >>> stream = create_stream([1, 2, 3])
        >>> stream['values']
        [1, 2, 3]
    """
    return {
        'values': values,
        'type': 'stream'
    }


def stream_map(stream: Dict, transform_func: Callable) -> Dict:
    """
    Transforms stream values using mapping function.
    
    Applies a function to every element in the stream,
    creating a new stream with transformed values.
    
    Args:
        stream: Stream to transform.
        transform_func: Function to apply to each element.
        
    Returns:
        New stream with transformed values.
    """
    transformed_values = [transform_func(value) for value in stream['values']]
    return create_stream(transformed_values)


def stream_filter(stream: Dict, predicate_func: Callable) -> Dict:
    """
    Filters stream values using predicate function.
    
    Creates a new stream containing only elements that
    satisfy the predicate condition.
    
    Args:
        stream: Stream to filter.
        predicate_func: Function that returns True for kept elements.
        
    Returns:
        New stream with filtered values.
    """
    filtered_values = [value for value in stream['values'] if predicate_func(value)]
    return create_stream(filtered_values)


def stream_fold(stream: Dict, initial: Any, accumulator_func: Callable) -> Any:
    """
    Reduces stream to a single value (fold operation).
    
    Also known as reduce, this operation combines all
    stream elements into a single result.
    
    Args:
        stream: Stream to fold.
        initial: Initial accumulator value.
        accumulator_func: Function to combine accumulator and element.
        
    Returns:
        Final accumulated value.
    """
    return reduce(accumulator_func, stream['values'], initial)


def create_welcome_stream(names: List[str]) -> Dict:
    """
    Creates a stream of welcome messages from names.
    
    Demonstrates FRP patterns by processing data through
    a stream of transformations.
    
    Args:
        names: List of names to process.
        
    Returns:
        Stream of welcome messages or error placeholders.
    """
    def process_name(name: str) -> str:
        result = validate_name_monadic(name)
        if maybe_is_just(result):
            value, _ = result
            return create_greeting_monadic(value)
        return "Invalid name"
    
    name_stream = create_stream(names)
    welcome_stream = stream_map(name_stream, process_name)
    return welcome_stream


# Solution 4: Lens patterns for functional immutable updates
def create_lens(getter: Callable, setter: Callable) -> Dict:
    """
    Creates a lens for functional immutable updates.
    
    Lenses provide a way to focus on parts of data structures
    and update them immutably. This is crucial for managing
    complex nested state in functional programming.
    
    Args:
        getter: Function to extract value from structure.
        setter: Function to update value in structure.
        
    Returns:
        Lens representation as dictionary of operations.
        
    Examples:
        >>> user = {'name': 'Alice', 'age': 30}
        >>> name_lens = create_lens(lambda u: u['name'], lambda u, n: {**u, 'name': n})
        >>> name_lens['get'](user)
        'Alice'
        >>> updated = name_lens['set'](user, 'Bob')
        >>> updated['name']
        'Bob'
    """
    def lens_get(data: Any) -> Any:
        return getter(data)
    
    def lens_set(data: Any, value: Any) -> Any:
        return setter(data, value)
    
    def lens_modify(data: Any, transform_func: Callable) -> Any:
        current_value = getter(data)
        new_value = transform_func(current_value)
        return setter(data, new_value)
    
    return {
        'get': lens_get,
        'set': lens_set,
        'modify': lens_modify
    }


def create_user_lenses() -> Dict:
    """
    Creates lens collection for user profile manipulation.
    
    Demonstrates how lenses can be composed to work with
    complex nested data structures functionally.
    
    Returns:
        Dictionary of lenses for different user properties.
    """
    def get_name(user: Dict) -> str:
        return user.get('name', '')
    
    def set_name(user: Dict, name: str) -> Dict:
        return {**user, 'name': name}
    
    def get_greeting(user: Dict) -> str:
        return user.get('greeting', '')
    
    def set_greeting(user: Dict, greeting: str) -> Dict:
        return {**user, 'greeting': greeting}
    
    return {
        'name': create_lens(get_name, set_name),
        'greeting': create_lens(get_greeting, set_greeting)
    }


# Solution 5: Async functional programming
async def async_validate_name(name: str) -> Tuple:
    """
    Validates name asynchronously.
    
    Demonstrates how to work with async operations in
    functional programming by treating them as effects
    that can be composed.
    
    Args:
        name: Name to validate.
        
    Returns:
        Maybe result with validated name or nothing.
    """
    await asyncio.sleep(0.1)  # Simulate async operation
    return validate_name_monadic(name)


async def async_create_greeting(name: str) -> str:
    """
    Creates greeting asynchronously.
    
    Simulates an async operation for greeting creation,
    such as fetching templates from a database.
    
    Args:
        name: Validated name to use in greeting.
        
    Returns:
        Greeting message.
    """
    await asyncio.sleep(0.1)
    return create_greeting_monadic(name)


async def async_welcome_system(name: str) -> Tuple:
    """
    Async functional welcome system.
    
    Composes async operations using async/await while
    maintaining functional purity through Maybe types.
    
    Args:
        name: User name to process.
        
    Returns:
        Maybe result with greeting or nothing.
    """
    validated_name = await async_validate_name(name)
    
    if maybe_is_just(validated_name):
        valid_name, _ = validated_name
        greeting = await async_create_greeting(valid_name)
        return maybe_just(greeting)
    
    return maybe_nothing()


# Solution 6: Reader pattern for functional dependency passing
def create_configurable_validator(validator_config: Dict) -> Callable:
    """
    Creates configurable validation using Reader pattern.
    
    Demonstrates how Reader pattern can be used for
    configuration management in functional programming.
    
    Args:
        validator_config: Configuration for validation rules.
        
    Returns:
        Function that takes environment and returns validator.
    """
    def configurable_validator(environment: Dict) -> Callable:
        full_config = {**validator_config, **environment}
        min_len = full_config.get('min_length', 2)
        max_len = full_config.get('max_length', 50)
        
        def validate_with_config(name: str) -> Tuple:
            if not name or len(name.strip()) < min_len:
                return maybe_nothing()
            if len(name.strip()) > max_len:
                return maybe_nothing()
            return maybe_just(create_greeting_monadic(name.strip().title()))
        
        return validate_with_config
    
    return configurable_validator


# Solution 7: Functional error accumulation with Validation pattern
def validation_success(value: Any) -> Tuple:
    """
    Creates successful Validation result.
    
    Validation pattern accumulates errors rather than
    short-circuiting on first error like Maybe.
    
    Args:
        value: Successfully computed value.
        
    Returns:
        Tuple of (value, empty errors list)
    """
    return (value, [])


def validation_failure(errors: List[str]) -> Tuple:
    """
    Creates failed Validation result.
    
    Contains all validation errors that occurred
    during the computation.
    
    Args:
        errors: List of error messages.
        
    Returns:
        Tuple of (None, errors)
    """
    return (None, errors)


def validate_name_accumulative(name: str) -> Tuple:
    """
    Validates name accumulating all errors.
    
    Unlike Maybe which fails fast, this validation
    collects all validation failures.
    
    Args:
        name: Name to validate.
        
    Returns:
        Validation with name or list of all errors.
    """
    errors = []
    
    if not name or not name.strip():
        errors.append("Name cannot be empty")
    
    clean_name = name.strip() if name else ""
    
    if len(clean_name) < 2:
        errors.append("Name must be at least 2 characters")
    
    if len(clean_name) > 50:
        errors.append("Name cannot exceed 50 characters")
    
    if not re.match(r'^[A-Za-z\s\-]+$', clean_name):
        errors.append("Name can only contain letters, spaces, and hyphens")
    
    if errors:
        return validation_failure(errors)
    
    return validation_success(clean_name.title())


# Solution 8: Free monads for functional DSLs
def free_pure(value: Any) -> Dict:
    """
    Lifts a value into Free monad.
    
    Free monads allow building embedded domain-specific
    languages (DSLs) that can be interpreted in different ways.
    
    Args:
        value: Pure value to lift.
        
    Returns:
        Free monad representation.
    """
    return {
        'type': 'free_pure',
        'value': value
    }


def free_map(free_value: Dict, transform_func: Callable) -> Dict:
    """
    Functor map for Free monad.
    
    Applies transformation to the value inside Free monad.
    
    Args:
        free_value: Free monad to transform.
        transform_func: Function to apply.
        
    Returns:
        Transformed Free monad.
    """
    if free_value['type'] == 'free_pure':
        return free_pure(transform_func(free_value['value']))
    return free_value


# Solution 9: Property-based testing in functional style
def generate_random_name() -> str:
    """
    Generates random name for property testing.
    
    Property-based testing requires generating random
    inputs to test properties that should hold for all inputs.
    
    Returns:
        Randomly generated name string.
    """
    length = random.randint(1, 10)
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def test_property_for_all(generator: Callable, 
                         property_func: Callable,
                         num_tests: int = 100) -> bool:
    """
    Tests property for multiple generated inputs.
    
    Property-based testing verifies that properties hold
    across many randomly generated test cases.
    
    Args:
        generator: Function that generates test inputs.
        property_func: Property to test (should return True if property holds).
        num_tests: Number of test cases to generate.
        
    Returns:
        True if property held for all tests, False otherwise.
    """
    for _ in range(num_tests):
        test_input = generator()
        if not property_func(test_input):
            return False
    return True


def greeting_contains_name_property(name: str) -> bool:
    """
    Property: greeting should contain the name.
    
    Example property for property-based testing.
    For valid names, the greeting should contain the name.
    
    Args:
        name: Name to test property against.
        
    Returns:
        True if property holds, False otherwise.
    """
    result = validate_name_monadic(name)
    if maybe_is_just(result):
        value, _ = result
        greeting = create_greeting_monadic(value)
        return name.title() in greeting
    return True  # Property holds for invalid names (no greeting produced)


def run_property_tests() -> bool:
    """
    Runs all property-based tests.
    
    Executes property tests and returns overall result.
    
    Returns:
        True if all properties passed, False otherwise.
    """
    return test_property_for_all(generate_random_name, greeting_contains_name_property, 50)


# Solution 10: Kleisli composition for monadic functions
def kleisli_compose(func1: Callable, func2: Callable) -> Callable:
    """
    Composes monadic functions using Kleisli composition.
    
    Kleisli composition allows chaining functions that
    return monadic values, creating new monadic functions.
    
    Args:
        func1: First monadic function A -> Maybe[B]
        func2: Second monadic function B -> Maybe[C]
        
    Returns:
        Composed function A -> Maybe[C]
        
    Examples:
        >>> def validate(x): return maybe_just(x.upper()) if x else maybe_nothing()
        >>> def greet(x): return maybe_just(f"Hello {x}")
        >>> composed = kleisli_compose(validate, greet)
        >>> composed("alice")
        ('Hello ALICE', None)
    """
    def composed_function(input_value: Any) -> Tuple:
        result1 = func1(input_value)
        return maybe_bind(result1, func2)
    
    return composed_function


def create_kleisli_welcome() -> Callable:
    """
    Creates welcome system using Kleisli composition.
    
    Demonstrates how Kleisli composition can build complex
    pipelines from simple monadic functions.
    
    Returns:
        Composed welcome function.
    """
    def create_greeting_maybe(name: str) -> Tuple:
        return maybe_just(create_greeting_monadic(name))
    
    return kleisli_compose(validate_name_monadic, create_greeting_maybe)


# Demonstration functions
def demonstrate_solution_1():
    """Demonstrates Solution 1: Monadic System."""
    print("Testing Monadic System")
    action = monadic_welcome_system()
    result = action()
    value, _ = result
    if maybe_is_just(result):
        print(f"Greeting: {value}")
    else:
        print("Error: No greeting produced")


def demonstrate_solution_2():
    """Demonstrates Solution 2: Dependency Injection."""
    print("Testing Dependency Injection")
    service = create_welcome_service(validate_name_monadic, create_greeting_monadic)
    name = input("Enter name: ")
    result = service(name)
    value, _ = result
    if maybe_is_just(result):
        print(f"Greeting: {value}")
    else:
        print("Error: Validation failed")


def demonstrate_solution_3():
    """Demonstrates Solution 3: FRP Streams."""
    print("Testing FRP Streams")
    names = ["Alice", "Bob", "", "Charlie"]
    stream = create_welcome_stream(names)
    print(f"Stream values: {stream['values']}")


def demonstrate_solution_4():
    """Demonstrates Solution 4: Lens Patterns."""
    print("Testing Lens Patterns")
    user = {'name': 'Alice', 'greeting': ''}
    lenses = create_user_lenses()
    
    # Use name lens
    name_lens = lenses['name']
    current_name = name_lens['get'](user)
    print(f"Current name: {current_name}")
    
    updated_user = name_lens['set'](user, 'Bob')
    new_name = name_lens['get'](updated_user)
    print(f"Updated name: {new_name}")


def demonstrate_solution_5():
    """Demonstrates Solution 5: Async Functional."""
    print("Testing Async Functional")
    name = input("Enter name: ")
    
    async def run_async():
        result = await async_welcome_system(name)
        return result
    
    # Run async for demonstration
    result = asyncio.run(run_async())
    value, _ = result
    if maybe_is_just(result):
        print(f"Async greeting: {value}")
    else:
        print("Error: Async validation failed")


def demonstrate_solution_6():
    """Demonstrates Solution 6: Reader Pattern."""
    print("Testing Reader Pattern")
    config = {'min_length': 3, 'max_length': 10}
    config_validator = create_configurable_validator(config)
    
    # Apply environment
    environment = {'environment': 'production'}
    validator = config_validator(environment)
    
    name = input("Enter name: ")
    result = validator(name)
    value, _ = result
    if maybe_is_just(result):
        print(f"Greeting: {value}")
    else:
        print("Error: Validation failed with current config")


def demonstrate_solution_7():
    """Demonstrates Solution 7: Error Accumulation."""
    print("Testing Error Accumulation")
    name = input("Enter name (try invalid): ")
    result, errors = validate_name_accumulative(name)
    if errors:
        print(f"Errors: {errors}")
    else:
        print(f"Valid name: {result}")


def demonstrate_solution_8():
    """Demonstrates Solution 8: Free Monads."""
    print("Testing Free Monads")
    free_value = free_pure("Hello")
    transformed = free_map(free_value, str.upper)
    print(f"Free monad value: {transformed['value']}")


def demonstrate_solution_9():
    """Demonstrates Solution 9: Property Testing."""
    print("Testing Property Testing")
    passed = run_property_tests()
    if passed:
        print("All property tests passed!")
    else:
        print("Error: Some property tests failed")


def demonstrate_solution_10():
    """Demonstrates Solution 10: Kleisli Composition."""
    print("Testing Kleisli Composition")
    welcome_func = create_kleisli_welcome()
    name = input("Enter name: ")
    result = welcome_func(name)
    value, _ = result
    if maybe_is_just(result):
        print(f"Greeting: {value}")
    else:
        print("Error: Kleisli composition failed")


def main():
    """
    Interactive demonstration of advanced functional programming.
    
    Provides menu-driven access to the most advanced functional
    programming patterns and category theory concepts.
    """
    solutions = {
        '1': ("Monadic System", demonstrate_solution_1),
        '2': ("Dependency Injection", demonstrate_solution_2),
        '3': ("FRP Streams", demonstrate_solution_3),
        '4': ("Lens Patterns", demonstrate_solution_4),
        '5': ("Async Functional", demonstrate_solution_5),
        '6': ("Reader Pattern", demonstrate_solution_6),
        '7': ("Error Accumulation", demonstrate_solution_7),
        '8': ("Free Monads", demonstrate_solution_8),
        '9': ("Property Testing", demonstrate_solution_9),
        '10': ("Kleisli Composition", demonstrate_solution_10)
    }
    
    print("Functional Programming - Advanced Level")
    
    for key, (description, _) in solutions.items():
        print(f"{key}. {description}")
    
    print("\nEnter 'q' to quit.")
    
    while True:
        choice = input("\nChoose solution (1-10): ").strip()
        
        if choice.lower() == 'q':
            print("Thank you for exploring Advanced Functional Programming!")
            break
        
        if choice in solutions:
            try:
                procedure = solutions[choice][1]
                procedure()
            except Exception as error:
                print(f"Error: Demonstration error: {error}")
        else:
            print("Error: Invalid choice. Please enter 1-10 or 'q'.")


if __name__ == "__main__":
    main()

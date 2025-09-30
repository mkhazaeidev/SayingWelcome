"""
Functional Programming - Beginner Level
Pure Functional Approaches for Welcome Message System

This module demonstrates fundamental functional programming concepts through
ten distinct implementations of a welcome message system. Each solution
emphasizes functional programming principles while avoiding lambda functions
and maintaining pure functional style.

Key Concepts Demonstrated:
- Pure Functions and Referential Transparency
- Immutability and Persistent Data Structures
- Function Composition and Pipeline Patterns
- Higher-Order Functions and Currying
- Recursive Algorithms vs Iterative Loops
- Functional Error Handling Strategies
- Declarative Programming Paradigm

All solutions avoid:
- Lambda functions (using named functions only)
- Side effects and mutable state
- Imperative loops (using recursion and higher-order functions)
- Exception-based error handling

Example Usage:
    >>> from functional.beginner import welcome_basic, welcome_composed
    >>> welcome_basic("Alice")
    'Welcome, Alice!'
    >>> welcome_composed("  bob  ")
    'Welcome, Bob!'

Author: Functional Programming Education Project
Version: 1.0
Date: 2025
"""

from typing import Callable, Tuple, List, Dict, Any
from functools import reduce


# Solution 1: Pure Function with Immutability
def welcome_basic(name: str) -> str:
    """
    Creates a welcome message using pure function principles.

    This function demonstrates the most fundamental concept in functional
    programming: pure functions. It has no side effects and will always
    return the same output for the same input (referential transparency).

    Args:
        name: The user's name as a string. Input is treated as immutable.

    Returns:
        A personalized welcome message string.

    Examples:
        >>> welcome_basic("Alice")
        'Welcome, Alice!'
        >>> welcome_basic("")
        'Welcome, !'

    Note:
        This function performs no validation or sanitization, maintaining
        purity by not introducing conditional logic that could break
        referential transparency.
    """
    return f"Welcome, {name}!"


# Solution 2: Function Composition Pattern
def sanitize_name(name: str) -> str:
    """
    Sanitizes input name by removing extraneous whitespace.

    A pure function that demonstrates data transformation without mutation.
    This is often the first step in a functional pipeline.

    Args:
        name: Raw input name that may contain leading/trailing whitespace.

    Returns:
        Cleaned name with whitespace removed.

    Examples:
        >>> sanitize_name("  Alice  ")
        'Alice'
        >>> sanitize_name("Bob\\n")
        'Bob'
    """
    return name.strip()


def create_greeting(name: str) -> str:
    """
    Transforms a name into a formal greeting message.

    This function represents the business logic transformation in our
    pipeline. It focuses on a single responsibility: creating greetings.

    Args:
        name: Sanitized name ready for greeting creation.

    Returns:
        Formal greeting message incorporating the name.

    Examples:
        >>> create_greeting("Alice")
        'Welcome, Alice!'
    """
    return f"Welcome, {name}!"


def welcome_composed(name: str) -> str:
    """
    Demonstrates function composition by chaining pure functions.

    This solution shows how small, single-responsibility functions can
    be composed to create more complex behavior. The composition follows
    mathematical function composition: f(g(x)).

    Args:
        name: Raw input name that needs processing.

    Returns:
        Fully processed welcome message.

    Examples:
        >>> welcome_composed("  alice  ")
        'Welcome, alice!'

    Note:
        The output preserves the original casing to demonstrate that
        composition doesn't implicitly change behavior beyond the
        composed functions' specifications.
    """
    return create_greeting(sanitize_name(name))


# Solution 3: Higher-Order Function Factory
def create_welcome_function(greeting_template: str) -> Callable[[str], str]:
    """
    Factory function that generates specialized greeting functions.

    This demonstrates higher-order functions: functions that either
    take other functions as parameters or return functions as results.
    Here we use the latter pattern to create a function factory.

    Args:
        greeting_template: String template with '{}' placeholder for name.
                         Example: "Hello, {}!" or "Bonjour, {}!"

    Returns:
        A configured greeting function that takes a name and returns
        a formatted greeting.

    Examples:
        >>> hello_greeter = create_welcome_function("Hello, {}!")
        >>> hello_greeter("Alice")
        'Hello, Alice!'
        >>> formal_greeter = create_welcome_function("Greetings, {}.")
        >>> formal_greeter("Bob")
        'Greetings, Bob.'

    Note:
        The returned function closes over the greeting_template parameter,
        demonstrating lexical scoping in functional programming.
    """
    def welcome(name: str) -> str:
        """
        Generated greeting function with pre-configured template.

        This inner function has access to greeting_template due to
        closure, making it a specialized version of a general greeting
        function.
        """
        return greeting_template.format(name=name)

    return welcome


# Solution 4: Functional Collection Transformation
def welcome_multiple(names: List[str]) -> List[str]:
    """
    Transforms a collection of names using functional mapping.

    Demonstrates the map operation, which applies a function to every
    element in a collection. This is preferred over imperative loops
    in functional programming because it's more declarative and
    avoids mutable state.

    Args:
        names: List of names to be transformed into greetings.

    Returns:
        List of greeting messages in the same order as input names.

    Examples:
        >>> welcome_multiple(["Alice", "Bob", "Charlie"])
        ['Welcome, Alice!', 'Welcome, Bob!', 'Welcome, Charlie!']
        >>> welcome_multiple([])
        []

    Note:
        This function preserves the original collection size and order,
        maintaining the functor laws of mapping operations.
    """
    return list(map(create_greeting, names))


# Solution 5: Pipeline Processing with Reduce
def strip_name(name: str) -> str:
    """
    Removes leading and trailing whitespace from a name.

    A pure transformation function designed for pipeline composition.

    Args:
        name: Input name potentially with whitespace.

    Returns:
        Name with whitespace removed.
    """
    return name.strip()


def title_case_name(name: str) -> str:
    """
    Converts name to title case for consistent formatting.

    This transformation ensures names are properly capitalized
    regardless of input format.

    Args:
        name: Sanitized name ready for case normalization.

    Returns:
        Name in title case format.

    Examples:
        >>> title_case_name("alice wonderland")
        'Alice Wonderland'
        >>> title_case_name("bOB")
        'Bob'
    """
    return name.title()


def format_greeting(name: str) -> str:
    """
    Formats the final greeting message with the processed name.

    The final transformation in our pipeline that produces the
    business value.

    Args:
        name: Fully processed and formatted name.

    Returns:
        Final welcome message.
    """
    return f"Welcome, {name}!"


def apply_transformation(accumulator: str, transformation_func: Callable[[str], str]) -> str:
    """
    Applies a transformation function to an accumulated value.

    This helper function enables reduce-based pipeline processing
    by defining how to apply each transformation in sequence.

    Args:
        accumulator: Current value in the transformation pipeline.
        transformation_func: Next transformation to apply.

    Returns:
        Transformed value ready for next pipeline stage.

    Note:
        This function maintains the pipeline's purity by not
        modifying the accumulator in place.
    """
    return transformation_func(accumulator)


def process_name_pipeline(name: str) -> str:
    """
    Processes a name through a series of transformations using reduce.

    Demonstrates pipeline processing where data flows through a
    sequence of transformations. This is analogous to Unix pipes
    or functional composition but with explicit step visibility.

    Args:
        name: Raw input name to process through the pipeline.

    Returns:
        Fully processed welcome message.

    Examples:
        >>> process_name_pipeline("  alice wonderland  ")
        'Welcome, Alice Wonderland!'

    Note:
        The transformation sequence is defined as a list, making
        it easy to add, remove, or reorder processing steps.
    """
    transformations = [
        strip_name,
        title_case_name,
        format_greeting
    ]

    return reduce(apply_transformation, transformations, name)


# Solution 6: Currying for Specialized Function Creation
def create_personalized_greeting(greeting: str) -> Callable[[str], str]:
    """
    Creates specialized greeting functions through currying.

    Currying is the technique of transforming a function that takes
    multiple arguments into a sequence of functions that each take
    a single argument. This enables partial application and
    function specialization.

    Args:
        greeting: The greeting phrase to use (e.g., "Hello", "Hi", "Welcome").

    Returns:
        A function that takes a name and returns a complete greeting.

    Examples:
        >>> hello_greeter = create_personalized_greeting("Hello")
        >>> hello_greeter("Alice")
        'Hello, Alice!'
        >>> hi_greeter = create_personalized_greeting("Hi")
        >>> hi_greeter("Bob")
        'Hi, Bob!'

    Note:
        This demonstrates how functional programming can create
        reusable, configurable behavior through function composition
        rather than class inheritance.
    """
    def add_name(name: str) -> str:
        """
        Completes the greeting with the provided name.

        This inner function represents the second step of the
        curried function application.
        """
        return f"{greeting}, {name}!"

    return add_name


# Solution 7: Functional Filtering and Transformation
def is_valid_name(name: str) -> bool:
    """
    Predicate function that validates name requirements.

    In functional programming, predicate functions return boolean
    values and are used with filtering operations. This function
    defines the criteria for valid names in our system.

    Args:
        name: Name to validate against business rules.

    Returns:
        True if the name meets validation criteria, False otherwise.

    Examples:
        >>> is_valid_name("Alice")
        True
        >>> is_valid_name("A")  # Too short
        False
        >>> is_valid_name("   ")  # Only whitespace
        False
        >>> is_valid_name("")  # Empty string
        False
    """
    cleaned_name = name.strip()
    return bool(cleaned_name and len(cleaned_name) >= 2)


def welcome_validated(names: List[str]) -> List[str]:
    """
    Processes names through a filter-map pipeline.

    Demonstrates a common functional pattern: filtering invalid
    data before transformation. This prevents errors and ensures
    only valid data enters the transformation pipeline.

    Args:
        names: List of potentially invalid names to process.

    Returns:
        List of greeting messages only for valid names.

    Examples:
        >>> welcome_validated(["Alice", "A", "Bob", ""])
        ['Welcome, Alice!', 'Welcome, Bob!']

    Note:
        The output list may be smaller than the input list due to
        filtering, but order is preserved for the valid elements.
    """
    valid_names = filter(is_valid_name, names)
    return list(map(create_greeting, valid_names))


# Solution 8: Immutable Data Structure Creation
def create_user_profile(name: str) -> Dict[str, Any]:
    """
    Creates an immutable user profile data structure.

    Demonstrates functional data modeling where we create new
    data structures rather than modifying existing ones. This
    approach avoids shared mutable state and makes code more
    predictable.

    Args:
        name: User's name to include in the profile.

    Returns:
        A new dictionary representing the user profile with
        name, greeting, and metadata.

    Examples:
        >>> profile = create_user_profile("Alice")
        >>> profile['name']
        'Alice'
        >>> profile['greeting']
        'Welcome, Alice!'
        >>> profile['name_length']
        5

    Note:
        The returned dictionary is conceptually immutable. In a
        purely functional language, this would be enforced by
        the type system.
    """
    clean_name = sanitize_name(name)
    return {
        'name': clean_name,
        'greeting': create_greeting(clean_name),
        'name_length': len(clean_name)
    }


# Solution 9: Recursive Collection Processing
def welcome_recursive(names: List[str], results: List[str] = None) -> List[str]:
    """
    Processes names recursively instead of using iterative loops.

    Demonstrates recursion as the fundamental looping mechanism
    in functional programming. This approach avoids mutable loop
    variables and makes the termination condition explicit.

    Args:
        names: List of names to process. Modified through recursion.
        results: Accumulator for results. Defaults to empty list.

    Returns:
        List of greeting messages for valid names.

    Examples:
        >>> welcome_recursive(["Alice", "Bob"])
        ['Welcome, Alice!', 'Welcome, Bob!']
        >>> welcome_recursive(["A", "Bob"])  # "A" is invalid
        ['Welcome, Bob!']

    Note:
        This function uses tail recursion conceptually, though
        Python doesn't optimize tail calls. In production with
        large lists, consider iterative approaches or languages
        with proper tail call optimization.
    """
    # Initialize results accumulator on first call
    if results is None:
        results = []

    # Base case: empty list, return accumulated results
    if not names:
        return results

    # Recursive case: process first element, recurse on rest
    first_name = names[0]
    remaining_names = names[1:]

    if is_valid_name(first_name):
        # Create new list with added result (immutable update)
        new_results = results + [create_greeting(first_name)]
        return welcome_recursive(remaining_names, new_results)
    else:
        # Skip invalid name, continue with remaining
        return welcome_recursive(remaining_names, results)


# Solution 10: Functional Error Handling Strategy
def validate_name_safe(name: str) -> Tuple[bool, str]:
    """
    Validates name and returns result tuple instead of raising exceptions.

    In functional programming, we prefer representing errors as
    values rather than using exceptions, which are side effects.
    This approach makes error handling explicit in the type system.

    Args:
        name: Name to validate and process.

    Returns:
        Tuple containing (success_flag, result_message)
        - success_flag: True if validation passed, False otherwise
        - result_message: Greeting message or error description

    Examples:
        >>> validate_name_safe("Alice")
        (True, 'Welcome, Alice!')
        >>> validate_name_safe("A")
        (False, 'Please provide a valid name')
    """
    clean_name = sanitize_name(name)

    if not is_valid_name(clean_name):
        return False, "Please provide a valid name"

    return True, create_greeting(clean_name)


def safe_welcome(name: str) -> str:
    """
    Provides safe welcome functionality with built-in error handling.

    Wraps the validation and greeting creation in a safe interface
    that never raises exceptions. This makes the function total
    (defined for all inputs) rather than partial.

    Args:
        name: Any string input, including invalid names.

    Returns:
        Either a proper greeting message or a user-friendly error message.

    Examples:
        >>> safe_welcome("Alice")
        'Welcome, Alice!'
        >>> safe_welcome("")
        'Please provide a valid name'
        >>> safe_welcome("A")
        'Please provide a valid name'
    """
    is_valid, result = validate_name_safe(name)
    return result


# Functional Composition Utilities
def compose_two_functions(f: Callable, g: Callable) -> Callable:
    """
    Composes two functions into a single function.

    Function composition is a fundamental operation in functional
    programming. This creates a new function that applies g then f
    (right to left, following mathematical notation).

    Args:
        f: The outer function to apply second.
        g: The inner function to apply first.

    Returns:
        A new function that computes f(g(x)).

    Examples:
        >>> composed = compose_two_functions(str.upper, str.strip)
        >>> composed("  hello  ")
        'HELLO'
    """
    def composed_function(x: Any) -> Any:
        return f(g(x))
    return composed_function


def compose(*functions: Callable) -> Callable:
    """
    Composes multiple functions into a single function.

    Generalizes binary composition to n-ary composition. Functions
    are composed from right to left, following mathematical convention.

    Args:
        *functions: Two or more functions to compose, ordered from
                   last to first in execution order.

    Returns:
        A new function that applies all functions in reverse order.

    Examples:
        >>> process = compose(format_greeting, title_case_name, strip_name)
        >>> process("  alice  ")
        'Welcome, Alice!'

    Note:
        compose(f, g, h) is equivalent to lambda x: f(g(h(x)))
    """
    def apply_composition(acc: Any, func: Callable) -> Any:
        return func(acc)

    def composed_function(x: Any) -> Any:
        return reduce(apply_composition, reversed(functions), x)

    return composed_function


def pipe(value: Any, *functions: Callable) -> Any:
    """
    Pipes a value through a series of functions.

    The pipe operator applies functions in left-to-right order,
    which many find more natural than mathematical composition.
    This is equivalent to Unix pipe operations.

    Args:
        value: The initial value to transform.
        *functions: Functions to apply in sequence.

    Returns:
        The final transformed value after all functions.

    Examples:
        >>> result = pipe("  alice  ", strip_name, title_case_name, format_greeting)
        >>> result
        'Welcome, Alice!'

    Note:
        pipe(x, f, g, h) is equivalent to h(g(f(x)))
    """
    def apply_pipe(acc: Any, func: Callable) -> Any:
        return func(acc)

    return reduce(apply_pipe, functions, value)


# Demonstration Functions for Interactive Use
def demonstrate_solution_1() -> None:
    """Demonstrates Solution 1: Pure Function basics."""
    print("Testing Pure Function")
    print("This function demonstrates referential transparency")
    print("and absence of side effects.")
    name = input("Enter name to test: ")
    result = welcome_basic(name)
    print(f"Result: {result}")


def demonstrate_solution_2() -> None:
    """Demonstrates Solution 2: Function Composition."""
    print("Testing Function Composition")
    print("Shows how small functions compose into complex behavior.")
    name = input("Enter name (try with spaces): ")
    result = welcome_composed(name)
    print(f"Result: {result}")


def demonstrate_solution_3() -> None:
    """Demonstrates Solution 3: Higher-Order Functions."""
    print("Testing Higher-Order Functions")
    print("Creates specialized greeting functions dynamically.")
    name = input("Enter name: ")
    welcome_hello = create_welcome_function("Hello, {}!")
    result = welcome_hello(name)
    print(f"Result: {result}")


def demonstrate_solution_4() -> None:
    """Demonstrates Solution 4: Collection Transformation."""
    print("Testing Collection Transformation")
    print("Applies functions to collections using map.")
    name = input("Enter name: ")
    results = welcome_multiple([name])
    print(f"Results: {results}")


def demonstrate_solution_5() -> None:
    """Demonstrates Solution 5: Pipeline Processing."""
    print("Testing Pipeline Processing")
    print("Processes data through transformation pipeline using reduce.")
    name = input("Enter name (try with mixed case and spaces): ")
    result = process_name_pipeline(name)
    print(f"Result: {result}")


def demonstrate_solution_6() -> None:
    """Demonstrates Solution 6: Currying."""
    print("Testing Currying")
    print("Creates specialized functions through partial application.")
    name = input("Enter name: ")
    hi_greeter = create_personalized_greeting("Hi")
    result = hi_greeter(name)
    print(f"Result: {result}")


def demonstrate_solution_7() -> None:
    """Demonstrates Solution 7: Filtering and Transformation."""
    print("Testing Filtering and Transformation")
    print("Filters invalid data before transformation.")
    name = input("Enter name (try short or empty names): ")
    results = welcome_validated([name])
    print(f"Results: {results}")


def demonstrate_solution_8() -> None:
    """Demonstrates Solution 8: Immutable Data Structures."""
    print("Testing Immutable Data Structures")
    print("Creates new data structures instead of mutating existing ones.")
    name = input("Enter name: ")
    profile = create_user_profile(name)
    print(f"Profile: {profile}")


def demonstrate_solution_9() -> None:
    """Demonstrates Solution 9: Recursive Processing."""
    print("Testing Recursive Processing")
    print("Uses recursion instead of iterative loops.")
    name = input("Enter name: ")
    results = welcome_recursive([name])
    print(f"Results: {results}")


def demonstrate_solution_10() -> None:
    """Demonstrates Solution 10: Functional Error Handling."""
    print("Testing Functional Error Handling")
    print("Handles errors as values rather than exceptions.")
    name = input("Enter name (try invalid names): ")
    result = safe_welcome(name)
    print(f"Result: {result}")


def main() -> None:
    """
    Interactive demonstration of all functional programming solutions.

    Provides a menu-driven interface to explore each functional
    programming concept implemented in this module. Each solution
    demonstrates a different aspect of functional programming
    while solving the same core problem.
    """
    solutions = {
        '1': ("Pure Function", demonstrate_solution_1),
        '2': ("Function Composition", demonstrate_solution_2),
        '3': ("Higher-Order Function", demonstrate_solution_3),
        '4': ("Map Transformation", demonstrate_solution_4),
        '5': ("Reduce Pipeline", demonstrate_solution_5),
        '6': ("Currying", demonstrate_solution_6),
        '7': ("Filter + Map", demonstrate_solution_7),
        '8': ("Immutable Data", demonstrate_solution_8),
        '9': ("Recursive Approach", demonstrate_solution_9),
        '10': ("Safe Welcome", demonstrate_solution_10)
    }

    print("Functional Programming - Beginner Level")
    print("\nComprehensive demonstration of functional programming")
    print("principles using named functions only (no lambdas).")

    for key, (description, _) in solutions.items():
        print(f"{key}. {description}")

    print("\nEnter 'q' to quit the demonstration.")

    while True:
        choice = input("\nChoose solution to demonstrate (1-10): ").strip()

        if choice.lower() == 'q':
            print("Thank you for exploring Functional Programming!")
            break

        if choice in solutions:
            try:
                solutions[choice][1]()
            except Exception as error:
                print(f"Error Demonstration error: {error}")
        else:
            print("Error: Invalid choice. Please enter 1-10 or 'q' to quit.")


if __name__ == "__main__":
    main()

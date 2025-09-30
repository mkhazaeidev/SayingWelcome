"""
Functional Programming - Intermediate Level
Advanced Functional Approaches with Comprehensive Error Handling and Composition

This module demonstrates intermediate functional programming concepts through
sophisticated patterns and techniques. The solutions showcase pure functional programming with
advanced error handling, composition patterns, and immutable data flow.

Key Concepts Demonstrated:
- Monadic error handling with Either pattern (class-free implementation)
- Advanced function composition and pipeline patterns
- Immutable state management using closures
- Functional data validation and sanitization
- Memoization and performance optimization
- Feature toggles and configuration management
- Async patterns in functional style

All implementations maintain:
- Pure functions without side effects
- Immutable data transformations
- Comprehensive type safety

Author: Functional Programming Education Project
Version: 1.0
Date: 2025
"""

from typing import Callable, Tuple, Optional, List, Dict, Any, Union
from functools import reduce, partial
from datetime import datetime
import re
import asyncio


# Type definitions for functional error handling
EitherResult = Union[Tuple[None, str], Tuple[Any, None]]  # (value, error) pattern


# Solution 1: Functional validation with Either pattern (class-free)
def either_success(value: Any) -> EitherResult:
    """
    Creates a successful Either result.

    In functional programming, we represent computations that can fail
    using sum types. Here we use tuples to represent Either[Value, Error]
    without creating classes.

    Args:
        value: The successful computation result.

    Returns:
        A tuple representing success: (value, None)

    Examples:
        >>> either_success("Hello")
        ('Hello', None)
    """
    return (value, None)


def either_failure(error: str) -> EitherResult:
    """
    Creates a failed Either result.

    Represents a computation that failed with an error message.
    This approach avoids exceptions and makes error handling explicit.

    Args:
        error: Description of what went wrong.

    Returns:
        A tuple representing failure: (None, error)

    Examples:
        >>> either_failure("Invalid input")
        (None, 'Invalid input')
    """
    return (None, error)


def either_map(either_result: EitherResult, transform_func: Callable) -> EitherResult:
    """
    Applies a function to the value in an Either if it's successful.

    This is the functor map operation for our Either implementation.
    If the result is successful, apply the transformation; if it failed,
    propagate the error unchanged.

    Args:
        either_result: Either result from a previous computation.
        transform_func: Pure function to apply to the successful value.

    Returns:
        New Either result with transformed value or original error.

    Examples:
        >>> result = either_success("hello")
        >>> either_map(result, str.upper)
        ('HELLO', None)
        >>> failed = either_failure("error")
        >>> either_map(failed, str.upper)
        (None, 'error')
    """
    value, error = either_result
    if error is not None:
        return either_result
    try:
        return either_success(transform_func(value))
    except Exception as e:
        return either_failure(f"Mapping error: {str(e)}")


def either_bind(either_result: EitherResult, continuation_func: Callable) -> EitherResult:
    """
    Chains computations that may fail (monadic bind operation).

    Also known as flatMap, this operation allows sequencing of
    computations that each return Either results. If any computation
    fails, the error propagates through the chain.

    Args:
        either_result: Result from previous computation.
        continuation_func: Function that takes a value and returns Either.

    Returns:
        Result of the continuation or the original error.

    Examples:
        >>> def validate_length(text):
        ...     if len(text) > 3:
        ...         return either_success(text)
        ...     return either_failure("Too short")
        >>> either_bind(either_success("test"), validate_length)
        ('test', None)
        >>> either_bind(either_success("a"), validate_length)
        (None, 'Too short')
    """
    value, error = either_result
    if error is not None:
        return either_result
    try:
        return continuation_func(value)
    except Exception as e:
        return either_failure(f"Binding error: {str(e)}")


def validate_name_functional(name: str) -> EitherResult:
    """
    Validates name using functional Either pattern.

    Demonstrates comprehensive validation without exceptions.
    Each validation check is a pure function that returns Either.

    Args:
        name: User input name to validate.

    Returns:
        Either success with sanitized name or error message.

    Examples:
        >>> validate_name_functional("Alice")
        ('Alice', None)
        >>> validate_name_functional("")
        (None, 'Name cannot be empty')
        >>> validate_name_functional("A")
        (None, 'Name must be at least 2 characters')
    """
    if not name or not name.strip():
        return either_failure("Name cannot be empty")

    clean_name = name.strip()

    if len(clean_name) < 2:
        return either_failure("Name must be at least 2 characters")

    if len(clean_name) > 50:
        return either_failure("Name cannot exceed 50 characters")

    if not re.match(r'^[A-Za-z\s\-]+$', clean_name):
        return either_failure("Name can only contain letters, spaces, and hyphens")

    return either_success(clean_name.title())


def create_welcome_message(name: str) -> str:
    """
    Creates welcome message from validated name.

    Pure function that assumes input is already validated.
    This separation allows for easier testing and composition.

    Args:
        name: Validated and sanitized name.

    Returns:
        Personalized welcome message.
    """
    return f"Welcome, {name}!"


def welcome_with_validation(name: str) -> EitherResult:
    """
    Functional welcome with comprehensive validation using Either.

    Composes validation and message creation using monadic operations.
    This approach makes error handling explicit in the type system.

    Args:
        name: Raw user input name.

    Returns:
        Either success with welcome message or error description.

    Examples:
        >>> welcome_with_validation("Alice")
        ('Welcome, Alice!', None)
        >>> welcome_with_validation("")
        (None, 'Name cannot be empty')
    """
    return either_map(
        validate_name_functional(name),
        create_welcome_message
    )


# Solution 2: Time-based greeting with functional composition
def get_current_hour() -> int:
    """
    Gets current hour as a pure function.

    While getting current time is technically a side effect,
    we treat it as a boundary of our pure functional core.
    In a more strict FP environment, we'd use IO monad.

    Returns:
        Current hour as integer (0-23).
    """
    return datetime.now().hour


def get_time_greeting(hour: int) -> str:
    """
    Determines appropriate greeting based on time of day.

    Pure function that encapsulates time-based greeting logic.

    Args:
        hour: Current hour (0-23).

    Returns:
        Time-appropriate greeting phrase.

    Examples:
        >>> get_time_greeting(8)
        'Good morning'
        >>> get_time_greeting(14)
        'Good afternoon'
        >>> get_time_greeting(20)
        'Good evening'
    """
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


def create_time_based_greeting(name: str) -> str:
    """
    Creates time-based greeting using function composition.

    Demonstrates how to work with side effects (current time)
    in a functional way by pushing them to the boundaries.

    Args:
        name: User's name to include in greeting.

    Returns:
        Time-appropriate personalized greeting.
    """
    def sanitize_input(text: str) -> str:
        return text.strip() or "Guest"

    def build_greeting(sanitized_name: str) -> str:
        time_greeting = get_time_greeting(get_current_hour())
        return f"{time_greeting}, {sanitized_name}!"

    return build_greeting(sanitize_input(name))


# Solution 3: Multi-language support with functional configuration
def create_language_greeter(language: str) -> Callable[[str], str]:
    """
    Creates language-specific greeting functions.

    Higher-order function that returns configured greeters
    based on language selection. Demonstrates functional
    configuration and specialization.

    Args:
        language: Language code ('english', 'spanish', etc.)

    Returns:
        Function that creates greetings in the specified language.

    Examples:
        >>> spanish_greeter = create_language_greeter('spanish')
        >>> spanish_greeter("Maria")
        'Bienvenido, Maria!'
    """
    language_greetings = {
        'english': 'Welcome',
        'spanish': 'Bienvenido',
        'french': 'Bienvenue',
        'german': 'Willkommen',
        'italian': 'Benvenuto'
    }

    greeting_word = language_greetings.get(language.lower(), 'Welcome')

    def greet_in_language(name: str) -> str:
        clean_name = name.strip().title()
        return f"{greeting_word}, {clean_name}!"

    return greet_in_language


# Solution 4: Functional state management using closures
def create_session_manager() -> Tuple[Callable[[str], Dict], Callable[[], Dict]]:
    """
    Creates functional state management system.

    Returns two functions: one for adding greetings to the session,
    and one for getting the current session state. This demonstrates
    how to manage state functionally using closures instead of classes.

    Returns:
        Tuple of (add_greeting_function, get_state_function)

    Examples:
        >>> add_greet, get_state = create_session_manager()
        >>> add_greet("Alice")
        >>> state = get_state()
        >>> state['greeting_count']
        1
    """
    session_state = {
        'start_time': datetime.now(),
        'greeting_count': 0,
        'users': [],
        'last_activity': datetime.now()
    }

    def add_greeting(name: str) -> Dict[str, Any]:
        """
        Adds a greeting to the session immutably.

        Instead of mutating the session state, this function
        computes a new state based on the current state.

        Args:
            name: User name to add to session.

        Returns:
            Updated session state.
        """
        clean_name = name.strip().title()
        new_users = session_state['users'] + [clean_name]

        # Create new state (conceptually immutable)
        new_state = {
            'start_time': session_state['start_time'],
            'greeting_count': session_state['greeting_count'] + 1,
            'users': new_users,
            'last_activity': datetime.now(),
            'current_greeting': create_welcome_message(clean_name)
        }

        # Update closure state (in real FP, we'd return new state)
        nonlocal session_state
        session_state = new_state

        return new_state

    def get_session_state() -> Dict[str, Any]:
        """
        Gets current session state.

        Returns:
            Current session state dictionary.
        """
        return session_state.copy()  # Return copy to prevent mutation

    return add_greeting, get_session_state


# Solution 5: Functional configuration management
def create_configurable_validator(
    min_length: int = 2,
    max_length: int = 50,
    allow_numbers: bool = False
) -> Callable[[str], EitherResult]:
    """
    Creates configurable validation functions.

    Higher-order function that returns validators with specific
    configuration. Demonstrates how to create specialized behavior
    through function configuration.

    Args:
        min_length: Minimum valid name length.
        max_length: Maximum valid name length.
        allow_numbers: Whether to allow digits in names.

    Returns:
        Configured validation function that returns Either.

    Examples:
        >>> strict_validator = create_configurable_validator(3, 30, False)
        >>> strict_validator("Al")
        (None, 'Name must be at least 3 characters')
        >>> lenient_validator = create_configurable_validator(1, 100, True)
        >>> lenient_validator("A1")
        ('A1', None)
    """
    def configured_validator(name: str) -> EitherResult:
        clean_name = name.strip()

        if not clean_name:
            return either_failure("Name cannot be empty")

        if len(clean_name) < min_length:
            return either_failure(f"Name must be at least {min_length} characters")

        if len(clean_name) > max_length:
            return either_failure(f"Name cannot exceed {max_length} characters")

        if not allow_numbers and any(char.isdigit() for char in clean_name):
            return either_failure("Name cannot contain numbers")

        return either_success(create_welcome_message(clean_name.title()))

    return configured_validator


# Solution 6: Functional error recovery patterns
def create_fallback_strategy(
    primary_strategy: Callable,
    fallback_strategy: Callable
) -> Callable:
    """
    Creates error recovery strategy through function composition.

    Higher-order function that combines primary and fallback strategies.
    If primary fails (returns Either error), fallback is used.

    Args:
        primary_strategy: Main strategy function.
        fallback_strategy: Backup strategy when primary fails.

    Returns:
        Composite function that tries primary, then fallback.

    Examples:
        >>> def primary(x): return either_success(x.upper())
        >>> def fallback(x): return either_success("Guest")
        >>> strategy = create_fallback_strategy(primary, fallback)
        >>> result = strategy("hello")
        >>> result[0]
        'HELLO'
    """
    def recovered_function(*args, **kwargs):
        primary_result = primary_strategy(*args, **kwargs)

        # Check if primary failed (has error)
        if primary_result[1] is not None:
            return fallback_strategy(*args, **kwargs)

        return primary_result

    return recovered_function


# Solution 7: Functional data transformation pipeline
def create_processing_pipeline() -> Callable[[List[str]], Dict[str, Any]]:
    """
    Creates analytics pipeline using functional composition.

    Demonstrates building complex data processing pipelines
    from simple, composable functions.

    Returns:
        Pipeline function that processes lists of names.

    Examples:
        >>> pipeline = create_processing_pipeline()
        >>> result = pipeline(["Alice", "Bob", ""])
        >>> result['valid_greetings']
        2
        >>> result['success_rate']
        0.6666666666666666
    """
    def is_valid_name(name: str) -> bool:
        clean_name = name.strip()
        return bool(clean_name and len(clean_name) >= 2)

    def process_names(names: List[str]) -> Dict[str, Any]:
        valid_names = list(filter(is_valid_name, names))
        greetings = list(map(create_welcome_message, valid_names))

        total_count = len(names)
        valid_count = len(valid_names)

        return {
            'total_processed': total_count,
            'valid_greetings': valid_count,
            'success_rate': valid_count / total_count if total_count > 0 else 0,
            'greetings': greetings,
            'invalid_count': total_count - valid_count
        }

    return process_names


# Solution 8: Memoization for functional performance optimization
def create_memoized_function(original_func: Callable) -> Callable:
    """
    Creates memoized version of a function.

    Memoization caches function results to avoid recomputation
    for same inputs. This is a pure functional optimization
    technique.

    Args:
        original_func: Pure function to memoize.

    Returns:
        Memoized version of the function.

    Examples:
        >>> def expensive(x): return x * 1000
        >>> memoized = create_memoized_function(expensive)
        >>> memoized(5)  # Computes
        5000
        >>> memoized(5)  # Uses cache
        5000
    """
    cache = {}

    def memoized_func(*args):
        cache_key = str(args)  # Simple serialization for demo

        if cache_key in cache:
            return cache[cache_key]

        result = original_func(*args)
        cache[cache_key] = result
        return result

    return memoized_func


def expensive_greeting_computation(name: str) -> str:
    """
    Simulates expensive greeting computation.

    This function represents a computationally expensive
    operation that benefits from memoization.

    Args:
        name: User name to process.

    Returns:
        Greeting with simulated processing metadata.
    """
    # Simulate expensive operation
    processed_name = name.upper() * 1000
    return f"Welcome, {name}! (Processed: {len(processed_name)} characters)"


# Create memoized version
memoized_greeting = create_memoized_function(expensive_greeting_computation)


# Solution 9: Functional input sanitization pipeline
def create_sanitization_pipeline(*sanitizers: Callable[[str], str]) -> Callable[[str], str]:
    """
    Creates pipeline of sanitization functions.

    Higher-order function that composes multiple sanitization
    steps into a single pipeline function.

    Args:
        *sanitizers: Sanitization functions to compose.

    Returns:
        Composed sanitization function.

    Examples:
        >>> pipeline = create_sanitization_pipeline(str.strip, str.title)
        >>> pipeline("  hello world  ")
        'Hello World'
    """
    def apply_sanitization(accumulator: str, sanitizer_func: Callable[[str], str]) -> str:
        return sanitizer_func(accumulator)

    def sanitization_pipeline(text: str) -> str:
        return reduce(apply_sanitization, sanitizers, text)

    return sanitization_pipeline


def remove_html_tags(text: str) -> str:
    """
    Removes HTML tags from text.

    Pure function for HTML sanitization.

    Args:
        text: Input text that may contain HTML.

    Returns:
        Text with HTML tags removed.
    """
    return re.sub(r'<[^>]+>', '', text)


def remove_extra_spaces(text: str) -> str:
    """
    Normalizes whitespace in text.

    Replaces multiple whitespace characters with single spaces
    and trims leading/trailing spaces.

    Args:
        text: Text with potential extra whitespace.

    Returns:
        Text with normalized whitespace.
    """
    return re.sub(r'\s+', ' ', text).strip()


def limit_text_length(text: str, max_length: int = 50) -> str:
    """
    Limits text to maximum length.

    Pure function for enforcing length constraints.

    Args:
        text: Text to truncate if needed.
        max_length: Maximum allowed length.

    Returns:
        Text truncated to max_length if necessary.
    """
    return text[:max_length]


# Create composed sanitization function
def create_default_sanitizer(max_length: int = 50) -> Callable[[str], str]:
    """
    Creates default sanitization pipeline.

    Configurable sanitizer that combines multiple sanitization steps.

    Args:
        max_length: Maximum length for text limiting.

    Returns:
        Composed sanitization function.
    """
    return create_sanitization_pipeline(
        remove_html_tags,
        remove_extra_spaces,
        # Simple lambda for configuration
        lambda text: limit_text_length(text, max_length)
    )


# Solution 10: Functional feature toggles
def create_feature_toggle_manager() -> Tuple[Callable[[str, bool], None], Callable[[str, Callable], Callable]]:
    """
    Creates functional feature toggle system.

    Returns functions for managing feature flags and creating
    feature-toggled functions. Demonstrates how to implement
    feature flags in functional style.

    Returns:
        Tuple of (set_feature_function, create_toggled_function)
    """
    feature_states = {}

    def set_feature_state(feature_name: str, enabled: bool) -> None:
        """
        Sets the state of a feature flag.

        Args:
            feature_name: Name of the feature to configure.
            enabled: Whether the feature is enabled.
        """
        feature_states[feature_name] = enabled

    def create_toggled_function(feature_name: str, enabled_function: Callable) -> Callable:
        """
        Creates function that respects feature toggle.

        Args:
            feature_name: Feature that controls this function.
            enabled_function: Function to call when feature is enabled.

        Returns:
            Function that calls enabled_function or returns disabled message.
        """
        def toggled_function(*args, **kwargs):
            if feature_states.get(feature_name, False):
                return enabled_function(*args, **kwargs)
            return f"Feature '{feature_name}' is disabled"

        return toggled_function

    return set_feature_state, create_toggled_function


# Demonstration functions
def demonstrate_solution_1():
    """Demonstrates Solution 1: Either Monad Validation."""
    print("Testing Either Monad Validation")
    name = input("Enter name: ")
    result = welcome_with_validation(name)
    value, error = result
    if error:
        print(f"Error: {error}")
    else:
        print(f"Greeting: {value}")


def demonstrate_solution_2():
    """Demonstrates Solution 2: Time-based Greeting."""
    print("Testing Time-based Greeting")
    name = input("Enter name: ")
    result = create_time_based_greeting(name)
    print(f"Greeting: {result}")


def demonstrate_solution_3():
    """Demonstrates Solution 3: Multi-language Support."""
    print("Testing Multi-language Support")
    name = input("Enter name: ")
    language = input(
        "Enter language (english/spanish/french/german): ").strip().lower()
    greeter = create_language_greeter(language)
    result = greeter(name)
    print(f"Greeting: {result}")


def demonstrate_solution_4():
    """Demonstrates Solution 4: Session Management."""
    print("Testing Session Management")
    add_greeting, get_state = create_session_manager()
    name = input("Enter name: ")
    state = add_greeting(name)
    print(f"Session state: {state}")


def demonstrate_solution_5():
    """Demonstrates Solution 5: Configurable Validation."""
    print("Testing Configurable Validation")
    name = input("Enter name: ")
    validator = create_configurable_validator(min_length=3, max_length=10)
    result = validator(name)
    value, error = result
    if error:
        print(f"Error: {error}")
    else:
        print(f"Greeting: {value}")


def demonstrate_solution_6():
    """Demonstrates Solution 6: Error Recovery."""
    print("Testing Error Recovery")
    name = input("Enter name (try empty or invalid): ")

    def primary(name):
        result = welcome_with_validation(name)
        return result[0] or "Validation failed"

    def fallback(name):
        return f"Fallback: Hello, {name or 'Guest'}!"

    strategy = create_fallback_strategy(primary, fallback)
    result = strategy(name)
    print(f"Result: {result}")


def demonstrate_solution_7():
    """Demonstrates Solution 7: Analytics Pipeline."""
    print("Testing Analytics Pipeline")
    names_input = input("Enter names separated by commas: ")
    names = [name.strip() for name in names_input.split(",") if name.strip()]
    pipeline = create_processing_pipeline()
    result = pipeline(names)
    print(f"Analytics: {result}")


def demonstrate_solution_8():
    """Demonstrates Solution 8: Memoization."""
    print("Testing Memoization")
    name = input("Enter name: ")
    result1 = memoized_greeting(name)
    print(f"First call: {result1}")
    result2 = memoized_greeting(name)
    print(f"Second call (cached): {result2}")


def demonstrate_solution_9():
    """Demonstrates Solution 9: Sanitization Pipeline."""
    print("Testing Sanitization Pipeline")
    text = input("Enter text (try with HTML or extra spaces): ")
    sanitizer = create_default_sanitizer()
    result = sanitizer(text)
    print(f"Sanitized: '{result}'")


def demonstrate_solution_10():
    """Demonstrates Solution 10: Feature Toggles."""
    print("Testing Feature Toggles")
    set_feature, create_toggled = create_feature_toggle_manager()

    # Configure features
    set_feature("advanced_analytics", True)
    set_feature("social_sharing", False)

    # Create toggled functions
    analytics_func = create_toggled(
        "advanced_analytics", lambda x: f"Analytics for {x}")
    social_func = create_toggled("social_sharing", lambda x: f"Shared {x}")

    name = input("Enter name: ")
    print(f"Analytics: {analytics_func(name)}")
    print(f"Social: {social_func(name)}")


def main():
    """
    Interactive demonstration of intermediate functional programming.

    Provides menu-driven access to all intermediate functional
    programming patterns and techniques.
    """
    solutions = {
        '1': ("Either Monad Validation", demonstrate_solution_1),
        '2': ("Time-based Greeting", demonstrate_solution_2),
        '3': ("Multi-language Support", demonstrate_solution_3),
        '4': ("Session Management", demonstrate_solution_4),
        '5': ("Configurable Validation", demonstrate_solution_5),
        '6': ("Error Recovery", demonstrate_solution_6),
        '7': ("Analytics Pipeline", demonstrate_solution_7),
        '8': ("Memoization", demonstrate_solution_8),
        '9': ("Sanitization Pipeline", demonstrate_solution_9),
        '10': ("Feature Toggles", demonstrate_solution_10)
    }

    print("Functional Programming - Intermediate Level")

    for key, (description, _) in solutions.items():
        print(f"{key}. {description}")

    print("\nEnter 'q' to quit.")

    while True:
        choice = input("\nChoose solution (1-10): ").strip()

        if choice.lower() == 'q':
            print("Thank you for exploring Intermediate Functional Programming!")
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

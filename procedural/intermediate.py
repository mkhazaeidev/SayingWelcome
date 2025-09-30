"""
Procedural Programming - Intermediate Level
Advanced approaches to solve the welcome message task with error handling,
validation, and additional features.

This module demonstrates intermediate procedural programming concepts
including error handling, data validation, and code organization.
"""

import re
import json
from datetime import datetime
from typing import Optional, Dict, Any


# Solution 1: Comprehensive input validation
def welcome_with_comprehensive_validation():
    """
    Advanced input validation with multiple checks.

    This solution demonstrates thorough input validation including:
    - Empty input check
    - Minimum length validation
    - Alphabetic character validation
    - Name length limits
    """
    print("=== Welcome with Comprehensive Validation ===")

    while True:
        name = input("Please enter your name: ").strip()

        # Check for empty input
        if not name:
            print("Error: Name cannot be empty. Please try again.")
            continue

        # Check minimum length
        if len(name) < 2:
            print("Error: Name must be at least 2 characters long.")
            continue

        # Check maximum length
        if len(name) > 50:
            print("Error: Name cannot exceed 50 characters.")
            continue

        # Check for alphabetic characters (allowing spaces and hyphens)
        if not re.match(r'^[A-Za-z\s\-]+$', name):
            print("Error: Name can only contain letters, spaces, and hyphens.")
            continue

        # If all checks pass
        break

    print(f"Welcome, {name.title()}!")


# Solution 2: With time-based greeting
def welcome_with_time_greeting():
    """
    Time-based personalized greeting.

    Changes the greeting message based on the time of day:
    - Morning (5:00 - 11:59)
    - Afternoon (12:00 - 17:59) 
    - Evening (18:00 - 4:59)
    """
    print("Welcome with Time-Based Greeting")

    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        time_greeting = "Good morning"
    elif 12 <= current_hour < 18:
        time_greeting = "Good afternoon"
    else:
        time_greeting = "Good evening"

    name = input("What's your name? ").strip()

    if not name:
        name = "Guest"

    print(f"{time_greeting}, {name}! We're glad to see you.")


# Solution 3: With language selection
def welcome_with_language_selection():
    """
    Multi-language welcome message.

    Allows users to choose from different languages for their greeting.
    Demonstrates dictionary usage and user preferences.
    """
    print("Welcome with Language Selection")

    languages = {
        '1': {'name': 'English', 'greeting': 'Welcome'},
        '2': {'name': 'Spanish', 'greeting': 'Bienvenido'},
        '3': {'name': 'French', 'greeting': 'Bienvenue'},
        '4': {'name': 'German', 'greeting': 'Willkommen'},
        '5': {'name': 'Italian', 'greeting': 'Benvenuto'}
    }

    print("Please select your preferred language:")
    for key, lang in languages.items():
        print(f"{key}. {lang['name']}")

    while True:
        choice = input("Enter your choice (1-5): ").strip()
        if choice in languages:
            selected_lang = languages[choice]
            break
        else:
            print("Error: Invalid choice. Please select 1-5.")

    name = input("What's your name? ").strip()
    if not name:
        name = "Friend"

    print(f"{selected_lang['greeting']}, {name}!")


# Solution 4: With user profile creation
def welcome_with_user_profile():
    """
    Create a simple user profile with additional information.

    Demonstrates collecting multiple data points and organizing them
    into a structured format (dictionary).
    """
    print("Welcome with User Profile")

    user_profile = {}

    # Get name with validation
    while True:
        name = input("Enter your full name: ").strip()
        if name and len(name) >= 2:
            user_profile['name'] = name.title()
            break
        print("Error: Please enter a valid name (at least 2 characters).")

    # Get optional email
    email = input("Enter your email (optional): ").strip()
    if email:
        if re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            user_profile['email'] = email
        else:
            print("Warning: Email format invalid. Skipping email storage.")

    # Get title/role
    title = input("What's your role/title? (optional): ").strip()
    if title:
        user_profile['title'] = title

    # Generate welcome message
    welcome_msg = f"Welcome, {user_profile['name']}"
    if 'title' in user_profile:
        welcome_msg += f" ({user_profile['title']})"
    welcome_msg += "! We're excited to have you here."

    print(welcome_msg)

    # Display profile summary
    if len(user_profile) > 1:
        print("\nProfile Summary:")
        for key, value in user_profile.items():
            print(f"\t{key.capitalize()}: {value}")


# Solution 5: With greeting history
def welcome_with_greeting_history():
    """
    Maintain a history of greetings in memory.

    Demonstrates list operations and data persistence within a session.
    Shows how to track and display historical data.
    """
    print("Welcome with Greeting History")

    greeting_history = []
    session_start = datetime.now()

    def add_to_history(user_name: str, greeting: str):
        """Add a greeting to the history with timestamp."""
        entry = {
            'name': user_name,
            'greeting': greeting,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        greeting_history.append(entry)

    while True:
        name = input(
            "\nEnter your name (or 'quit' to exit, 'history' to view): ").strip()

        if name.lower() == 'quit':
            break
        elif name.lower() == 'history':
            # Display greeting history
            if not greeting_history:
                print("No greetings recorded yet.")
            else:
                print(
                    f"\nGreeting History (Session started at {session_start.strftime('%H:%M:%S')}):")
                for i, entry in enumerate(greeting_history, 1):
                    print(
                        f"   {i}. {entry['greeting']} at {entry['timestamp']}")
            continue

        if not name:
            print("Error: Please enter a valid name.")
            continue

        # Create personalized greeting
        greeting = f"Hello, {name}! You're visitor #{len(greeting_history) + 1}"
        print(greeting)

        # Add to history
        add_to_history(name, greeting)

    print(f"\nSession Summary: {len(greeting_history)} greetings recorded.")


# Solution 6: With configuration settings
def welcome_with_configuration():
    """
    Configurable welcome system using settings.

    Demonstrates using configuration dictionaries to control
    program behavior and make code more maintainable.
    """
    print("Welcome with Configuration")

    # Configuration settings
    CONFIG = {
        'min_name_length': 2,
        'max_name_length': 30,
        'default_greeting': 'Welcome',
        'allow_numbers': False,
        'auto_title_case': True,
        'max_attempts': 3
    }

    def validate_name(name: str) -> tuple[bool, str]:
        """Validate name based on configuration."""
        if not name:
            return False, "Name cannot be empty."

        if len(name) < CONFIG['min_name_length']:
            return False, f"Name must be at least {CONFIG['min_name_length']} characters."

        if len(name) > CONFIG['max_name_length']:
            return False, f"Name cannot exceed {CONFIG['max_name_length']} characters."

        if not CONFIG['allow_numbers'] and any(char.isdigit() for char in name):
            return False, "Name cannot contain numbers."

        return True, "Valid"

    attempts = 0
    while attempts < CONFIG['max_attempts']:
        name = input("Please enter your name: ").strip()
        is_valid, message = validate_name(name)

        if is_valid:
            # Format name based on configuration
            if CONFIG['auto_title_case']:
                name = name.title()

            print(f"{CONFIG['default_greeting']}, {name}!")
            break
        else:
            attempts += 1
            print(f"Error: {message} (Attempt {attempts}/{CONFIG['max_attempts']})")

    if attempts >= CONFIG['max_attempts']:
        print("Too many failed attempts. Please try again later.")


# Solution 7: With error handling and exceptions
def welcome_with_error_handling():
    """
    Robust error handling with try-except blocks.

    Demonstrates proper exception handling for production-ready code.
    Includes handling for common input/output errors.
    """
    print("Welcome with Error Handling")

    def safe_input(prompt: str) -> Optional[str]:
        """Safely get user input with error handling."""
        try:
            return input(prompt).strip()
        except KeyboardInterrupt:
            print("\n\nError: Operation cancelled by user.")
            return None
        except EOFError:
            print("\n\nError: End of input reached.")
            return None
        except Exception as e:
            print(f"\n\nError: An unexpected error occurred: {e}")
            return None

    def validate_and_format_name(name: str) -> Optional[str]:
        """Validate and format name with error handling."""
        try:
            if not name:
                raise ValueError("Name cannot be empty.")

            if len(name) < 2:
                raise ValueError("Name must be at least 2 characters.")

            # Format the name
            formatted_name = name.title()

            return formatted_name

        except ValueError as e:
            print(f"Error: Validation error: {e}")
            return None
        except Exception as e:
            print(f"Error: Unexpected error during validation: {e}")
            return None

    # Main execution with error handling
    try:
        name = safe_input("Please enter your name: ")

        if name is None:
            return  # Exit if input was cancelled

        formatted_name = validate_and_format_name(name)

        if formatted_name:
            print(f"Welcome, {formatted_name}! We're glad you're here.")
        else:
            print("Could not process your name. Please try again.")

    except Exception as e:
        print(f"Error: A critical error occurred: {e}")


# Solution 8: With greeting templates
def welcome_with_templates():
    """
    Template-based greeting system.

    Demonstrates using templates for dynamic message generation
    and separation of content from logic.
    """
    print("Welcome with Templates")

    # Template library
    GREETING_TEMPLATES = {
        'formal': "Dear {name}, it is our distinct pleasure to welcome you.",
        'casual': "Hey {name}! Great to see you!",
        'friendly': "Hello {name}! We're so happy you're here!",
        'professional': "Welcome {name}. We look forward to working with you.",
        'enthusiastic': "WOW! {name} is here! Let's get started!"
    }

    print("Choose your greeting style:")
    for i, (key, template) in enumerate(GREETING_TEMPLATES.items(), 1):
        print(f"{i}. {key.capitalize()}")

    while True:
        try:
            choice = int(input("Enter your choice (1-5): ").strip())
            if 1 <= choice <= len(GREETING_TEMPLATES):
                selected_style = list(GREETING_TEMPLATES.keys())[choice - 1]
                break
            else:
                print("Error: Please enter a number between 1 and 5.")
        except ValueError:
            print("Error: Please enter a valid number.")

    name = input("What's your name? ").strip()
    if not name:
        name = "Guest"

    # Format name
    formatted_name = name.title()

    # Generate greeting using template
    greeting_template = GREETING_TEMPLATES[selected_style]
    final_greeting = greeting_template.format(name=formatted_name)

    print(f"\n{final_greeting}")


# Solution 9: With input sanitization
def welcome_with_sanitization():
    """
    Advanced input sanitization and security.

    Demonstrates security-conscious programming by sanitizing
    user input to prevent potential issues.
    """
    print("Welcome with Input Sanitization")

    def sanitize_input(text: str) -> str:
        """
        Sanitize user input to prevent various issues.

        Removes or escapes potentially problematic characters
        while preserving legitimate name characters.
        """
        # Remove leading/trailing whitespace
        sanitized = text.strip()

        # Remove any HTML tags
        sanitized = re.sub(r'<[^>]+>', '', sanitized)

        # Remove excessive whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized)

        # Limit length
        sanitized = sanitized[:50]

        return sanitized

    def is_safe_name(name: str) -> tuple[bool, str]:
        """Check if the name is safe to use."""
        # Check for empty name
        if not name:
            return False, "Name cannot be empty."

        # Check for minimum length
        if len(name) < 2:
            return False, "Name is too short."

        # Check for suspicious patterns
        suspicious_patterns = [
            r'.*[<>].*',  # HTML tags
            r'.*[{}].*',  # Code injection
            r'.*script.*',  # Script tags
            r'.*http.*',   # URLs
        ]

        for pattern in suspicious_patterns:
            if re.match(pattern, name, re.IGNORECASE):
                return False, "Name contains suspicious characters."

        return True, "Name is safe"

    raw_name = input("Enter your name: ")
    sanitized_name = sanitize_input(raw_name)

    is_safe, message = is_safe_name(sanitized_name)

    if is_safe:
        formatted_name = sanitized_name.title()
        print(f"Welcome, {formatted_name}! Your input has been verified.")
    else:
        print(f"Error: {message} Please enter a valid name.")


# Solution 10: With performance monitoring
def welcome_with_performance_monitoring():
    """
    Performance monitoring and benchmarking.

    Demonstrates how to measure and monitor code performance
    for optimization purposes.
    """
    print("Welcome with Performance Monitoring")

    import time

    def timed_input(prompt: str) -> tuple[Optional[str], float]:
        """Get input with timing measurement."""
        start_time = time.time()
        try:
            user_input = input(prompt).strip()
            end_time = time.time()
            return user_input, end_time - start_time
        except:
            end_time = time.time()
            return None, end_time - start_time

    def timed_validation(name: str) -> tuple[bool, float]:
        """Validate name with timing."""
        start_time = time.time()

        # Perform validation checks
        is_valid = (
            name and
            len(name) >= 2 and
            len(name) <= 50 and
            re.match(r'^[A-Za-z\s\-]+$', name)
        )

        end_time = time.time()
        return is_valid, end_time - start_time

    # Monitor total execution time
    total_start_time = time.time()

    # Get input with timing
    name, input_time = timed_input("Please enter your name: ")

    if name is None:
        print("Error: Input was cancelled.")
        return

    # Validate with timing
    is_valid, validation_time = timed_validation(name)

    if is_valid:
        # Generate greeting
        greeting_start = time.time()
        formatted_name = name.title()
        greeting = f"Welcome, {formatted_name}!"
        greeting_time = time.time() - greeting_start

        # Display results
        print(greeting)

        # Performance report
        total_time = time.time() - total_start_time
        print(f"\nPerformance Report:")
        print(f"\tInput time: {input_time:.4f} seconds")
        print(f"\tValidation time: {validation_time:.4f} seconds")
        print(f"\tGreeting generation: {greeting_time:.4f} seconds")
        print(f"\tTotal execution: {total_time:.4f} seconds")

    else:
        print("Error: Invalid name provided.")


def main():
    """
    Main function to demonstrate all intermediate solutions.

    Provides an interactive menu to test different intermediate
    implementations of the welcome message system.
    """
    solutions = {
        '1': ("Comprehensive Validation", welcome_with_comprehensive_validation),
        '2': ("Time-Based Greeting", welcome_with_time_greeting),
        '3': ("Language Selection", welcome_with_language_selection),
        '4': ("User Profile", welcome_with_user_profile),
        '5': ("Greeting History", welcome_with_greeting_history),
        '6': ("Configuration Settings", welcome_with_configuration),
        '7': ("Error Handling", welcome_with_error_handling),
        '8': ("Greeting Templates", welcome_with_templates),
        '9': ("Input Sanitization", welcome_with_sanitization),
        '10': ("Performance Monitoring", welcome_with_performance_monitoring)
    }

    print("Procedural Programming - Intermediate Level")
    print("=" * 55)
    print("Choose a solution to test (1-10):")

    for key, (description, procedure) in solutions.items():
        print(f"{key}. {description}")

    print("0. Exit")

    while True:
        choice = input("\nEnter your choice: ").strip()

        if choice == '0':
            print("Goodbye! 👋")
            break
        elif choice in solutions:
            print(f"\n🧪 Testing: {solutions[choice][0]}")
            print("-" * 40)
            try:
                procedure = solutions[choice][1]
                procedure()
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Invalid choice. Please enter 1-10 or 0 to exit.")


if __name__ == "__main__":
    main()

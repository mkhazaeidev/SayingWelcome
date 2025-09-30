"""
Procedural Programming - Beginner Level
Ten different approaches to solve the welcome message task.

This module demonstrates various simple procedural ways to get a user's name
and display a welcome message, focusing on basic Python concepts.
"""

# Solution 1: Most Basic Approach


def welcome_basic():
    """
    The simplest possible implementation.

    This solution uses basic input/output without any validation
    or additional features.
    """
    name = input("Enter your name: ")
    print("Welcome, " + name + "!")


# Solution 2: Using f-string (Python 3.6+)
def welcome_fstring():
    """
    Using f-strings for string formatting.

    F-strings provide a more readable and efficient way
    to format strings compared to concatenation.
    """
    name = input("Please enter your name: ")
    print(f"Welcome, {name}!")


# Solution 3: Using .format() method
def welcome_format():
    """
    Using the .format() method for string formatting.

    This method works in older Python versions and provides
    flexible string formatting options.
    """
    name = input("What's your name? ")
    print("Welcome, {}!".format(name))


# Solution 4: With multiple variables
def welcome_multiple_vars():
    """
    Demonstrating the use of multiple variables.

    This approach shows how to break down the problem
    into smaller, manageable parts using variables.
    """
    prompt = "Enter your name: "
    greeting_start = "Welcome, "
    greeting_end = "!"

    name = input(prompt)
    full_greeting = greeting_start + name + greeting_end
    print(full_greeting)


# Solution 5: Using % formatting (old style)
def welcome_percent_format():
    """
    Using %-formatting (old-style string formatting).

    This method is from older Python versions but is still
    supported and useful to know for maintaining legacy code.
    """
    name = input("Your name please: ")
    print("Welcome, %s!" % name)


# Solution 6: With a greeting function
def create_greeting(name):
    """
    Create a personalized greeting message.

    Args:
        name (str): The user's name

    Returns:
        str: A personalized welcome message
    """
    return f"Welcome, {name}!"


def welcome_with_function():
    """
    Separating concerns with a dedicated greeting function.

    This approach demonstrates basic function usage and
    separation of concerns in procedural programming.
    """
    name = input("Please tell me your name: ")
    message = create_greeting(name)
    print(message)


# Solution 7: With basic input validation
def welcome_with_validation():
    """
    Adding basic input validation.

    This solution ensures the user provides some input
    before proceeding with the greeting.
    """
    name = input("Enter your name: ").strip()

    if name == "":
        print("Please enter a valid name!")
        return

    print(f"Welcome, {name}!")


# Solution 8: Using a constant for the greeting
def welcome_with_constant():
    """
    Using constants for reusable values.

    This approach demonstrates the use of constants
    to make code more maintainable and readable.
    """
    GREETING_TEMPLATE = "Welcome, {}!"

    name = input("What should I call you? ")
    print(GREETING_TEMPLATE.format(name))


# Solution 9: With title case formatting
def welcome_title_case():
    """
    Formatting the name for consistent output.

    This solution demonstrates basic string manipulation
    by formatting the name in title case.
    """
    name = input("Enter your name: ").strip()
    formatted_name = name.title()
    print(f"Welcome, {formatted_name}!")


# Solution 10: Complete beginner solution with comments
def welcome_complete_beginner():
    """
    A complete beginner-friendly solution with detailed comments.

    This solution includes extensive comments to explain
    each step for absolute beginners learning Python.
    """
    # Ask the user for their name
    # input() function displays a prompt and waits for user input
    name = input("Please enter your name: ")

    # Remove any extra spaces from the beginning and end
    cleaned_name = name.strip()

    # Create the welcome message by combining strings
    welcome_message = "Welcome, " + cleaned_name + "!"

    # Display the welcome message to the user
    # print() function shows the message on the screen
    print(welcome_message)


def main():
    """
    Main function to demonstrate all solutions.

    This function provides a menu to choose and test
    different implementations of the welcome message.
    """
    solutions = {
        '1': ("Most Basic", welcome_basic),
        '2': ("F-String", welcome_fstring),
        '3': ("Format Method", welcome_format),
        '4': ("Multiple Variables", welcome_multiple_vars),
        '5': ("Percent Format", welcome_percent_format),
        '6': ("With Function", welcome_with_function),
        '7': ("With Validation", welcome_with_validation),
        '8': ("With Constant", welcome_with_constant),
        '9': ("Title Case", welcome_title_case),
        '10': ("Complete Beginner", welcome_complete_beginner)
    }

    print("Procedural Programming - Beginner Level")
    print("Choose a solution to test (1-10):")

    for key, (description, procedure) in solutions.items():
        print(f"{key}. {description}")

    print("0. Exit")

    while True:
        choice = input("\nEnter your choice: ").strip()

        if choice == '0':
            print("Goodbye!")
            break
        elif choice in solutions:
            print(f"\nTesting: {solutions[choice][0]}")
            try:
                procedure = solutions[choice][1]
                procedure()
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                break
            except Exception as error:
                print(f"An error occurred: {error}")
        else:
            print("Invalid choice. Please enter 1-10 or 0 to exit.")


if __name__ == "__main__":
    main()

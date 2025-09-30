"""
Procedural Programming - Advanced Level
Enterprise-grade procedural solutions for the welcome message task.

This module demonstrates professional procedural programming concepts including:
configuration management, logging, context managers, decorators, and modular design
without using classes or object-oriented programming.
"""

import asyncio
import json
import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Generator
import configparser
import hashlib
import re


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('welcome_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Global configuration constants
GREETING_STYLES = {
    'formal': "Dear {name}, it is our distinct pleasure to welcome you to our system.",
    'casual': "Hey {name}! Awesome to have you here!",
    'professional': "Welcome {name}. We look forward to our professional collaboration.",
    'enthusiastic': "WOW! {name} is here! Let's create something amazing together!"
}

DEFAULT_CONFIG = {
    'VALIDATION': {
        'min_name_length': '2',
        'max_name_length': '50',
        'allow_numbers': 'false',
        'max_attempts': '3'
    },
    'DATABASE': {
        'enabled': 'true',
        'file_path': 'welcome_system.db'
    },
    'LOGGING': {
        'level': 'INFO',
        'file_enabled': 'true'
    },
    'SECURITY': {
        'hash_names': 'false',
        'sanitize_input': 'true'
    }
}


def performance_monitor(func):
    """Decorator to monitor function performance."""
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        logger.info(f"Starting {func.__name__}")

        try:
            result = func(*args, **kwargs)
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.info(
                f"Completed {func.__name__} in {execution_time:.4f} seconds")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise

    return wrapper


def load_config(config_file: str = "welcome_config.ini") -> configparser.ConfigParser:
    """
    Load configuration from file or create default.

    Args:
        config_file: Path to configuration file

    Returns:
        ConfigParser object with loaded configuration
    """
    config = configparser.ConfigParser()
    config_path = Path(config_file)

    if config_path.exists():
        config.read(config_path)
    else:
        # Create default configuration
        for section, settings in DEFAULT_CONFIG.items():
            config[section] = settings
        save_config(config, config_file)

    return config


def save_config(config: configparser.ConfigParser, config_file: str) -> None:
    """
    Save configuration to file.

    Args:
        config: ConfigParser object
        config_file: Path to configuration file
    """
    with open(config_file, 'w') as f:
        config.write(f)


def update_config_setting(config: configparser.ConfigParser, section: str,
                          key: str, value: str, config_file: str) -> None:
    """
    Update a configuration setting and save to file.

    Args:
        config: ConfigParser object
        section: Configuration section
        key: Setting key
        value: New value
        config_file: Path to configuration file
    """
    if section not in config:
        config[section] = {}
    config[section][key] = value
    save_config(config, config_file)


def get_validation_rules(config: configparser.ConfigParser) -> Dict[str, Any]:
    """
    Get validation rules from configuration.

    Args:
        config: ConfigParser object

    Returns:
        Dictionary of validation rules
    """
    return {
        'min_name_length': config.getint('VALIDATION', 'min_name_length'),
        'max_name_length': config.getint('VALIDATION', 'max_name_length'),
        'allow_numbers': config.getboolean('VALIDATION', 'allow_numbers'),
        'max_attempts': config.getint('VALIDATION', 'max_attempts')
    }


@contextmanager
def database_connection(db_path: str) -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager for database connections.

    Args:
        db_path: Path to SQLite database file

    Yields:
        SQLite connection object
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def initialize_database(db_path: str) -> None:
    """
    Initialize database tables.

    Args:
        db_path: Path to SQLite database file
    """
    with database_connection(db_path) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS user_greetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_hash TEXT,
                greeting_style TEXT NOT NULL,
                greeting_message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS greeting_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                greeting_count INTEGER DEFAULT 0,
                unique_users INTEGER DEFAULT 0
            )
        ''')


def store_greeting(db_path: str, name: str, greeting_style: str,
                   greeting_message: str, hash_names: bool = False) -> None:
    """
    Store a greeting in the database.

    Args:
        db_path: Path to SQLite database file
        name: User's name
        greeting_style: Style of greeting used
        greeting_message: The generated greeting message
        hash_names: Whether to hash names for privacy
    """
    name_hash = hashlib.sha256(
        name.encode()).hexdigest() if hash_names and name else None

    with database_connection(db_path) as conn:
        conn.execute('''
            INSERT INTO user_greetings (name, name_hash, greeting_style, greeting_message)
            VALUES (?, ?, ?, ?)
        ''', (name, name_hash, greeting_style, greeting_message))

        # Update analytics
        today = datetime.now().date().isoformat()
        conn.execute('''
            INSERT OR REPLACE INTO greeting_analytics (date, greeting_count, unique_users)
            VALUES (?, 
                COALESCE((SELECT greeting_count FROM greeting_analytics WHERE date = ?), 0) + 1,
                COALESCE((SELECT unique_users FROM greeting_analytics WHERE date = ?), 0) + 
                CASE WHEN (SELECT COUNT(*) FROM user_greetings WHERE name_hash = ? AND DATE(created_at) = ?) = 1 THEN 1 ELSE 0 END
            )
        ''', (today, today, today, name_hash, today))


def get_greeting_stats(db_path: str) -> Dict[str, Any]:
    """
    Get greeting statistics from database.

    Args:
        db_path: Path to SQLite database file

    Returns:
        Dictionary with greeting statistics
    """
    with database_connection(db_path) as conn:
        total_greetings = conn.execute(
            'SELECT COUNT(*) as count FROM user_greetings').fetchone()['count']
        unique_users = conn.execute(
            'SELECT COUNT(DISTINCT name_hash) as count FROM user_greetings').fetchone()['count']
        today_count = conn.execute('''
            SELECT greeting_count FROM greeting_analytics WHERE date = ?
        ''', (datetime.now().date().isoformat(),)).fetchone()

        return {
            'total_greetings': total_greetings,
            'unique_users': unique_users,
            'today_greetings': today_count['greeting_count'] if today_count else 0
        }


def sanitize_input(raw_input: str, allow_numbers: bool = False) -> tuple[bool, Optional[str], Optional[str]]:
    """
    Sanitize and validate user input.

    Args:
        raw_input: Raw user input
        allow_numbers: Whether to allow numbers in names

    Returns:
        Tuple: (is_valid, sanitized_input, error_message)
    """
    if not raw_input:
        return False, None, "Input cannot be empty"

    # Basic sanitization
    sanitized = raw_input.strip()
    sanitized = ' '.join(sanitized.split())  # Remove extra whitespace

    # Length validation
    if len(sanitized) < 2:
        return False, None, "Name must be at least 2 characters"

    if len(sanitized) > 50:
        return False, None, "Name cannot exceed 50 characters"

    # Character validation
    if not allow_numbers and any(c.isdigit() for c in sanitized):
        return False, None, "Name cannot contain numbers"

    # Security checks
    if contains_suspicious_patterns(sanitized):
        return False, None, "Name contains suspicious patterns"

    # Format name
    formatted_name = sanitized.title()

    return True, formatted_name, None


def contains_suspicious_patterns(text: str) -> bool:
    """
    Check for potentially malicious patterns.

    Args:
        text: Text to check

    Returns:
        True if suspicious patterns are found
    """
    suspicious_patterns = [
        r'<script.*?>.*?</script>',
        r'[{}]|\.\./',  # Code injection and path traversal
        r'(union|select|insert|delete|drop|update).*',  # SQL injection patterns
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def generate_greeting(name: str, style: str = 'casual',
                      include_timestamp: bool = False) -> str:
    """
    Generate a personalized greeting message.

    Args:
        name: User's name
        style: Greeting style
        include_timestamp: Whether to include timestamp

    Returns:
        Generated greeting message
    """
    template = GREETING_STYLES.get(style, GREETING_STYLES['casual'])
    greeting = template.format(name=name)

    if include_timestamp:
        time_str = datetime.now().strftime("%H:%M")
        greeting += f" (Registered at {time_str})"

    return greeting


# Solution 1: Enterprise Welcome System
@performance_monitor
def enterprise_welcome_system():
    """
    Complete enterprise-grade welcome system using pure procedural programming.

    Integrates configuration management, database storage,
    advanced validation, and comprehensive logging without OOP.
    """
    logger.info("Starting enterprise welcome system")

    # Initialize system components
    config = load_config()
    db_path = config['DATABASE']['file_path']
    validation_rules = get_validation_rules(config)

    # Initialize database
    initialize_database(db_path)

    print("Enterprise Welcome System")
    print("Type 'stats' to view statistics or 'config' to view settings")

    attempts = 0
    max_attempts = validation_rules['max_attempts']

    while attempts < max_attempts:
        user_input = input("\nEnter your name: ").strip()

        # Handle special commands
        if user_input.lower() == 'stats':
            stats = get_greeting_stats(db_path)
            print(f"\nSystem Statistics:")
            print(f"\tTotal Greetings: {stats['total_greetings']}")
            print(f"\tUnique Users: {stats['unique_users']}")
            print(f"\tToday's Greetings: {stats['today_greetings']}")
            continue
        elif user_input.lower() == 'config':
            rules = get_validation_rules(config)
            print(f"\nSystem Configuration:")
            for key, value in rules.items():
                print(f"\t{key}: {value}")
            continue

        # Process user input
        is_valid, sanitized_name, error_message = sanitize_input(
            user_input, validation_rules['allow_numbers']
        )

        if not is_valid:
            attempts += 1
            print(f"Error: {error_message} (Attempt {attempts}/{max_attempts})")
            logger.warning(f"Validation failed: {error_message}")
            continue

        # Generate greeting
        greeting_message = generate_greeting(sanitized_name, 'casual', True)

        # Store in database
        if config.getboolean('DATABASE', 'enabled'):
            store_greeting(
                db_path,
                sanitized_name,
                'casual',
                greeting_message,
                config.getboolean('SECURITY', 'hash_names')
            )

        # Display greeting
        print(f"\n{greeting_message}")
        logger.info(f"Greeting generated for user: {sanitized_name}")
        break
    else:
        print("Maximum attempts reached. Please try again later.")
        logger.error("Maximum validation attempts reached")


# Solution 2: Async Welcome System
async def async_welcome_system():
    """
    Asynchronous welcome system demonstrating async/await patterns.

    Simulates multiple concurrent welcome operations using
    pure procedural programming with async/await.
    """
    print("Async Welcome System")

    async def simulate_network_request(name: str, delay: float) -> str:
        """Simulate network delay for greeting generation."""
        print(f"Processing greeting for {name}...")
        await asyncio.sleep(delay)  # Simulate network/DB call
        return f"Hello, {name}! (processed in {delay}s)"

    # Simulate multiple concurrent greetings
    names = ["Alice", "Bob", "Charlie", "Diana"]
    delays = [1.0, 0.5, 2.0, 0.3]

    tasks = [
        simulate_network_request(name, delay)
        for name, delay in zip(names, delays)
    ]

    print("Starting concurrent greeting processing...")
    results = await asyncio.gather(*tasks, return_exceptions=True)

    print("\nGreeting Results:")
    for name, result in zip(names, results):
        if isinstance(result, Exception):
            print(f"Error processing {name}: {result}")
        else:
            print(result)


# Solution 3: Context Manager for Session Management
@contextmanager
def welcome_session(session_name: str) -> Generator[Dict[str, Any], None, None]:
    """
    Context manager for welcome session management.

    Provides session-based resource management and
    automatic cleanup of session resources.
    """
    session_data = {
        'name': session_name,
        'start_time': datetime.now(),
        'greeting_count': 0,
        'users': []
    }

    logger.info(f"Starting welcome session: {session_name}")

    try:
        yield session_data
    except Exception as error:
        logger.error(f"Session {session_name} error: {error}")
        raise
    finally:
        session_data['end_time'] = datetime.now()
        duration = session_data['end_time'] - session_data['start_time']
        logger.info(
            f"Session {session_name} completed. Duration: {duration.total_seconds():.2f}s")
        print(f"\nSession Summary:")
        print(f"\tSession: {session_data['name']}")
        print(f"\tGreetings: {session_data['greeting_count']}")
        print(f"\tDuration: {duration.total_seconds():.2f} seconds")


def session_based_welcome():
    """Welcome system with session management using context manager."""
    print("Session-Based Welcome System")

    with welcome_session("Main Welcome Session") as session:
        while True:
            name = input("\nEnter name (or 'quit' to end session): ").strip()

            if name.lower() == 'quit':
                break

            if not name:
                print("Error: Please enter a valid name")
                continue

            # Process greeting
            greeting = f"Welcome, {name.title()}!"
            print(greeting)

            # Update session data
            session['greeting_count'] += 1
            session['users'].append(name)


# Solution 4: Plugin-based Greeting System using functions
def get_formal_greeting(name: str) -> str:
    """Generate formal greeting."""
    return f"Dear {name}, it is our pleasure to welcome you."


def get_casual_greeting(name: str) -> str:
    """Generate casual greeting."""
    return f"Hey {name}! Great to see you!"


def get_professional_greeting(name: str) -> str:
    """Generate professional greeting."""
    return f"Welcome {name}. We look forward to working with you."


def get_enthusiastic_greeting(name: str) -> str:
    """Generate enthusiastic greeting."""
    return f"WOW! {name} is here! Let's get started!"


# Plugin registry as a dictionary of functions
GREETING_PLUGINS = {
    'formal': get_formal_greeting,
    'casual': get_casual_greeting,
    'professional': get_professional_greeting,
    'enthusiastic': get_enthusiastic_greeting
}


def get_available_greeting_styles() -> List[str]:
    """Get list of available greeting styles."""
    return list(GREETING_PLUGINS.keys())


def welcome_user_with_plugin(name: str, style: str = 'casual') -> str:
    """
    Generate welcome message using selected plugin function.

    Args:
        name: User's name
        style: Greeting style

    Returns:
        Generated greeting message
    """
    plugin_func = GREETING_PLUGINS.get(style, GREETING_PLUGINS['casual'])
    return plugin_func(name)


def plugin_based_welcome():
    """Demonstrate plugin-based welcome system using functions."""
    print("Plugin-Based Welcome System")

    print("Available greeting styles:", ", ".join(
        get_available_greeting_styles()))

    name = input("Enter your name: ").strip()
    if not name:
        print("Error: Invalid name")
        return

    style = input("Choose greeting style (default: casual): ").strip().lower()
    if not style:
        style = 'casual'

    greeting = welcome_user_with_plugin(name.title(), style)
    print(f"\n{greeting}")


# Solution 5: Advanced Analytics and Reporting
def analytics_dashboard():
    """Display advanced analytics and reporting."""
    print("Welcome System Analytics Dashboard")

    config = load_config()
    db_path = config['DATABASE']['file_path']

    stats = get_greeting_stats(db_path)

    print("\nComprehensive Analytics:")
    print(f"\tTotal Greetings: {stats['total_greetings']:,}")
    print(f"\tUnique Users: {stats['unique_users']:,}")
    print(f"\tToday's Activity: {stats['today_greetings']:,}")

    # Calculate additional metrics
    if stats['unique_users'] > 0:
        avg_greetings = stats['total_greetings'] / stats['unique_users']
        print(f"\tAvg Greetings per User: {avg_greetings:.2f}")

    # Style usage analytics (simulated)
    print(f"\nGreeting Style Usage:")
    styles = ['casual', 'formal', 'professional', 'enthusiastic']
    for style in styles:
        count = len([s for s in styles if s == style])  # Simulated count
        print(f"\t{style.title()}: {count * 25}%")


# Solution 6: Configuration Management Interface
def configuration_interface():
    """Interactive configuration management interface."""
    print("Configuration Management Interface")

    config_file = "welcome_config.ini"
    config = load_config(config_file)

    while True:
        print(f"\nCurrent Configuration:")
        sections = ['VALIDATION', 'DATABASE', 'LOGGING', 'SECURITY']

        for section in sections:
            print(f"\n[{section}]")
            for key, value in config[section].items():
                print(f"\t{key} = {value}")

        print(f"\nOptions:")
        print("1. Update setting")
        print("2. Reset to defaults")
        print("3. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == '1':
            section = input("Enter section: ").strip()
            key = input("Enter key: ").strip()
            value = input("Enter new value: ").strip()

            if section in sections and key in config[section]:
                update_config_setting(config, section, key, value, config_file)
                print("Setting updated successfully")
            else:
                print("Error: Invalid section or key")

        elif choice == '2':
            for section, settings in DEFAULT_CONFIG.items():
                config[section] = settings
            save_config(config, config_file)
            print("Configuration reset to defaults")

        elif choice == '3':
            break

        else:
            print("Error: Invalid option")


# Solution 7: Batch Processing System
def batch_welcome_processing():
    """Process multiple welcome requests in batch."""
    print("Batch Welcome Processing")

    # Simulate batch data (in real scenario, this could be from file/DB)
    batch_data = [
        "Alice Johnson", "Bob Smith", "Charlie Brown",
        "Diana Prince", "", "Eve Wilson123"  # Includes invalid entries
    ]

    config = load_config()
    validation_rules = get_validation_rules(config)

    successful_greetings = 0
    failed_entries = 0

    print(f"Processing {len(batch_data)} entries...\n")

    for index, raw_name in enumerate(batch_data, 1):
        is_valid, sanitized_name, error_message = sanitize_input(
            raw_name, validation_rules['allow_numbers']
        )

        if is_valid and sanitized_name:
            greeting = generate_greeting(sanitized_name)
            print(f"{index:2d}. {greeting}")
            successful_greetings += 1
        else:
            print(f"Error {index:2d}. SKIPPED: {raw_name or 'Empty'} - {error_message}")
            failed_entries += 1

    print(f"\nBatch Processing Complete:")
    print(f"\tSuccessful: {successful_greetings}")
    print(f"\tFailed: {failed_entries}")
    print(
        f"\tSuccess Rate: {(successful_greetings/len(batch_data))*100:.1f}%")


# Solution 8: Advanced Error Recovery System
def error_resilient_welcome_system():
    """Welcome system with advanced error recovery mechanisms."""
    print("Error-Resilient Welcome System")

    config = load_config()
    validation_rules = get_validation_rules(config)

    def fallback_greeting(name: str) -> str:
        """Fallback greeting when main system fails."""
        return f"Hello, {name}! (Fallback Mode)"

    attempts = 0
    max_attempts = 2

    while attempts < max_attempts:
        try:
            name = input("Enter your name: ").strip()

            if not name:
                raise ValueError("Name cannot be empty")

            # Simulate potential failure points
            if attempts == 0 and "error" in name.lower():
                raise ConnectionError("Simulated database connection error")

            # Input validation
            is_valid, sanitized_name, error_message = sanitize_input(
                name, validation_rules['allow_numbers']
            )

            if not is_valid:
                raise ValueError(error_message)

            # Main greeting generation
            greeting = generate_greeting(sanitized_name, 'casual', True)

            print(greeting)
            break

        except (ValueError, ConnectionError) as errr:
            attempts += 1
            logger.warning(f"Attempt {attempts} failed: {errr}")

            if attempts < max_attempts:
                print(f"Warning:  {errr}. Retrying...")
            else:
                print("🔧 Switching to fallback mode...")
                fallback = fallback_greeting(name if name else "Guest")
                print(fallback)

        except Exception as errr:
            logger.error(f"Unexpected error: {errr}")
            print("💥 An unexpected error occurred. Please contact support.")
            break


# Solution 9: Multi-format Output System
def multi_format_welcome_system():
    """Welcome system with multiple output formats."""
    print("Multi-Format Welcome System")

    name = input("Enter your name: ").strip()
    if not name:
        print("Error: Invalid name")
        return

    print("\nAvailable output formats:")
    formats = ['console', 'json', 'xml', 'html']
    for index, format in enumerate(formats, 1):
        print(f"{index}. {format.upper()}")

    choice = input("Select format: ").strip()

    try:
        format_choice = formats[int(
            choice) - 1] if choice.isdigit() and 1 <= int(choice) <= len(formats) else 'console'
    except (ValueError, IndexError):
        format_choice = 'console'

    greeting_data = {
        'name': name.title(),
        'greeting': f"Welcome, {name.title()}!",
        'timestamp': datetime.now().isoformat(),
        'system': 'Advanced Welcome System'
    }

    if format_choice == 'console':
        print(f"\n{greeting_data['greeting']}")

    elif format_choice == 'json':
        import json
        print(f"\nJSON Output:\n{json.dumps(greeting_data, indent=2)}")

    elif format_choice == 'xml':
        xml_output = f"""<?xml version="1.0" encoding="UTF-8"?>
<greeting>
    <name>{greeting_data['name']}</name>
    <message>{greeting_data['greeting']}</message>
    <timestamp>{greeting_data['timestamp']}</timestamp>
    <system>{greeting_data['system']}</system>
</greeting>"""
        print(f"\nXML Output:\n{xml_output}")

    elif format_choice == 'html':
        html_output = f"""<!DOCTYPE html>
<html>
<head>
    <title>Welcome Message</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        .greeting {{ color: #2c3e50; font-size: 24px; }}
        .info {{ color: #7f8c8d; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="greeting">{greeting_data['greeting']}</div>
    <div class="info">Generated at {greeting_data['timestamp']} by {greeting_data['system']}</div>
</body>
</html>"""
        print(f"\nHTML Output:\n{html_output}")


# Solution 10: Feature Toggle System using global variables
# Feature flags stored in global dictionary
FEATURE_FLAGS = {
    'advanced_analytics': True,
    'multi_language': False,
    'social_sharing': False,
    'personalized_recommendations': True
}


def is_feature_enabled(feature: str) -> bool:
    """Check if a feature is enabled."""
    return FEATURE_FLAGS.get(feature, False)


def enable_feature(feature: str) -> None:
    """Enable a feature."""
    FEATURE_FLAGS[feature] = True
    logger.info(f"Feature enabled: {feature}")


def disable_feature(feature: str) -> None:
    """Disable a feature."""
    FEATURE_FLAGS[feature] = False
    logger.info(f"Feature disabled: {feature}")


def feature_toggle_welcome_system():
    """Welcome system with feature toggles."""
    print("Feature Toggle Welcome System")

    name = input("Enter your name: ").strip()
    if not name:
        print("Error: Invalid name")
        return

    base_greeting = generate_greeting(name.title())

    # Apply feature toggles
    final_greeting = base_greeting

    print(f"\n{final_greeting}")

    # Show active features
    active_features = [f for f, enabled in FEATURE_FLAGS.items() if enabled]
    if active_features:
        print(f"\nActive Features: {', '.join(active_features)}")


def main():
    """Main function to demonstrate all advanced procedural solutions."""
    solutions = {
        '1': ("Enterprise System", enterprise_welcome_system),
        '2': ("Async System", lambda: asyncio.run(async_welcome_system())),
        '3': ("Session Management", session_based_welcome),
        '4': ("Plugin Architecture", plugin_based_welcome),
        '5': ("Analytics Dashboard", analytics_dashboard),
        '6': ("Configuration Interface", configuration_interface),
        '7': ("Batch Processing", batch_welcome_processing),
        '8': ("Error Recovery", error_resilient_welcome_system),
        '9': ("Multi-Format Output", multi_format_welcome_system),
        '10': ("Feature Toggles", feature_toggle_welcome_system)
    }

    print("Procedural Programming - Advanced Level")
    print("Choose a solution to test (1-10):")

    for key, (description, _) in solutions.items():
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
            except Exception as e:
                print(f"An error occurred: {e}")
                logger.error(f"Error in {solutions[choice][0]}: {e}")
        else:
            print("Invalid choice. Please enter 1-10 or 0 to exit.")


if __name__ == "__main__":
    main()

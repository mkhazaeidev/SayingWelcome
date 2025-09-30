"""
Object-Oriented Programming - Beginner Level
Fundamental OOP Concepts for Welcome Message System

This module demonstrates basic object-oriented programming principles
through simple class-based implementations. Each solution showcases
essential OOP concepts suitable for beginners learning class-based
programming in Python.

Key OOP Concepts Demonstrated:
- Class definition and object instantiation
- Encapsulation with instance attributes and methods
- Constructors and instance initialization
- Basic method design and responsibility assignment
- Object state management
- Simple inheritance and polymorphism

All implementations follow OOP principles:
- Everything is an object with state and behavior
- Clear separation of concerns through classes
- Encapsulation of data and operations
- Object-based problem decomposition

Author: OOP Education Project
Version: 1.0
Date: 2025
"""


class BasicWelcome:
    """
    A simple class that demonstrates basic OOP principles.
    
    This class encapsulates the welcome message functionality
    within a single object that maintains its own state and
    provides methods to interact with that state.
    
    Attributes:
        default_greeting (str): The default greeting template used
                               when no custom greeting is provided.
        usage_count (int): Tracks how many times welcome messages
                          have been created.
    
    Example:
        >>> welcome = BasicWelcome()
        >>> message = welcome.welcome_user("Alice")
        >>> print(message)
        Welcome, Alice!
    """
    
    def __init__(self):
        """
        Initialize the BasicWelcome object with default values.
        
        The constructor sets up the initial state of the object.
        This is where we define instance attributes that represent
        the object's data.
        """
        self.default_greeting = "Welcome, {}!"
        self.usage_count = 0
    
    def welcome_user(self, name: str) -> str:
        """
        Create a welcome message for the given user.
        
        This method demonstrates the fundamental OOP concept of
        combining data (name) with behavior (message creation).
        The method also maintains object state by tracking usage.
        
        Args:
            name (str): The name of the user to welcome.
            
        Returns:
            str: A personalized welcome message.
            
        Example:
            >>> welcome = BasicWelcome()
            >>> welcome.welcome_user("Bob")
            'Welcome, Bob!'
        """
        self.usage_count += 1
        return self.default_greeting.format(name)


class PersonalizedWelcome:
    """
    A welcome class that allows for personalized greeting styles.
    
    This class demonstrates how objects can maintain configuration
    state and use it to customize their behavior. It shows the
    power of encapsulation by hiding the greeting style logic
    within the object.
    
    Attributes:
        greeting_style (str): The style of greeting to use.
        available_styles (dict): Mapping of style names to templates.
    """
    
    def __init__(self, style: str = "formal"):
        """
        Initialize with a specific greeting style.
        
        The constructor allows customization of object behavior
        through parameters, demonstrating how objects can be
        configured at creation time.
        
        Args:
            style (str): The greeting style to use. Defaults to "formal".
        """
        self.greeting_style = style
        self.available_styles = {
            "formal": "Dear {}, we are pleased to welcome you.",
            "casual": "Hey {}! Great to see you!",
            "friendly": "Hello {}! We're so happy you're here!",
            "professional": "Welcome {}. We look forward to working with you."
        }
    
    def welcome_user(self, name: str) -> str:
        """
        Create a personalized welcome based on the configured style.
        
        This method demonstrates how objects can use their internal
        state to modify their behavior. The greeting logic is
        encapsulated within the object.
        
        Args:
            name (str): The name of the user to welcome.
            
        Returns:
            str: A style-specific welcome message.
            
        Raises:
            ValueError: If the configured style is not available.
        """
        if self.greeting_style not in self.available_styles:
            raise ValueError(f"Unknown greeting style: {self.greeting_style}")
        
        template = self.available_styles[self.greeting_style]
        return template.format(name)


class WelcomeWithValidation:
    """
    A welcome class that includes input validation.
    
    This class demonstrates how objects can enforce business rules
    and maintain data integrity through validation methods.
    It shows the OOP principle of objects being responsible for
    their own data validation.
    
    Attributes:
        min_name_length (int): Minimum allowed name length.
        max_name_length (int): Maximum allowed name length.
    """
    
    def __init__(self, min_length: int = 2, max_length: int = 50):
        """
        Initialize with validation parameters.
        
        Args:
            min_length (int): Minimum valid name length.
            max_length (int): Maximum valid name length.
        """
        self.min_name_length = min_length
        self.max_name_length = max_length
    
    def validate_name(self, name: str) -> bool:
        """
        Validate if a name meets the criteria.
        
        This method demonstrates how objects can encapsulate
        validation logic, keeping the rules closely tied to
        the data they validate.
        
        Args:
            name (str): The name to validate.
            
        Returns:
            bool: True if the name is valid, False otherwise.
        """
        if not name or not isinstance(name, str):
            return False
        
        clean_name = name.strip()
        return (self.min_name_length <= len(clean_name) <= self.max_name_length)
    
    def welcome_user(self, name: str) -> str:
        """
        Create a welcome message only if the name is valid.
        
        This method shows how objects can combine multiple
        responsibilities (validation and message creation)
        while maintaining clean separation of concerns.
        
        Args:
            name (str): The name to welcome.
            
        Returns:
            str: Welcome message or error indication.
        """
        if not self.validate_name(name):
            return "Please provide a valid name"
        
        clean_name = name.strip().title()
        return f"Welcome, {clean_name}!"


class WelcomeCounter:
    """
    A welcome class that tracks usage statistics.
    
    This class demonstrates how objects can maintain and
    provide access to internal state statistics. It shows
    the OOP concept of objects having memory of their usage.
    
    Attributes:
        total_welcomes (int): Total number of welcomes performed.
        user_welcomes (dict): Count of welcomes per user.
    """
    
    def __init__(self):
        """Initialize with empty statistics."""
        self.total_welcomes = 0
        self.user_welcomes = {}
    
    def welcome_user(self, name: str) -> str:
        """
        Welcome a user and update usage statistics.
        
        This method demonstrates how objects can maintain
        complex internal state and update it as part of
        their operations.
        
        Args:
            name (str): The name of the user to welcome.
            
        Returns:
            str: Personalized welcome message.
        """
        clean_name = name.strip().title()
        
        # Update statistics
        self.total_welcomes += 1
        self.user_welcomes[clean_name] = self.user_welcomes.get(clean_name, 0) + 1
        
        user_count = self.user_welcomes[clean_name]
        return f"Welcome, {clean_name}! (Welcome #{user_count} for you)"


class ConfigurableWelcome:
    """
    A highly configurable welcome class.
    
    This class demonstrates how objects can be designed for
    flexibility through configuration options. It shows the
    OOP principle of designing objects that are open for
    extension but closed for modification.
    
    Attributes:
        template (str): The greeting template to use.
        auto_title_case (bool): Whether to automatically title-case names.
        include_count (bool): Whether to include welcome counts.
    """
    
    def __init__(self, template: str = None, auto_title_case: bool = True, 
                 include_count: bool = False):
        """
        Initialize with configuration options.
        
        Args:
            template (str): Custom greeting template with {} placeholder.
            auto_title_case (bool): Auto-convert names to title case.
            include_count (bool): Include welcome count in message.
        """
        self.template = template or "Welcome, {}!"
        self.auto_title_case = auto_title_case
        self.include_count = include_count
        self._welcome_count = 0
    
    def welcome_user(self, name: str) -> str:
        """
        Create a welcome message using the configured options.
        
        This method demonstrates how objects can use their
        configuration state to provide flexible behavior
        without changing the method signature.
        
        Args:
            name (str): The name to welcome.
            
        Returns:
            str: Configured welcome message.
        """
        self._welcome_count += 1
        
        # Process name based on configuration
        processed_name = name.strip()
        if self.auto_title_case:
            processed_name = processed_name.title()
        
        # Create base message
        message = self.template.format(processed_name)
        
        # Add count if configured
        if self.include_count:
            message += f" [Total: {self._welcome_count}]"
        
        return message


class WelcomeFactory:
    """
    A factory class for creating different types of welcome objects.
    
    This class demonstrates the Factory Pattern, a fundamental
    OOP design pattern for creating objects without specifying
    the exact class of object that will be created.
    
    Attributes:
        registry (dict): Mapping of welcome types to their classes.
    """
    
    def __init__(self):
        """Initialize with available welcome types."""
        self.registry = {
            "basic": BasicWelcome,
            "personalized": PersonalizedWelcome,
            "validated": WelcomeWithValidation,
            "counter": WelcomeCounter,
            "configurable": ConfigurableWelcome
        }
    
    def create_welcome(self, welcome_type: str, **kwargs):
        """
        Create a welcome object of the specified type.
        
        This method demonstrates the Factory Method pattern,
        where object creation is centralized and can be
        customized based on parameters.
        
        Args:
            welcome_type (str): Type of welcome object to create.
            **kwargs: Additional arguments for the welcome constructor.
            
        Returns:
            object: An instance of the requested welcome type.
            
        Raises:
            ValueError: If the welcome type is not recognized.
        """
        if welcome_type not in self.registry:
            raise ValueError(f"Unknown welcome type: {welcome_type}")
        
        welcome_class = self.registry[welcome_type]
        return welcome_class(**kwargs)


class WelcomeSystem:
    """
    A comprehensive welcome system that demonstrates basic OOP system design.
    
    This class shows how multiple objects can work together to
    provide complex functionality. It demonstrates the OOP
    principle of composing systems from collaborating objects.
    
    Attributes:
        validator (WelcomeWithValidation): Handles name validation.
        greeter (BasicWelcome): Handles message creation.
        counter (WelcomeCounter): Tracks usage statistics.
    """
    
    def __init__(self):
        """Initialize the system with component objects."""
        self.validator = WelcomeWithValidation()
        self.greeter = BasicWelcome()
        self.counter = WelcomeCounter()
        self.system_usage = 0
    
    def welcome_user(self, name: str) -> str:
        """
        Process a welcome request through the complete system.
        
        This method demonstrates how objects can collaborate
        to accomplish complex tasks, with each object handling
        a specific responsibility.
        
        Args:
            name (str): The name to welcome.
            
        Returns:
            str: The final welcome message or error.
        """
        self.system_usage += 1
        
        # Step 1: Validate input
        if not self.validator.validate_name(name):
            return "System: Invalid name provided"
        
        # Step 2: Create greeting
        greeting = self.greeter.welcome_user(name)
        
        # Step 3: Track statistics
        final_message = self.counter.welcome_user(name)
        
        return f"System: {final_message}"


class InheritedWelcome(BasicWelcome):
    """
    A specialized welcome class that demonstrates inheritance.
    
    This class shows how OOP inheritance allows extending and
    modifying behavior from a parent class. It demonstrates
    method overriding and the Liskov Substitution Principle.
    
    Attributes:
        enthusiasm_level (str): Level of enthusiasm for greetings.
    """
    
    def __init__(self, enthusiasm: str = "normal"):
        """
        Initialize the inherited welcome object.
        
        Args:
            enthusiasm (str): Enthusiasm level for greetings.
        """
        super().__init__()  # Call parent constructor
        self.enthusiasm_level = enthusiasm
        self.enthusiasm_map = {
            "low": "Hello, {}.",
            "normal": "Welcome, {}!",
            "high": "WOW! Welcome, {}!",
            "extreme": "OMG!!! WELCOME, {}!"
        }
    
    def welcome_user(self, name: str) -> str:
        """
        Create an enthusiastic welcome message.
        
        This method overrides the parent class method to
        provide specialized behavior, demonstrating
        polymorphism in action.
        
        Args:
            name (str): The name to welcome.
            
        Returns:
            str: Enthusiastic welcome message.
        """
        self.usage_count += 1
        
        template = self.enthusiasm_map.get(
            self.enthusiasm_level, 
            self.enthusiasm_map["normal"]
        )
        
        return template.format(name)


class WelcomeDecorator:
    """
    A decorator class that adds functionality to existing welcome objects.
    
    This class demonstrates the Decorator Pattern, which allows
    adding behavior to objects dynamically without affecting
    other objects of the same class.
    
    Attributes:
        wrapped_welcome: The welcome object being decorated.
    """
    
    def __init__(self, welcome_object):
        """
        Initialize with a welcome object to decorate.
        
        Args:
            welcome_object: Any object with a welcome_user method.
        """
        self.wrapped_welcome = welcome_object
        self.decoration_count = 0
    
    def welcome_user(self, name: str) -> str:
        """
        Add decorative elements to the welcome message.
        
        This method wraps the original welcome method to
        add additional behavior, demonstrating how OOP
        enables flexible composition of functionality.
        
        Args:
            name (str): The name to welcome.
            
        Returns:
            str: Decorated welcome message.
        """
        self.decoration_count += 1
        
        # Get the original message
        original_message = self.wrapped_welcome.welcome_user(name)
        
        return original_message


class MultiLingualWelcome:
    """
    A welcome class that supports multiple languages.
    
    This class demonstrates how objects can manage complex
    configuration state and use it to provide sophisticated
    behavior through clear method interfaces.
    
    Attributes:
        current_language (str): The currently active language.
        translations (dict): Greeting templates for different languages.
    """
    
    def __init__(self, language: str = "english"):
        """
        Initialize with a specific language.
        
        Args:
            language (str): The default language for greetings.
        """
        self.current_language = language
        self.translations = {
            "english": "Welcome, {}!",
            "spanish": "¡Bienvenido, {}!",
            "french": "Bienvenue, {}!",
            "german": "Willkommen, {}!",
            "italian": "Benvenuto, {}!"
        }
    
    def set_language(self, language: str) -> None:
        """
        Change the current language.
        
        This method demonstrates how objects can provide
        controlled ways to modify their state, encapsulating
        the state change logic.
        
        Args:
            language (str): The new language to use.
            
        Raises:
            ValueError: If the language is not supported.
        """
        if language not in self.translations:
            raise ValueError(f"Unsupported language: {language}")
        self.current_language = language
    
    def welcome_user(self, name: str) -> str:
        """
        Create a welcome message in the current language.
        
        Args:
            name (str): The name to welcome.
            
        Returns:
            str: Welcome message in the configured language.
        """
        template = self.translations[self.current_language]
        return template.format(name.title())


def demonstrate_oop_beginner():
    """
    Demonstrate all OOP beginner level implementations.
    
    This function showcases how to use the various welcome
    classes and demonstrates OOP principles in action.
    """
    print("Object-Oriented Programming - Beginner Level")
    
    # Demonstration 1: Basic Welcome
    print("\n1. Basic Welcome Class:")
    basic = BasicWelcome()
    print(f"   {basic.welcome_user('Alice')}")
    print(f"   Usage count: {basic.usage_count}")
    
    # Demonstration 2: Personalized Welcome
    print("\n2. Personalized Welcome:")
    casual = PersonalizedWelcome("casual")
    formal = PersonalizedWelcome("formal")
    print(f"   Casual: {casual.welcome_user('Bob')}")
    print(f"   Formal: {formal.welcome_user('Bob')}")
    
    # Demonstration 3: Validation
    print("\n3. Welcome with Validation:")
    validator = WelcomeWithValidation()
    print(f"   Valid: {validator.welcome_user('Charlie')}")
    print(f"   Invalid: {validator.welcome_user('A')}")
    
    # Demonstration 4: Counter
    print("\n4. Welcome with Counting:")
    counter = WelcomeCounter()
    print(f"   First: {counter.welcome_user('Diana')}")
    print(f"   Second: {counter.welcome_user('Diana')}")
    print(f"   Different user: {counter.welcome_user('Eve')}")
    
    # Demonstration 5: Configuration
    print("\n5. Configurable Welcome:")
    config = ConfigurableWelcome(
        template="Hello there, {}!",
        auto_title_case=True,
        include_count=True
    )
    print(f"   {config.welcome_user('frank')}")
    print(f"   {config.welcome_user('grace')}")
    
    # Demonstration 6: Factory Pattern
    print("\n6. Factory Pattern:")
    factory = WelcomeFactory()
    basic_from_factory = factory.create_welcome("basic")
    print(f"   Factory created: {basic_from_factory.welcome_user('Henry')}")
    
    # Demonstration 7: System Design
    print("\n7. Welcome System:")
    system = WelcomeSystem()
    print(f"   System: {system.welcome_user('Ivan')}")
    
    # Demonstration 8: Inheritance
    print("\n8. Inheritance:")
    enthusiastic = InheritedWelcome("high")
    print(f"   Enthusiastic: {enthusiastic.welcome_user('Jack')}")
    
    # Demonstration 9: Decorator Pattern
    print("\n9. Decorator Pattern:")
    decorated = WelcomeDecorator(basic)
    print(f"   Decorated: {decorated.welcome_user('Karen')}")
    
    # Demonstration 10: Multi-lingual
    print("\n10. Multi-lingual Welcome:")
    multi = MultiLingualWelcome("spanish")
    print(f"   Spanish: {multi.welcome_user('Luis')}")
    multi.set_language("french")
    print(f"   French: {multi.welcome_user('Marie')}")


if __name__ == "__main__":
    demonstrate_oop_beginner()

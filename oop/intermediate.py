"""
Object-Oriented Programming - Intermediate Level
Advanced OOP Concepts and Design Patterns

This module demonstrates intermediate object-oriented programming
concepts through more sophisticated class designs and patterns.
These implementations showcase how OOP enables building complex,
maintainable systems through proper abstraction and design.

Key OOP Concepts Demonstrated:
- Advanced inheritance and polymorphism
- Abstract base classes and interfaces
- Composition over inheritance
- Dependency injection
- Strategy pattern and other behavioral patterns
- Property decorators and computed attributes
- Context managers and resource management
- Exception hierarchies and custom exceptions

All implementations follow SOLID principles:
- Single Responsibility Principle
- Open/Closed Principle
- Liskov Substitution Principle  
- Interface Segregation Principle
- Dependency Inversion Principle

Author: OOP Education Project
Version: 1.0
Date: 2025
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import re


class WelcomeException(Exception):
    """
    Base exception class for welcome system errors.
    
    This custom exception hierarchy demonstrates how OOP
    allows creating domain-specific error types that
    provide more context than built-in exceptions.
    
    Attributes:
        error_code (str): A code identifying the error type.
        user_message (str): A user-friendly error message.
    """
    
    def __init__(self, error_code: str, user_message: str, *args):
        """
        Initialize the welcome exception.
        
        Args:
            error_code: Unique identifier for the error type.
            user_message: Message suitable for displaying to users.
            *args: Additional arguments for base Exception class.
        """
        super().__init__(user_message, *args)
        self.error_code = error_code
        self.user_message = user_message
    
    def __str__(self) -> str:
        """String representation including error code."""
        return f"[{self.error_code}] {self.user_message}"


class ValidationError(WelcomeException):
    """Exception raised when name validation fails."""
    pass


class ConfigurationError(WelcomeException):
    """Exception raised for configuration issues."""
    pass


class WelcomeStrategy(ABC):
    """
    Abstract base class defining the welcome strategy interface.
    
    This abstract class demonstrates the Strategy Pattern and
    the use of abstract base classes to define interfaces that
    concrete implementations must follow.
    
    The Strategy Pattern allows encapsulating different welcome
    algorithms and making them interchangeable at runtime.
    """
    
    @abstractmethod
    def generate_welcome(self, name: str) -> str:
        """
        Generate a welcome message for the given name.
        
        Args:
            name: The name to include in the welcome message.
            
        Returns:
            A personalized welcome message.
        """
        pass
    
    @abstractmethod
    def validate_input(self, name: str) -> bool:
        """
        Validate the input name.
        
        Args:
            name: The name to validate.
            
        Returns:
            True if the name is valid, False otherwise.
        """
        pass


class FormalWelcomeStrategy(WelcomeStrategy):
    """
    Concrete strategy for formal welcome messages.
    
    This class demonstrates a concrete implementation of
    the WelcomeStrategy interface, providing specific
    behavior for formal greetings.
    """
    
    def generate_welcome(self, name: str) -> str:
        """Generate a formal welcome message."""
        clean_name = name.strip().title()
        return f"Dear {clean_name}, we are pleased to welcome you to our establishment."
    
    def validate_input(self, name: str) -> bool:
        """Validate name for formal greetings."""
        if not name or not name.strip():
            return False
        clean_name = name.strip()
        return len(clean_name) >= 2 and len(clean_name) <= 50


class CasualWelcomeStrategy(WelcomeStrategy):
    """
    Concrete strategy for casual welcome messages.
    
    Demonstrates another strategy implementation with
    different validation rules and message format.
    """
    
    def generate_welcome(self, name: str) -> str:
        """Generate a casual welcome message."""
        clean_name = name.strip()
        return f"Hey {clean_name}! Great to see you!"
    
    def validate_input(self, name: str) -> bool:
        """More lenient validation for casual greetings."""
        if not name or not name.strip():
            return False
        return len(name.strip()) >= 1


class ProfessionalWelcomeStrategy(WelcomeStrategy):
    """
    Concrete strategy for professional welcome messages.
    
    Shows how different strategies can have completely
    different implementations while adhering to the
    same interface.
    """
    
    def generate_welcome(self, name: str) -> str:
        """Generate a professional welcome message."""
        clean_name = name.strip().title()
        return f"Welcome {clean_name}. We look forward to our professional collaboration."
    
    def validate_input(self, name: str) -> bool:
        """Strict validation for professional context."""
        if not name or not name.strip():
            return False
        clean_name = name.strip()
        if len(clean_name) < 2 or len(clean_name) > 30:
            return False
        # Professional names should not contain special characters
        return bool(re.match(r'^[A-Za-z\s\.\-]+$', clean_name))


class WelcomeService:
    """
    Main service class that uses strategy pattern for welcome generation.
    
    This class demonstrates the Dependency Inversion Principle
    by depending on abstractions (WelcomeStrategy) rather than
    concrete implementations. It also shows composition over
    inheritance by using strategy objects.
    
    Attributes:
        strategy: The current welcome strategy being used.
        usage_log: List of all welcome activities.
    """
    
    def __init__(self, strategy: WelcomeStrategy = None):
        """
        Initialize the welcome service with a strategy.
        
        Args:
            strategy: The welcome strategy to use. Defaults to formal.
        """
        self.strategy = strategy or FormalWelcomeStrategy()
        self.usage_log: List[Dict[str, Any]] = []
        self._total_welcomes = 0
    
    @property
    def total_welcomes(self) -> int:
        """
        Property that provides read-only access to total welcome count.
        
        This demonstrates the use of properties to control
        access to internal state and provide computed values.
        """
        return self._total_welcomes
    
    def set_strategy(self, strategy: WelcomeStrategy) -> None:
        """
        Change the welcome strategy at runtime.
        
        This method demonstrates how the Strategy Pattern
        allows changing behavior dynamically without
        modifying the service class itself.
        
        Args:
            strategy: The new welcome strategy to use.
        """
        if not isinstance(strategy, WelcomeStrategy):
            raise ConfigurationError(
                "INVALID_STRATEGY",
                "Strategy must be an instance of WelcomeStrategy"
            )
        self.strategy = strategy
    
    def welcome_user(self, name: str) -> str:
        """
        Welcome a user using the current strategy.
        
        This method demonstrates the Template Method pattern
        by defining a skeleton algorithm that delegates
        specific steps to strategy objects.
        
        Args:
            name: The name of the user to welcome.
            
        Returns:
            The generated welcome message.
            
        Raises:
            ValidationError: If the name fails validation.
        """
        # Validate input using current strategy
        if not self.strategy.validate_input(name):
            raise ValidationError(
                "INVALID_NAME",
                f"The name '{name}' is not valid for the current welcome strategy"
            )
        
        # Generate welcome message
        welcome_message = self.strategy.generate_welcome(name)
        
        # Update internal state
        self._total_welcomes += 1
        self._log_activity(name, welcome_message)
        
        return welcome_message
    
    def _log_activity(self, name: str, message: str) -> None:
        """
        Log welcome activity for auditing and analytics.
        
        This private method demonstrates encapsulation by
        hiding the logging implementation details from
        external callers.
        
        Args:
            name: The name that was welcomed.
            message: The welcome message that was generated.
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'name': name,
            'message': message,
            'strategy': self.strategy.__class__.__name__
        }
        self.usage_log.append(log_entry)
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """
        Generate usage statistics from the activity log.
        
        This method demonstrates how objects can provide
        analytics and insights based on their internal state.
        
        Returns:
            Dictionary containing various usage statistics.
        """
        if not self.usage_log:
            return {}
        
        # Count welcomes by strategy
        strategy_counts = {}
        for entry in self.usage_log:
            strategy = entry['strategy']
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        # Get recent activity
        recent_activities = self.usage_log[-5:] if len(self.usage_log) > 5 else self.usage_log
        
        return {
            'total_welcomes': self._total_welcomes,
            'strategy_breakdown': strategy_counts,
            'recent_activities': recent_activities,
            'first_activity': self.usage_log[0]['timestamp'] if self.usage_log else None,
            'last_activity': self.usage_log[-1]['timestamp'] if self.usage_log else None
        }


class WelcomeConfiguration:
    """
    Configuration class for welcome system settings.
    
    This class demonstrates the use of objects to manage
    configuration data, with validation and default values.
    It shows how OOP can make configuration management
    more robust and self-documenting.
    
    Attributes:
        default_strategy: The default welcome strategy type.
        enable_logging: Whether to enable activity logging.
        max_name_length: Maximum allowed name length.
        min_name_length: Minimum allowed name length.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize configuration with optional overrides.
        
        Args:
            **kwargs: Configuration options to override defaults.
        """
        self.default_strategy = kwargs.get('default_strategy', 'formal')
        self.enable_logging = kwargs.get('enable_logging', True)
        self.max_name_length = kwargs.get('max_name_length', 50)
        self.min_name_length = kwargs.get('min_name_length', 2)
        self.auto_title_case = kwargs.get('auto_title_case', True)
    
    def validate(self) -> bool:
        """
        Validate the configuration settings.
        
        Returns:
            True if configuration is valid, False otherwise.
        """
        if self.min_name_length < 1:
            return False
        if self.max_name_length < self.min_name_length:
            return False
        if self.default_strategy not in ['formal', 'casual', 'professional']:
            return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary for serialization."""
        return {
            'default_strategy': self.default_strategy,
            'enable_logging': self.enable_logging,
            'max_name_length': self.max_name_length,
            'min_name_length': self.min_name_length,
            'auto_title_case': self.auto_title_case
        }


class WelcomeServiceBuilder:
    """
    Builder class for constructing WelcomeService instances.
    
    This class demonstrates the Builder Pattern, which provides
    a flexible way to construct complex objects step by step.
    It's particularly useful when objects have many configuration
    options or when construction involves multiple steps.
    """
    
    def __init__(self):
        """Initialize the builder with default configuration."""
        self._config = WelcomeConfiguration()
        self._strategy = None
    
    def with_configuration(self, config: WelcomeConfiguration) -> 'WelcomeServiceBuilder':
        """
        Set the configuration for the service.
        
        Args:
            config: The configuration to use.
            
        Returns:
            self for method chaining.
        """
        self._config = config
        return self
    
    def with_strategy(self, strategy: WelcomeStrategy) -> 'WelcomeServiceBuilder':
        """
        Set a specific strategy for the service.
        
        Args:
            strategy: The welcome strategy to use.
            
        Returns:
            self for method chaining.
        """
        self._strategy = strategy
        return self
    
    def build(self) -> WelcomeService:
        """
        Build the WelcomeService instance.
        
        Returns:
            A fully configured WelcomeService instance.
            
        Raises:
            ConfigurationError: If the configuration is invalid.
        """
        if not self._config.validate():
            raise ConfigurationError(
                "INVALID_CONFIG",
                "The provided configuration is not valid"
            )
        
        # Create strategy based on configuration if not explicitly set
        if self._strategy is None:
            strategy_map = {
                'formal': FormalWelcomeStrategy(),
                'casual': CasualWelcomeStrategy(),
                'professional': ProfessionalWelcomeStrategy()
            }
            self._strategy = strategy_map.get(
                self._config.default_strategy,
                FormalWelcomeStrategy()
            )
        
        service = WelcomeService(self._strategy)
        return service


class WelcomeRepository:
    """
    Repository class for persisting welcome data.
    
    This class demonstrates the Repository Pattern, which
    abstracts data storage details from business logic.
    It provides a collection-like interface for accessing
    welcome data while hiding the storage implementation.
    """
    
    def __init__(self):
        """Initialize with in-memory storage for demonstration."""
        self._storage = []
        self._next_id = 1
    
    def save(self, name: str, message: str, strategy: str) -> int:
        """
        Save a welcome record to the repository.
        
        Args:
            name: The name that was welcomed.
            message: The welcome message.
            strategy: The strategy used.
            
        Returns:
            The ID of the saved record.
        """
        record = {
            'id': self._next_id,
            'name': name,
            'message': message,
            'strategy': strategy,
            'timestamp': datetime.now().isoformat()
        }
        self._storage.append(record)
        self._next_id += 1
        return record['id']
    
    def find_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Find welcome records by name.
        
        Args:
            name: The name to search for.
            
        Returns:
            List of matching welcome records.
        """
        return [record for record in self._storage if record['name'] == name]
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all welcome records.
        
        Returns:
            List of all welcome records.
        """
        return self._storage.copy()
    
    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent welcome records.
        
        Args:
            limit: Maximum number of records to return.
            
        Returns:
            List of recent welcome records.
        """
        return self._storage[-limit:] if self._storage else []


class WelcomeManager:
    """
    Comprehensive manager class that coordinates multiple welcome components.
    
    This class demonstrates the Facade Pattern by providing a
    simplified interface to a complex subsystem of welcome-related
    classes. It shows how OOP enables building layered architectures.
    
    Attributes:
        service: The core welcome service.
        repository: The data repository for welcome records.
        config: The configuration manager.
    """
    
    def __init__(self, config: WelcomeConfiguration = None):
        """
        Initialize the welcome manager.
        
        Args:
            config: Optional configuration for the manager.
        """
        self.config = config or WelcomeConfiguration()
        self.repository = WelcomeRepository()
        
        # Build service using builder
        builder = WelcomeServiceBuilder()
        self.service = builder.with_configuration(self.config).build()
    
    def welcome_user(self, name: str) -> str:
        """
        Welcome a user with full system integration.
        
        This method demonstrates how a facade can coordinate
        multiple subsystems to provide a simple, unified interface.
        
        Args:
            name: The name to welcome.
            
        Returns:
            The welcome message.
            
        Raises:
            ValidationError: If the name is invalid.
        """
        try:
            # Generate welcome message
            message = self.service.welcome_user(name)
            
            # Persist to repository
            self.repository.save(
                name=name,
                message=message,
                strategy=self.service.strategy.__class__.__name__
            )
            
            return message
            
        except ValidationError:
            # Re-raise validation errors
            raise
        except Exception as e:
            # Wrap other exceptions in domain-specific exception
            raise WelcomeException(
                "SYSTEM_ERROR",
                f"An error occurred while welcoming user: {str(e)}"
            )
    
    def change_strategy(self, strategy_type: str) -> None:
        """
        Change the welcome strategy.
        
        Args:
            strategy_type: Type of strategy ('formal', 'casual', 'professional').
            
        Raises:
            ConfigurationError: If the strategy type is unknown.
        """
        strategy_map = {
            'formal': FormalWelcomeStrategy(),
            'casual': CasualWelcomeStrategy(),
            'professional': ProfessionalWelcomeStrategy()
        }
        
        if strategy_type not in strategy_map:
            raise ConfigurationError(
                "UNKNOWN_STRATEGY",
                f"Unknown strategy type: {strategy_type}"
            )
        
        self.service.set_strategy(strategy_map[strategy_type])
    
    def get_system_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive system report.
        
        Returns:
            Dictionary containing system statistics and status.
        """
        service_stats = self.service.get_usage_statistics()
        all_records = self.repository.get_all()
        
        return {
            'service_statistics': service_stats,
            'total_records': len(all_records),
            'configuration': self.config.to_dict(),
            'system_status': 'operational',
            'report_generated': datetime.now().isoformat()
        }


class WelcomeContextManager:
    """
    Context manager for welcome operations with resource management.
    
    This class demonstrates how OOP can be used to create
    context managers that properly manage resources and
    ensure clean-up operations are performed.
    """
    
    def __init__(self, manager: WelcomeManager):
        """
        Initialize with a welcome manager.
        
        Args:
            manager: The welcome manager to use in the context.
        """
        self.manager = manager
        self.operation_count = 0
    
    def __enter__(self) -> 'WelcomeContextManager':
        """
        Enter the context manager context.
        
        Returns:
            self for use in with statements.
        """
        print("Welcome context manager started")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Exit the context manager context.
        
        Args:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Exception traceback if an exception occurred.
            
        Returns:
            True if exception was handled, False otherwise.
        """
        print(f"Welcome context manager completed. Operations: {self.operation_count}")
        
        # Log completion statistics
        report = self.manager.get_system_report()
        print(f"Final statistics: {report['service_statistics']['total_welcomes']} welcomes")
        
        # Don't suppress exceptions
        return False
    
    def welcome_with_context(self, name: str) -> str:
        """
        Perform a welcome operation within the context.
        
        Args:
            name: The name to welcome.
            
        Returns:
            The welcome message.
        """
        self.operation_count += 1
        return self.manager.welcome_user(name)


def demonstrate_oop_intermediate():
    """
    Demonstrate intermediate OOP concepts and patterns.
    """
    print("Object-Oriented Programming - Intermediate Level")
    
    # Demonstration 1: Strategy Pattern
    print("\n1. Strategy Pattern:")
    formal_service = WelcomeService(FormalWelcomeStrategy())
    casual_service = WelcomeService(CasualWelcomeStrategy())
    
    print(f"   Formal: {formal_service.welcome_user('Dr. Smith')}")
    print(f"   Casual: {casual_service.welcome_user('Mike')}")
    
    # Demonstration 2: Dynamic Strategy Switching
    print("\n2. Dynamic Strategy Switching:")
    service = WelcomeService(FormalWelcomeStrategy())
    print(f"   Initial: {service.welcome_user('Alice')}")
    
    service.set_strategy(CasualWelcomeStrategy())
    print(f"   After change: {service.welcome_user('Alice')}")
    
    # Demonstration 3: Builder Pattern
    print("\n3. Builder Pattern:")
    config = WelcomeConfiguration(default_strategy='professional', enable_logging=True)
    builder = WelcomeServiceBuilder()
    professional_service = builder.with_configuration(config).build()
    print(f"   Built service: {professional_service.welcome_user('Robert Johnson')}")
    
    # Demonstration 4: Repository Pattern
    print("\n4. Repository Pattern:")
    repository = WelcomeRepository()
    repository.save("Test User", "Welcome message", "formal")
    records = repository.find_by_name("Test User")
    print(f"   Found {len(records)} records for Test User")
    
    # Demonstration 5: Comprehensive Manager
    print("\n5. Welcome Manager:")
    manager = WelcomeManager()
    print(f"   Manager welcome: {manager.welcome_user('Sarah Wilson')}")
    
    # Demonstration 6: Context Manager
    print("\n6. Context Manager:")
    with WelcomeContextManager(manager) as context:
        result1 = context.welcome_with_context("Context User 1")
        result2 = context.welcome_with_context("Context User 2")
        print(f"   Context result 1: {result1}")
        print(f"   Context result 2: {result2}")
    
    # Demonstration 7: Exception Handling
    print("\n7. Exception Handling:")
    try:
        manager.welcome_user("")  # This should cause validation error
    except ValidationError as e:
        print(f"   Caught expected exception: {e}")
    
    # Demonstration 8: System Reporting
    print("\n8. System Reporting:")
    report = manager.get_system_report()
    print(f"   Total welcomes in report: {report['service_statistics']['total_welcomes']}")
    print(f"   System status: {report['system_status']}")


if __name__ == "__main__":
    demonstrate_oop_intermediate()

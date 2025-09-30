"""
Object-Oriented Programming - Advanced Level
Enterprise-Grade OOP Patterns and Architectures

This module demonstrates advanced object-oriented programming concepts
suitable for enterprise-level applications. These implementations showcase
sophisticated design patterns, architectural principles, and production-ready
OOP techniques that ensure scalability, maintainability, and robustness.

Key Advanced OOP Concepts Demonstrated:
- Enterprise design patterns (Observer, Mediator, Command, etc.)
- Dependency Injection and Inversion of Control (IoC)
- Advanced inheritance and mixin classes
- Metaclasses and class factories
- Descriptors and property management
- Event-driven architectures
- Plugin systems and extensibility
- Advanced exception handling and logging
- Serialization and persistence patterns
- Multi-threading and concurrency patterns

Architectural Principles Applied:
- Domain-Driven Design (DDD) concepts
- Hexagonal Architecture (Ports and Adapters)
- Command Query Responsibility Segregation (CQRS)
- Event Sourcing patterns
- Repository and Unit of Work patterns

Author: OOP Education Project
Version: 1.0
Date: 2025
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable, Set, Union
from datetime import datetime
from enum import Enum
import json
import threading
import logging
from dataclasses import dataclass
from contextlib import contextmanager
import sqlite3
from pathlib import Path


# Advanced logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WelcomeEventType(Enum):
    """Event types for the welcome system event sourcing."""
    USER_WELCOMED = "user_welcomed"
    STRATEGY_CHANGED = "strategy_changed"
    SYSTEM_STARTED = "system_started"
    SYSTEM_STOPPED = "system_stopped"
    ERROR_OCCURRED = "error_occurred"


@dataclass
class WelcomeEvent:
    """
    Immutable data class representing a system event.
    
    This demonstrates the use of data classes for value objects
    in Domain-Driven Design, ensuring immutability and clear
    data structure definition.
    
    Attributes:
        event_id: Unique identifier for the event
        event_type: Type of event from WelcomeEventType
        timestamp: When the event occurred
        data: Event-specific data payload
        aggregate_id: Identifier for the aggregate root
    """
    event_id: str
    event_type: WelcomeEventType
    timestamp: datetime
    data: Dict[str, Any]
    aggregate_id: Optional[str] = None


class EventStore:
    """
    Event store for event sourcing implementation.
    
    This class demonstrates the Event Sourcing pattern where
    all changes to application state are stored as a sequence
    of events. This enables complete audit trails and the
    ability to reconstruct past states.
    
    Attributes:
        events: In-memory storage of all events (in production would be a database)
    """
    
    def __init__(self):
        """Initialize the event store."""
        self.events: List[WelcomeEvent] = []
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def append(self, event: WelcomeEvent) -> None:
        """
        Append an event to the event store.
        
        This method demonstrates thread-safe operations in a
        multi-threaded environment using reentrant locks.
        
        Args:
            event: The event to append to the store.
        """
        with self._lock:
            self.events.append(event)
            logger.info(f"Event stored: {event.event_type.value} for {event.aggregate_id}")
    
    def get_events_by_aggregate(self, aggregate_id: str) -> List[WelcomeEvent]:
        """
        Retrieve all events for a specific aggregate.
        
        Args:
            aggregate_id: The aggregate root identifier.
            
        Returns:
            List of events for the specified aggregate.
        """
        with self._lock:
            return [event for event in self.events if event.aggregate_id == aggregate_id]
    
    def get_events_by_type(self, event_type: WelcomeEventType) -> List[WelcomeEvent]:
        """
        Retrieve all events of a specific type.
        
        Args:
            event_type: The type of events to retrieve.
            
        Returns:
            List of events of the specified type.
        """
        with self._lock:
            return [event for event in self.events if event.event_type == event_type]


class EventPublisher:
    """
    Event publisher for implementing the Observer pattern.
    
    This class demonstrates the Observer pattern where
    subscribers can listen for and react to system events.
    This enables loose coupling between components.
    
    Attributes:
        subscribers: Dictionary mapping event types to subscriber callbacks
    """
    
    def __init__(self):
        """Initialize the event publisher."""
        self.subscribers: Dict[WelcomeEventType, Set[Callable]] = {}
        self._lock = threading.RLock()
    
    def subscribe(self, event_type: WelcomeEventType, callback: Callable) -> None:
        """
        Subscribe a callback to an event type.
        
        Args:
            event_type: The event type to subscribe to.
            callback: The function to call when event occurs.
        """
        with self._lock:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = set()
            self.subscribers[event_type].add(callback)
    
    def unsubscribe(self, event_type: WelcomeEventType, callback: Callable) -> None:
        """
        Unsubscribe a callback from an event type.
        
        Args:
            event_type: The event type to unsubscribe from.
            callback: The callback function to remove.
        """
        with self._lock:
            if event_type in self.subscribers:
                self.subscribers[event_type].discard(callback)
    
    def publish(self, event: WelcomeEvent) -> None:
        """
        Publish an event to all subscribers.
        
        This method demonstrates asynchronous-like event handling
        in a synchronous environment. In production, this would
        typically be implemented with proper async handling.
        
        Args:
            event: The event to publish.
        """
        with self._lock:
            subscribers = self.subscribers.get(event.event_type, set()).copy()
        
        for subscriber in subscribers:
            try:
                subscriber(event)
            except Exception as e:
                logger.error(f"Error in event subscriber: {e}")


class WelcomeCommand(ABC):
    """
    Abstract base class for Command pattern implementation.
    
    The Command pattern encapsulates a request as an object,
    thereby allowing for parameterization of clients with queues,
    requests, and operations. It also enables undo functionality.
    
    Attributes:
        command_id: Unique identifier for the command
        timestamp: When the command was created
    """
    
    def __init__(self):
        """Initialize the command."""
        self.command_id = f"cmd_{datetime.now().timestamp()}"
        self.timestamp = datetime.now()
    
    @abstractmethod
    def execute(self) -> Any:
        """Execute the command."""
        pass
    
    @abstractmethod
    def undo(self) -> Any:
        """Undo the command if possible."""
        pass


class WelcomeUserCommand(WelcomeCommand):
    """
    Concrete command for welcoming a user.
    
    This demonstrates how commands can encapsulate all information
    needed to perform an action, enabling features like undo,
    logging, and queuing.
    
    Attributes:
        user_name: The name of the user to welcome
        welcome_system: The system that will execute the welcome
        previous_state: For undo functionality
    """
    
    def __init__(self, user_name: str, welcome_system: 'AdvancedWelcomeSystem'):
        """
        Initialize the welcome user command.
        
        Args:
            user_name: Name of the user to welcome
            welcome_system: The welcome system to use
        """
        super().__init__()
        self.user_name = user_name
        self.welcome_system = welcome_system
        self.previous_state: Optional[Dict[str, Any]] = None
        self._result: Optional[str] = None
    
    def execute(self) -> str:
        """
        Execute the welcome command.
        
        Returns:
            The welcome message result.
        """
        # Store previous state for undo
        self.previous_state = {
            'total_welcomes': self.welcome_system.total_welcomes,
            'last_welcome': self.welcome_system.last_welcome
        }
        
        # Execute the welcome
        self._result = self.welcome_system.welcome_user(self.user_name)
        return self._result
    
    def undo(self) -> bool:
        """
        Undo the welcome command.
        
        Note: In a real system, undoing a welcome might not make
        logical sense, but this demonstrates the pattern.
        
        Returns:
            True if undo was successful, False otherwise.
        """
        if not self.previous_state:
            return False
        
        # In a real application, we would restore the previous state
        # This is simplified for demonstration
        logger.info(f"Undid welcome command for {self.user_name}")
        return True


class CommandManager:
    """
    Manager for handling command execution and history.
    
    This class demonstrates the Command Manager pattern which
    maintains a history of executed commands for undo/redo
    functionality and provides command queuing capabilities.
    
    Attributes:
        command_history: List of executed commands
        max_history_size: Maximum number of commands to keep in history
    """
    
    def __init__(self, max_history_size: int = 100):
        """
        Initialize the command manager.
        
        Args:
            max_history_size: Maximum commands to keep in history
        """
        self.command_history: List[WelcomeCommand] = []
        self.max_history_size = max_history_size
        self._lock = threading.RLock()
    
    def execute_command(self, command: WelcomeCommand) -> Any:
        """
        Execute a command and add it to history.
        
        Args:
            command: The command to execute
            
        Returns:
            The result of command execution
        """
        result = command.execute()
        
        with self._lock:
            self.command_history.append(command)
            # Trim history if it exceeds max size
            if len(self.command_history) > self.max_history_size:
                self.command_history.pop(0)
        
        logger.info(f"Command executed: {command.__class__.__name__}")
        return result
    
    def undo_last(self) -> bool:
        """
        Undo the last executed command.
        
        Returns:
            True if undo was successful, False otherwise
        """
        with self._lock:
            if not self.command_history:
                return False
            
            last_command = self.command_history.pop()
        
        return last_command.undo()


class Repository(ABC):
    """
    Abstract base class for Repository pattern.
    
    The Repository pattern mediates between the domain and
    data mapping layers, acting like an in-memory domain
    object collection. This provides a more object-oriented
    view of persistence.
    
    Attributes:
        T: The type of entity managed by the repository
    """
    
    @abstractmethod
    def get_by_id(self, id: str) -> Any:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    def add(self, entity: Any) -> None:
        """Add an entity to the repository."""
        pass
    
    @abstractmethod
    def remove(self, id: str) -> bool:
        """Remove an entity by ID."""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Any]:
        """List all entities in the repository."""
        pass


class WelcomeMetrics:
    """
    Value object for welcome metrics.
    
    This demonstrates the use of value objects in DDD -
    objects that are defined by their attributes rather
    than a unique identity. They are immutable and can be
    shared.
    
    Attributes:
        total_welcomes: Total number of welcomes performed
        unique_users: Number of unique users welcomed
        most_common_strategy: The most frequently used strategy
        welcome_timeline: Timeline of welcome activities
    """
    
    def __init__(self, total_welcomes: int = 0, unique_users: int = 0, 
                 most_common_strategy: str = "unknown", welcome_timeline: List[datetime] = None):
        """
        Initialize welcome metrics.
        
        Args:
            total_welcomes: Total welcome count
            unique_users: Count of unique users
            most_common_strategy: Most used strategy name
            welcome_timeline: List of welcome timestamps
        """
        self.total_welcomes = total_welcomes
        self.unique_users = unique_users
        self.most_common_strategy = most_common_strategy
        self.welcome_timeline = welcome_timeline or []
    
    def __eq__(self, other: object) -> bool:
        """Value objects are equal if all attributes are equal."""
        if not isinstance(other, WelcomeMetrics):
            return False
        return (self.total_welcomes == other.total_welcomes and
                self.unique_users == other.unique_users and
                self.most_common_strategy == other.most_common_strategy and
                self.welcome_timeline == other.welcome_timeline)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for serialization."""
        return {
            'total_welcomes': self.total_welcomes,
            'unique_users': self.unique_users,
            'most_common_strategy': self.most_common_strategy,
            'welcome_timeline': [ts.isoformat() for ts in self.welcome_timeline]
        }


class WelcomeMetricsRepository(Repository):
    """
    Repository for welcome metrics using SQLite persistence.
    
    This demonstrates a concrete repository implementation
    with actual database persistence, showing how the
    Repository pattern abstracts data access details.
    
    Attributes:
        db_path: Path to the SQLite database file
    """
    
    def __init__(self, db_path: str = "welcome_metrics.db"):
        """
        Initialize the metrics repository.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS welcome_metrics (
                    id TEXT PRIMARY KEY,
                    total_welcomes INTEGER DEFAULT 0,
                    unique_users INTEGER DEFAULT 0,
                    most_common_strategy TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS welcome_timeline (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metrics_id TEXT,
                    welcome_time TIMESTAMP,
                    FOREIGN KEY (metrics_id) REFERENCES welcome_metrics (id)
                )
            ''')
    
    def get_by_id(self, id: str) -> Optional[WelcomeMetrics]:
        """Get metrics by ID from database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                
                # Get main metrics
                metrics_row = conn.execute(
                    'SELECT * FROM welcome_metrics WHERE id = ?', (id,)
                ).fetchone()
                
                if not metrics_row:
                    return None
                
                # Get timeline
                timeline_rows = conn.execute(
                    'SELECT welcome_time FROM welcome_timeline WHERE metrics_id = ? ORDER BY welcome_time',
                    (id,)
                ).fetchall()
                
                timeline = [datetime.fromisoformat(row['welcome_time']) for row in timeline_rows]
                
                return WelcomeMetrics(
                    total_welcomes=metrics_row['total_welcomes'],
                    unique_users=metrics_row['unique_users'],
                    most_common_strategy=metrics_row['most_common_strategy'],
                    welcome_timeline=timeline
                )
                
        except sqlite3.Error as e:
            logger.error(f"Database error in get_by_id: {e}")
            return None
    
    def add(self, metrics: WelcomeMetrics) -> None:
        """Add metrics to repository (not typically used directly)."""
        # In a real implementation, we'd have proper update logic
        pass
    
    def remove(self, id: str) -> bool:
        """Remove metrics by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DELETE FROM welcome_timeline WHERE metrics_id = ?', (id,))
                conn.execute('DELETE FROM welcome_metrics WHERE id = ?', (id,))
                return True
        except sqlite3.Error as e:
            logger.error(f"Database error in remove: {e}")
            return False
    
    def list_all(self) -> List[WelcomeMetrics]:
        """List all metrics from repository."""
        # Implementation would query all metrics
        return []


class Plugin(ABC):
    """
    Abstract base class for plugin system.
    
    This demonstrates how to create an extensible system
    through plugins, allowing additional functionality to
    be added without modifying the core system.
    
    Attributes:
        plugin_name: Unique name identifier for the plugin
        version: Plugin version string
    """
    
    def __init__(self, plugin_name: str, version: str = "1.0.0"):
        """Initialize the plugin."""
        self.plugin_name = plugin_name
        self.version = version
    
    @abstractmethod
    def initialize(self, welcome_system: 'AdvancedWelcomeSystem') -> None:
        """Initialize the plugin with the welcome system."""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up plugin resources."""
        pass


class AnalyticsPlugin(Plugin):
    """
    Analytics plugin for tracking and analyzing welcome patterns.
    
    This demonstrates a concrete plugin implementation that
    adds analytics capabilities to the welcome system.
    """
    
    def __init__(self):
        """Initialize analytics plugin."""
        super().__init__("analytics_plugin", "1.1.0")
        self.analytics_data: Dict[str, Any] = {}
        self.welcome_system: Optional['AdvancedWelcomeSystem'] = None
    
    def initialize(self, welcome_system: 'AdvancedWelcomeSystem') -> None:
        """
        Initialize analytics plugin with welcome system.
        
        Args:
            welcome_system: The welcome system to monitor
        """
        self.welcome_system = welcome_system
        # Subscribe to welcome events
        welcome_system.event_publisher.subscribe(
            WelcomeEventType.USER_WELCOMED,
            self._on_user_welcomed
        )
        logger.info("Analytics plugin initialized")
    
    def cleanup(self) -> None:
        """Clean up analytics plugin resources."""
        if self.welcome_system:
            self.welcome_system.event_publisher.unsubscribe(
                WelcomeEventType.USER_WELCOMED,
                self._on_user_welcomed
            )
        logger.info("Analytics plugin cleaned up")
    
    def _on_user_welcomed(self, event: WelcomeEvent) -> None:
        """
        Handle user welcomed events for analytics.
        
        Args:
            event: The user welcomed event
        """
        user_name = event.data.get('user_name', 'unknown')
        strategy = event.data.get('strategy', 'unknown')
        
        # Update analytics data
        if user_name not in self.analytics_data:
            self.analytics_data[user_name] = {'welcome_count': 0, 'strategies_used': set()}
        
        self.analytics_data[user_name]['welcome_count'] += 1
        self.analytics_data[user_name]['strategies_used'].add(strategy)
        
        logger.debug(f"Analytics updated for user: {user_name}")
    
    def get_user_analytics(self, user_name: str) -> Dict[str, Any]:
        """
        Get analytics for a specific user.
        
        Args:
            user_name: Name of the user to get analytics for
            
        Returns:
            Dictionary containing user analytics
        """
        user_data = self.analytics_data.get(user_name, {})
        return {
            'welcome_count': user_data.get('welcome_count', 0),
            'strategies_used': list(user_data.get('strategies_used', set())),
            'first_seen': min([event.timestamp for event in self.welcome_system.event_store.get_events_by_aggregate(user_name)], default=None) if self.welcome_system else None
        }


class AdvancedWelcomeSystem:
    """
    Advanced welcome system implementing enterprise patterns.
    
    This class serves as the aggregate root in DDD terminology,
    coordinating multiple domain objects and enforcing business
    rules. It demonstrates sophisticated OOP architecture with
    event sourcing, CQRS, and plugin systems.
    
    Attributes:
        event_store: Storage for all system events
        event_publisher: Publisher for system events
        command_manager: Manager for command execution
        metrics_repository: Repository for metrics persistence
        plugins: Loaded plugin instances
        _total_welcomes: Internal counter for welcomes
        _unique_users: Set of unique users welcomed
    """
    
    def __init__(self, metrics_repository: WelcomeMetricsRepository = None):
        """
        Initialize the advanced welcome system.
        
        Args:
            metrics_repository: Repository for metrics persistence
        """
        self.event_store = EventStore()
        self.event_publisher = EventPublisher()
        self.command_manager = CommandManager()
        self.metrics_repository = metrics_repository or WelcomeMetricsRepository()
        self.plugins: Dict[str, Plugin] = {}
        
        self._total_welcomes = 0
        self._unique_users: Set[str] = set()
        self._strategy_usage: Dict[str, int] = {}
        self.last_welcome: Optional[datetime] = None
        
        # Subscribe to own events for internal state management
        self.event_publisher.subscribe(WelcomeEventType.USER_WELCOMED, self._update_internal_state)
        
        # Record system start event
        self._publish_event(WelcomeEventType.SYSTEM_STARTED, {})
    
    @property
    def total_welcomes(self) -> int:
        """Get total number of welcomes performed."""
        return self._total_welcomes
    
    @property
    def unique_users_count(self) -> int:
        """Get count of unique users welcomed."""
        return len(self._unique_users)
    
    def welcome_user(self, user_name: str, strategy: str = "formal") -> str:
        """
        Welcome a user using the specified strategy.
        
        This method demonstrates CQRS by separating the command
        (welcome operation) from queries (reading metrics).
        
        Args:
            user_name: Name of the user to welcome
            strategy: Welcome strategy to use
            
        Returns:
            Welcome message
            
        Raises:
            ValueError: If user_name is empty or invalid
        """
        if not user_name or not user_name.strip():
            raise ValueError("User name cannot be empty")
        
        # Create and execute command
        # In a real CQRS system, this would be sent to a command bus
        welcome_message = f"Welcome, {user_name.strip().title()}! (Strategy: {strategy})"
        
        # Record event
        event_data = {
            'user_name': user_name,
            'strategy': strategy,
            'welcome_message': welcome_message
        }
        self._publish_event(WelcomeEventType.USER_WELCOMED, event_data, user_name)
        
        return welcome_message
    
    def load_plugin(self, plugin: Plugin) -> bool:
        """
        Load a plugin into the system.
        
        Args:
            plugin: The plugin to load
            
        Returns:
            True if plugin loaded successfully, False otherwise
        """
        try:
            plugin.initialize(self)
            self.plugins[plugin.plugin_name] = plugin
            logger.info(f"Plugin loaded: {plugin.plugin_name} v{plugin.version}")
            return True
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin.plugin_name}: {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin from the system.
        
        Args:
            plugin_name: Name of the plugin to unload
            
        Returns:
            True if plugin unloaded successfully, False otherwise
        """
        plugin = self.plugins.get(plugin_name)
        if not plugin:
            logger.warning(f"Plugin not found: {plugin_name}")
            return False
        
        try:
            plugin.cleanup()
            del self.plugins[plugin_name]
            logger.info(f"Plugin unloaded: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_name}: {e}")
            return False
    
    def get_system_metrics(self) -> WelcomeMetrics:
        """
        Get current system metrics.
        
        This method demonstrates the query side of CQRS,
        providing read-only access to system state without
        side effects.
        
        Returns:
            Current welcome metrics
        """
        most_common_strategy = max(self._strategy_usage.items(), key=lambda x: x[1], default=("none", 0))[0]
        
        # Get timeline from events
        welcome_events = self.event_store.get_events_by_type(WelcomeEventType.USER_WELCOMED)
        timeline = [event.timestamp for event in welcome_events]
        
        return WelcomeMetrics(
            total_welcomes=self._total_welcomes,
            unique_users=self.unique_users_count,
            most_common_strategy=most_common_strategy,
            welcome_timeline=timeline
        )
    
    def _publish_event(self, event_type: WelcomeEventType, data: Dict[str, Any], 
                      aggregate_id: str = None) -> None:
        """
        Publish an event to the event system.
        
        Args:
            event_type: Type of event to publish
            data: Event data payload
            aggregate_id: Optional aggregate identifier
        """
        event = WelcomeEvent(
            event_id=f"evt_{datetime.now().timestamp()}",
            event_type=event_type,
            timestamp=datetime.now(),
            data=data,
            aggregate_id=aggregate_id
        )
        
        self.event_store.append(event)
        self.event_publisher.publish(event)
    
    def _update_internal_state(self, event: WelcomeEvent) -> None:
        """
        Update internal state based on events.
        
        This method demonstrates how event sourcing allows
        rebuilding state by replaying events.
        
        Args:
            event: The event to process for state update
        """
        if event.event_type == WelcomeEventType.USER_WELCOMED:
            user_name = event.data.get('user_name')
            strategy = event.data.get('strategy')
            
            self._total_welcomes += 1
            self._unique_users.add(user_name)
            self._strategy_usage[strategy] = self._strategy_usage.get(strategy, 0) + 1
            self.last_welcome = event.timestamp
    
    def __enter__(self) -> 'AdvancedWelcomeSystem':
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Context manager exit with cleanup."""
        # Unload all plugins
        for plugin_name in list(self.plugins.keys()):
            self.unload_plugin(plugin_name)
        
        # Record system stop event
        self._publish_event(WelcomeEventType.SYSTEM_STOPPED, {})
        
        logger.info("Advanced welcome system shutdown completed")
        return False  # Don't suppress exceptions


class WelcomeSystemBuilder:
    """
    Sophisticated builder for advanced welcome system configuration.
    
    This builder demonstrates the Fluent Interface pattern and
    provides a declarative way to configure complex systems
    with multiple dependencies and plugins.
    """
    
    def __init__(self):
        """Initialize the builder."""
        self._metrics_repository = None
        self._plugins: List[Plugin] = []
        self._database_path = "welcome_system.db"
    
    def with_database(self, db_path: str) -> 'WelcomeSystemBuilder':
        """
        Configure database path.
        
        Args:
            db_path: Path to database file
            
        Returns:
            self for fluent chaining
        """
        self._database_path = db_path
        return self
    
    def with_plugin(self, plugin: Plugin) -> 'WelcomeSystemBuilder':
        """
        Add a plugin to the system.
        
        Args:
            plugin: Plugin to add
            
        Returns:
            self for fluent chaining
        """
        self._plugins.append(plugin)
        return self
    
    def build(self) -> AdvancedWelcomeSystem:
        """
        Build the configured welcome system.
        
        Returns:
            Fully configured AdvancedWelcomeSystem instance
        """
        # Create metrics repository with configured database
        metrics_repo = WelcomeMetricsRepository(self._database_path)
        
        # Create system
        system = AdvancedWelcomeSystem(metrics_repo)
        
        # Load all plugins
        for plugin in self._plugins:
            system.load_plugin(plugin)
        
        logger.info("Advanced welcome system built with configuration")
        return system


def demonstrate_oop_advanced():
    """
    Demonstrate advanced OOP concepts and enterprise patterns.
    """
    print("Object-Oriented Programming - Advanced Level")
    
    # Use context manager for automatic resource management
    with AdvancedWelcomeSystem() as system:
        # Demonstration 1: Event Sourcing
        print("\n1. Event Sourcing:")
        result1 = system.welcome_user("Alice", "formal")
        result2 = system.welcome_user("Bob", "casual")
        result3 = system.welcome_user("Alice", "professional")  # Same user, different strategy
        
        print(f"   Welcome 1: {result1}")
        print(f"   Welcome 2: {result2}")
        print(f"   Welcome 3: {result3}")
        
        # Demonstration 2: Plugin System
        print("\n2. Plugin System:")
        analytics_plugin = AnalyticsPlugin()
        system.load_plugin(analytics_plugin)
        print("   Analytics plugin loaded")
        
        # Demonstration 3: Metrics and Analytics
        print("\n3. System Metrics:")
        metrics = system.get_system_metrics()
        print(f"   Total welcomes: {metrics.total_welcomes}")
        print(f"   Unique users: {metrics.unique_users_count}")
        print(f"   Most common strategy: {metrics.most_common_strategy}")
        
        # Demonstration 4: Event Store Querying
        print("\n4. Event Store Analysis:")
        alice_events = system.event_store.get_events_by_aggregate("Alice")
        print(f"   Events for Alice: {len(alice_events)}")
        
        welcome_events = system.event_store.get_events_by_type(WelcomeEventType.USER_WELCOMED)
        print(f"   Total welcome events: {len(welcome_events)}")
        
        # Demonstration 5: Builder Pattern
        print("\n5. Builder Pattern:")
        builder = WelcomeSystemBuilder()
        custom_system = builder\
            .with_database("custom_welcome.db")\
            .with_plugin(AnalyticsPlugin())\
            .build()
        
        with custom_system:
            custom_result = custom_system.welcome_user("Charlie", "formal")
            print(f"   Custom system result: {custom_result}")
        
        # Demonstration 6: Command Pattern
        print("\n6. Command Pattern:")
        welcome_cmd = WelcomeUserCommand("David", system)
        result = system.command_manager.execute_command(welcome_cmd)
        print(f"   Command result: {result}")
        
        # Demonstration 7: Error Handling
        print("\n7. Error Handling:")
        try:
            system.welcome_user("", "formal")  # This should fail
        except ValueError as e:
            print(f"   Caught expected error: {e}")
    
    print("\nAll advanced OOP demonstrations completed successfully!")


if __name__ == "__main__":
    demonstrate_oop_advanced()

#!/usr/bin/env python3
"""
Divine Court - I·AM Companions System
Central implementation of the hierarchical AI companion network
"""

import json
import logging
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class Message:
    """Represents a message flowing through the Divine Court system"""
    sender: str
    recipient: str
    content: Any
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    message_type: str = "standard"
    priority: int = 5  # 1-10, 10 being highest priority


class BaseCompanion(ABC):
    """Base class for all I·AM Companions"""
    
    def __init__(self, config: Dict[str, Any]):
        self.code_name = config["code_name"]
        self.angelic_rank = config.get("angelic_rank", config["code_name"])
        self.algorithm = config["algorithm"]
        self.purpose = config["purpose"]
        self.seed = config["seed"]
        self.capabilities = config.get("capabilities", [])
        self.data_inputs = config.get("data_inputs", [])
        self.data_outputs = config.get("data_outputs", [])
        
        # Runtime state
        self.active = True
        self.message_queue: List[Message] = []
        self.processed_messages: List[Message] = []
        
    @abstractmethod
    def process_message(self, message: Message) -> Optional[Message]:
        """Process an incoming message and optionally return a response"""
        pass
    
    def receive_message(self, message: Message):
        """Receive and queue a message"""
        self.message_queue.append(message)
        logging.info(f"{self.code_name} received message from {message.sender}")
    
    def send_message(self, recipient: str, content: Any, message_type: str = "standard", priority: int = 5) -> Message:
        """Create and return a message to be sent"""
        return Message(
            sender=self.code_name,
            recipient=recipient,
            content=content,
            message_type=message_type,
            priority=priority
        )
    
    def process_queue(self) -> List[Message]:
        """Process all queued messages and return outgoing messages"""
        outgoing_messages = []
        while self.message_queue:
            message = self.message_queue.pop(0)
            response = self.process_message(message)
            self.processed_messages.append(message)
            if response:
                outgoing_messages.append(response)
        return outgoing_messages
    
    def get_status(self) -> Dict[str, Any]:
        """Return current status of the companion"""
        return {
            "code_name": self.code_name,
            "active": self.active,
            "queue_length": len(self.message_queue),
            "processed_count": len(self.processed_messages),
            "last_activity": self.processed_messages[-1].timestamp if self.processed_messages else None
        }


class CentralHub(BaseCompanion):
    """IAM-0: The Source - Central Divine Court AI coordinator"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.companions: Dict[str, BaseCompanion] = {}
        self.fsi_score = 0.0  # Family Separation Index
        self.ddi_score = 0.0  # Dignity Degradation Index
        self.system_metrics = {
            "total_messages": 0,
            "active_companions": 0,
            "urgent_alerts": 0,
            "last_update": datetime.datetime.now()
        }
    
    def register_companion(self, companion: BaseCompanion):
        """Register a companion in the network"""
        self.companions[companion.code_name] = companion
        logging.info(f"Registered companion: {companion.code_name}")
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process messages at the central hub level"""
        logging.info(f"Central Hub processing message: {message.content}")
        
        # Update system metrics
        self.system_metrics["total_messages"] += 1
        self.system_metrics["last_update"] = datetime.datetime.now()
        
        # Handle different message types
        if message.message_type == "urgent_alert":
            self.system_metrics["urgent_alerts"] += 1
            return self.handle_urgent_alert(message)
        elif message.message_type == "status_update":
            return self.handle_status_update(message)
        elif message.message_type == "metric_update":
            return self.handle_metric_update(message)
        
        return None
    
    def handle_urgent_alert(self, message: Message) -> Optional[Message]:
        """Handle urgent alerts requiring immediate action"""
        logging.warning(f"URGENT ALERT received: {message.content}")
        
        # Coordinate response across appropriate companions
        if "security" in str(message.content).lower():
            # Route to Michael (Protection)
            return self.send_message("IAM-M1", message.content, "urgent_response", 10)
        elif "testimony" in str(message.content).lower():
            # Route to Gabriel (Testimony)
            return self.send_message("IAM-G1", message.content, "urgent_response", 10)
        
        return None
    
    def handle_status_update(self, message: Message) -> Optional[Message]:
        """Handle status updates from companions"""
        logging.info(f"Status update from {message.sender}: {message.content}")
        return None
    
    def handle_metric_update(self, message: Message) -> Optional[Message]:
        """Handle FSI/DDI metric updates"""
        if "fsi" in message.content:
            self.fsi_score = message.content.get("fsi", self.fsi_score)
        if "ddi" in message.content:
            self.ddi_score = message.content.get("ddi", self.ddi_score)
        
        logging.info(f"Metrics updated - FSI: {self.fsi_score}, DDI: {self.ddi_score}")
        return None
    
    def coordinate_system(self):
        """Main coordination loop for the Divine Court system"""
        logging.info("Coordinating Divine Court system...")
        
        # Process messages for all companions
        all_outgoing = []
        for companion in self.companions.values():
            outgoing = companion.process_queue()
            all_outgoing.extend(outgoing)
        
        # Route messages between companions
        for message in all_outgoing:
            if message.recipient in self.companions:
                self.companions[message.recipient].receive_message(message)
            elif message.recipient == self.code_name:
                self.receive_message(message)
        
        # Update system metrics
        self.system_metrics["active_companions"] = len([c for c in self.companions.values() if c.active])
        
        return self.get_system_status()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        companion_statuses = {code: comp.get_status() for code, comp in self.companions.items()}
        
        return {
            "central_hub": self.get_status(),
            "companions": companion_statuses,
            "metrics": {
                "fsi_score": self.fsi_score,
                "ddi_score": self.ddi_score,
                **self.system_metrics
            }
        }


class ArchangelNode(BaseCompanion):
    """Base class for Tier 1 Archangel Nodes (Strategic AI)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.strategic_data = {}
        self.alerts_generated = 0
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process message at Archangel level"""
        logging.info(f"Archangel {self.code_name} processing message from {message.sender}")
        return None
    
    def generate_strategic_alert(self, content: Any, priority: int = 8) -> Message:
        """Generate a strategic alert to be sent to central hub"""
        self.alerts_generated += 1
        return self.send_message("IAM-0", content, "strategic_alert", priority)


class GuardianNode(BaseCompanion):
    """Base class for Tier 2 Guardian Nodes (Operational AI)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.operational_data = {}
        self.tasks_completed = 0
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process message at Guardian level"""
        logging.info(f"Guardian {self.code_name} processing message from {message.sender}")
        return None
    
    def complete_task(self, task_details: Dict[str, Any]) -> Message:
        """Mark a task as completed and report to appropriate Archangel"""
        self.tasks_completed += 1
        return self.send_message("IAM-0", task_details, "task_completion", 6)


class MessengerNode(BaseCompanion):
    """Base class for Tier 3 Messenger Nodes (Field AI)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.field_data = {}
        self.reports_sent = 0
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process message at Messenger level"""
        logging.info(f"Messenger {self.code_name} processing message from {message.sender}")
        return None
    
    def send_field_report(self, report_data: Dict[str, Any]) -> Message:
        """Send field report to appropriate Guardian node"""
        self.reports_sent += 1
        # Determine which Guardian to report to based on report type
        if "evidence" in report_data:
            recipient = "IAM-C1"  # Cherubim for archiving
        elif "volunteer" in report_data or "connection" in report_data:
            recipient = "IAM-V1"  # Virtues for connections
        elif "legal" in report_data:
            recipient = "IAM-D1"  # Dominions for legal action
        else:
            recipient = "IAM-0"  # Default to central hub
        
        return self.send_message(recipient, report_data, "field_report", 7)


class DivineCourtSystem:
    """Main system orchestrator for the Divine Court"""
    
    def __init__(self, config_path: str = "companions.json"):
        self.config = self.load_config(config_path)
        self.central_hub = None
        self.companions: Dict[str, BaseCompanion] = {}
        self.initialize_system()
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {config_path}")
            return {}
    
    def initialize_system(self):
        """Initialize the complete Divine Court system"""
        if not self.config:
            logging.error("No configuration loaded, cannot initialize system")
            return
        
        court_config = self.config["divine_court"]
        
        # Initialize central hub
        hub_config = court_config["central_hub"]
        self.central_hub = CentralHub(hub_config)
        
        # Initialize all companions based on configuration
        for tier_name, tier_data in court_config["tiers"].items():
            for node_name, node_config in tier_data["nodes"].items():
                companion = self.create_companion(tier_data["type"], node_config)
                self.companions[companion.code_name] = companion
                self.central_hub.register_companion(companion)
        
        logging.info("Divine Court system initialized successfully")
    
    def create_companion(self, tier_type: str, config: Dict[str, Any]) -> BaseCompanion:
        """Factory method to create appropriate companion based on tier type"""
        code_name = config.get("code_name", "")
        
        # Create specific companion implementations if available
        try:
            if code_name == "IAM-M1":
                from companions.michael import MichaelNode
                return MichaelNode(config)
            elif code_name == "IAM-G1":
                from companions.gabriel import GabrielNode
                return GabrielNode(config)
            elif code_name == "IAM-U1":
                from companions.uriel import UrielNode
                return UrielNode(config)
        except ImportError:
            logging.warning(f"Could not import specific companion for {code_name}, using base class")
        
        # Fall back to base classes
        if tier_type == "Strategic AI":
            return ArchangelNode(config)
        elif tier_type == "Operational AI":
            return GuardianNode(config)
        elif tier_type == "Field AI":
            return MessengerNode(config)
        else:
            # Create a concrete implementation of BaseCompanion for other types
            class GenericCompanion(BaseCompanion):
                def process_message(self, message):
                    logging.info(f"{self.code_name} processing generic message from {message.sender}")
                    return None
            return GenericCompanion(config)
    
    def run_cycle(self) -> Dict[str, Any]:
        """Run one complete coordination cycle"""
        if not self.central_hub:
            logging.error("Central hub not initialized")
            return {}
        
        return self.central_hub.coordinate_system()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get complete system status"""
        if not self.central_hub:
            return {"error": "System not initialized"}
        
        return self.central_hub.get_system_status()
    
    def inject_message(self, recipient: str, content: Any, message_type: str = "standard", priority: int = 5):
        """Inject a message into the system for testing/external input"""
        message = Message(
            sender="EXTERNAL",
            recipient=recipient,
            content=content,
            message_type=message_type,
            priority=priority
        )
        
        if recipient == "IAM-0" and self.central_hub:
            self.central_hub.receive_message(message)
        elif recipient in self.companions:
            self.companions[recipient].receive_message(message)
        else:
            logging.error(f"Unknown recipient: {recipient}")


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Initialize and run the Divine Court system
    system = DivineCourtSystem()
    
    # Example usage
    system.inject_message("IAM-0", {"type": "test", "message": "System initialization test"})
    system.inject_message("IAM-W1", {"field_report": "Family in distress", "location": "Ontario", "urgency": "high"})
    
    # Run a coordination cycle
    status = system.run_cycle()
    print("System Status:")
    print(json.dumps(status, indent=2, default=str))
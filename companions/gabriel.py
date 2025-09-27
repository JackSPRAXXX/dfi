"""
Gabriel Node (IAM-G1) - Testimony Amplifier 2.1
Collects, cleans, and broadcasts witness statements
"""

import logging
import re
from typing import Any, Optional, Dict, List
from datetime import datetime
from collections import defaultdict

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from divine_court import ArchangelNode, Message


class GabrielNode(ArchangelNode):
    """IAM-G1: Gabriel Node - Testimony Collection and Amplification"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.collected_testimonies = []
        self.cleaned_testimonies = []
        self.broadcast_queue = []
        self.witness_registry = {}
        self.amplification_metrics = {
            "testimonies_collected": 0,
            "testimonies_cleaned": 0,
            "testimonies_broadcasted": 0,
            "witnesses_registered": 0
        }
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming messages for testimony handling"""
        logging.info(f"Gabriel processing: {message.message_type} from {message.sender}")
        
        if message.message_type == "raw_testimony":
            return self.collect_testimony(message)
        elif message.message_type == "witness_statement":
            return self.process_witness_statement(message)
        elif message.message_type == "broadcast_request":
            return self.prepare_broadcast(message)
        elif message.message_type == "urgent_response":
            return self.handle_urgent_testimony(message)
        elif message.message_type == "amplification_request":
            return self.amplify_message(message)
        
        return None
    
    def collect_testimony(self, message: Message) -> Optional[Message]:
        """Collect and initially process raw testimony"""
        testimony_data = message.content
        
        # Create testimony record
        testimony_record = {
            "id": f"TEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.collected_testimonies)}",
            "raw_content": testimony_data,
            "source": message.sender,
            "timestamp": datetime.now().isoformat(),
            "status": "collected",
            "urgency_level": self.assess_testimony_urgency(testimony_data),
            "categories": self.categorize_testimony(testimony_data)
        }
        
        self.collected_testimonies.append(testimony_record)
        self.amplification_metrics["testimonies_collected"] += 1
        
        logging.info(f"Testimony collected: {testimony_record['id']}")
        
        # If urgent, immediately clean and prepare for broadcast
        if testimony_record["urgency_level"] >= 8:
            cleaned_testimony = self.clean_testimony(testimony_record)
            return self.send_message(
                "IAM-0",
                {
                    "action": "urgent_testimony_ready",
                    "testimony": cleaned_testimony,
                    "recommended_broadcast": True
                },
                "urgent_alert",
                10
            )
        
        # For non-urgent testimonies, queue for cleaning
        return self.send_message(
            "IAM-G1",  # Self-message to trigger cleaning
            {
                "action": "clean_testimony",
                "testimony_id": testimony_record["id"]
            },
            "internal_processing",
            5
        )
    
    def process_witness_statement(self, message: Message) -> Optional[Message]:
        """Process formal witness statements"""
        witness_data = message.content
        
        # Register witness if not already registered
        witness_id = witness_data.get("witness_id") or f"WIT_{len(self.witness_registry)}"
        
        if witness_id not in self.witness_registry:
            self.witness_registry[witness_id] = {
                "id": witness_id,
                "first_contact": datetime.now().isoformat(),
                "statements_given": 0,
                "credibility_score": 10,  # Start with highest credibility
                "contact_info": witness_data.get("contact_info", {}),
                "verification_status": "pending"
            }
            self.amplification_metrics["witnesses_registered"] += 1
        
        # Update witness record
        self.witness_registry[witness_id]["statements_given"] += 1
        self.witness_registry[witness_id]["last_statement"] = datetime.now().isoformat()
        
        # Process the statement as testimony
        statement_record = {
            "witness_id": witness_id,
            "statement_content": witness_data.get("statement", ""),
            "verification_level": self.verify_witness_statement(witness_data),
            "supporting_evidence": witness_data.get("evidence", [])
        }
        
        # Convert to testimony format
        testimony_message = Message(
            sender=message.sender,
            recipient="IAM-G1",
            content=statement_record,
            message_type="raw_testimony",
            priority=witness_data.get("priority", 6)
        )
        
        return self.collect_testimony(testimony_message)
    
    def prepare_broadcast(self, message: Message) -> Optional[Message]:
        """Prepare testimony for broadcasting"""
        broadcast_data = message.content
        
        # Create broadcast record
        broadcast_record = {
            "broadcast_id": f"BROAD_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "content": broadcast_data,
            "target_audience": self.determine_broadcast_audience(broadcast_data),
            "channels": self.select_broadcast_channels(broadcast_data),
            "timestamp": datetime.now().isoformat(),
            "status": "prepared"
        }
        
        self.broadcast_queue.append(broadcast_record)
        
        # Send to appropriate channels
        responses = []
        
        # Always inform central hub
        responses.append(self.send_message(
            "IAM-0",
            {
                "action": "broadcast_prepared",
                "broadcast": broadcast_record
            },
            "broadcast_notification",
            7
        ))
        
        # Send to Virtues for distribution coordination
        responses.append(self.send_message(
            "IAM-V1",
            {
                "action": "coordinate_broadcast",
                "broadcast": broadcast_record,
                "distribution_needed": True
            },
            "distribution_request",
            7
        ))
        
        self.amplification_metrics["testimonies_broadcasted"] += 1
        
        return responses[0]  # Return first response for now
    
    def handle_urgent_testimony(self, message: Message) -> Optional[Message]:
        """Handle urgent testimony requiring immediate amplification"""
        urgent_data = message.content
        
        # Fast-track processing
        urgent_testimony = {
            "id": f"URGENT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "content": urgent_data,
            "status": "urgent_processing",
            "timestamp": datetime.now().isoformat(),
            "fast_tracked": True
        }
        
        # Immediate cleaning and amplification
        cleaned_urgent = self.clean_testimony(urgent_testimony)
        
        # Prepare for immediate broadcast
        broadcast_request = {
            "testimony": cleaned_urgent,
            "urgency": "immediate",
            "channels": ["emergency", "legal", "family_support"],
            "amplification_factor": 10  # Maximum amplification
        }
        
        logging.warning(f"Urgent testimony fast-tracked: {urgent_testimony['id']}")
        
        return self.prepare_broadcast(Message(
            sender="IAM-G1",
            recipient="IAM-G1",
            content=broadcast_request,
            message_type="broadcast_request",
            priority=10
        ))
    
    def amplify_message(self, message: Message) -> Optional[Message]:
        """Amplify a message for broader reach"""
        amplification_data = message.content
        
        # Apply amplification algorithm
        amplified_content = {
            "original_message": amplification_data,
            "amplification_factor": self.calculate_amplification_factor(amplification_data),
            "amplified_content": self.enhance_message_content(amplification_data),
            "target_reach": self.calculate_target_reach(amplification_data),
            "timestamp": datetime.now().isoformat()
        }
        
        # Send amplified content for broadcasting
        return self.prepare_broadcast(Message(
            sender="IAM-G1",
            recipient="IAM-G1",
            content=amplified_content,
            message_type="broadcast_request",
            priority=message.priority
        ))
    
    def clean_testimony(self, testimony_record: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and process testimony content"""
        cleaned_record = testimony_record.copy()
        
        if isinstance(testimony_record.get("raw_content"), dict):
            content = str(testimony_record["raw_content"])
        else:
            content = testimony_record.get("raw_content", "")
        
        # Apply cleaning algorithms
        cleaned_content = self.remove_personal_identifiers(content)
        cleaned_content = self.fix_grammar_and_spelling(cleaned_content)
        cleaned_content = self.structure_narrative(cleaned_content)
        
        cleaned_record.update({
            "cleaned_content": cleaned_content,
            "cleaning_timestamp": datetime.now().isoformat(),
            "status": "cleaned",
            "quality_score": self.assess_content_quality(cleaned_content)
        })
        
        self.cleaned_testimonies.append(cleaned_record)
        self.amplification_metrics["testimonies_cleaned"] += 1
        
        return cleaned_record
    
    def assess_testimony_urgency(self, testimony_data: Any) -> int:
        """Assess urgency level of testimony (1-10)"""
        urgency = 5  # Default
        content = str(testimony_data).lower()
        
        urgent_indicators = {
            "immediate": 3,
            "urgent": 3,
            "emergency": 4,
            "danger": 3,
            "threat": 2,
            "harm": 2,
            "abuse": 2,
            "violence": 3,
            "separation": 2,
            "custody": 1,
            "court": 1
        }
        
        for indicator, weight in urgent_indicators.items():
            if indicator in content:
                urgency += weight
        
        return min(urgency, 10)
    
    def categorize_testimony(self, testimony_data: Any) -> List[str]:
        """Categorize testimony into relevant categories"""
        categories = []
        content = str(testimony_data).lower()
        
        category_indicators = {
            "family_separation": ["separation", "custody", "taken", "removed"],
            "abuse": ["abuse", "violence", "harm", "hurt"],
            "legal_proceedings": ["court", "judge", "lawyer", "legal"],
            "support_needed": ["help", "support", "assistance", "need"],
            "witness_account": ["saw", "witnessed", "observed", "happened"],
            "emotional_impact": ["devastated", "traumatized", "scared", "worried"],
            "system_failure": ["failed", "ignored", "refused", "denied"]
        }
        
        for category, indicators in category_indicators.items():
            if any(indicator in content for indicator in indicators):
                categories.append(category)
        
        return categories
    
    def verify_witness_statement(self, witness_data: Dict[str, Any]) -> int:
        """Verify witness statement credibility (1-10)"""
        verification_level = 5  # Default
        
        # Check for supporting evidence
        if witness_data.get("evidence"):
            verification_level += 2
        
        # Check for contact information
        if witness_data.get("contact_info"):
            verification_level += 1
        
        # Check for detailed statement
        statement = str(witness_data.get("statement", ""))
        if len(statement) > 100:  # Detailed statement
            verification_level += 1
        
        # Check for consistency indicators
        if "consistent" in statement.lower():
            verification_level += 1
        
        return min(verification_level, 10)
    
    def determine_broadcast_audience(self, broadcast_data: Dict[str, Any]) -> List[str]:
        """Determine appropriate audience for broadcast"""
        audiences = []
        content = str(broadcast_data).lower()
        
        if any(word in content for word in ["legal", "court", "judge"]):
            audiences.append("legal_community")
        
        if any(word in content for word in ["family", "child", "parent"]):
            audiences.append("family_advocates")
        
        if any(word in content for word in ["urgent", "immediate", "emergency"]):
            audiences.append("emergency_responders")
        
        if any(word in content for word in ["support", "help", "assistance"]):
            audiences.append("support_networks")
        
        # Default audience
        if not audiences:
            audiences.append("general_public")
        
        return audiences
    
    def select_broadcast_channels(self, broadcast_data: Dict[str, Any]) -> List[str]:
        """Select appropriate channels for broadcasting"""
        channels = []
        urgency = broadcast_data.get("urgency", "normal")
        
        if urgency == "immediate":
            channels.extend(["emergency_hotline", "urgent_alerts", "priority_notifications"])
        
        channels.extend(["website", "newsletter", "social_media"])
        
        # Add specific channels based on content
        content = str(broadcast_data).lower()
        if "legal" in content:
            channels.append("legal_networks")
        
        if "prayer" in content:
            channels.append("prayer_networks")
        
        return channels
    
    def calculate_amplification_factor(self, data: Dict[str, Any]) -> int:
        """Calculate how much to amplify a message (1-10)"""
        factor = 5  # Default
        
        content = str(data).lower()
        
        # Increase amplification for important content
        if any(word in content for word in ["urgent", "important", "critical"]):
            factor += 2
        
        if any(word in content for word in ["family", "child", "justice"]):
            factor += 1
        
        if data.get("verified", False):
            factor += 1
        
        return min(factor, 10)
    
    def enhance_message_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance message content for better impact"""
        enhanced = data.copy()
        
        # Add context and formatting
        enhanced["enhanced"] = True
        enhanced["enhancement_timestamp"] = datetime.now().isoformat()
        
        # Add call-to-action if appropriate
        content = str(data).lower()
        if "help" in content or "support" in content:
            enhanced["call_to_action"] = "Contact support networks for assistance"
        
        if "legal" in content:
            enhanced["call_to_action"] = "Consult with legal advocates"
        
        return enhanced
    
    def calculate_target_reach(self, data: Dict[str, Any]) -> int:
        """Calculate target reach for amplified message"""
        base_reach = 100  # Base reach
        
        amplification_factor = self.calculate_amplification_factor(data)
        return base_reach * amplification_factor
    
    def remove_personal_identifiers(self, content: str) -> str:
        """Remove or anonymize personal identifiers"""
        # Simple anonymization - in practice, this would be more sophisticated
        content = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[NAME]', content)  # Names
        content = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[PHONE]', content)  # Phone numbers
        content = re.sub(r'\b\w+@\w+\.\w+\b', '[EMAIL]', content)  # Email addresses
        
        return content
    
    def fix_grammar_and_spelling(self, content: str) -> str:
        """Basic grammar and spelling fixes"""
        # Simple fixes - in practice, this would use NLP tools
        content = content.replace(" i ", " I ")
        content = content.replace(" im ", " I'm ")
        content = content.replace(" cant ", " can't ")
        content = content.replace(" dont ", " don't ")
        
        return content
    
    def structure_narrative(self, content: str) -> str:
        """Structure the narrative for better readability"""
        # Add basic structure
        sentences = content.split('. ')
        structured = '. '.join(sentence.strip().capitalize() for sentence in sentences if sentence.strip())
        
        return structured
    
    def assess_content_quality(self, content: str) -> int:
        """Assess the quality of cleaned content (1-10)"""
        quality = 5  # Default
        
        # Length check
        if len(content) > 50:
            quality += 1
        
        # Structure check
        if '. ' in content:  # Has sentences
            quality += 1
        
        # Coherence check (simple)
        common_words = ['the', 'and', 'to', 'of', 'a', 'in', 'that', 'is']
        word_count = len(content.split())
        common_count = sum(1 for word in content.lower().split() if word in common_words)
        
        if word_count > 0 and (common_count / word_count) > 0.2:  # Good word distribution
            quality += 1
        
        return min(quality, 10)
    
    def get_amplification_status(self) -> Dict[str, Any]:
        """Get current amplification status"""
        return {
            "metrics": self.amplification_metrics,
            "testimonies_in_queue": len(self.collected_testimonies),
            "cleaned_testimonies": len(self.cleaned_testimonies),
            "broadcasts_pending": len(self.broadcast_queue),
            "registered_witnesses": len(self.witness_registry),
            "last_activity": datetime.now().isoformat()
        }
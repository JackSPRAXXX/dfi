"""
Michael Node (IAM-M1) - Protection Algorithm v1.0
Encrypts & secures testimonies; flags urgent risks
"""

import hashlib
import json
import logging
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from divine_court import ArchangelNode, Message


class MichaelNode(ArchangelNode):
    """IAM-M1: Michael Node - Protection and Security"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.encrypted_testimonies = {}
        self.security_alerts = []
        self.threat_assessments = {}
        self.protection_protocols = {
            "encryption_enabled": True,
            "threat_monitoring": True,
            "urgent_escalation": True,
            "security_audit": True
        }
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming messages with protection protocols"""
        logging.info(f"Michael processing: {message.message_type} from {message.sender}")
        
        if message.message_type == "testimony":
            return self.secure_testimony(message)
        elif message.message_type == "threat_assessment":
            return self.assess_threat(message)
        elif message.message_type == "security_check":
            return self.perform_security_check(message)
        elif message.message_type == "urgent_response":
            return self.handle_urgent_security(message)
        
        # Default processing for other message types
        return self.apply_security_filter(message)
    
    def secure_testimony(self, message: Message) -> Optional[Message]:
        """Encrypt and secure testimony data"""
        testimony_data = message.content
        
        # Generate secure hash for testimony
        testimony_str = json.dumps(testimony_data, sort_keys=True)
        testimony_hash = hashlib.sha256(testimony_str.encode()).hexdigest()
        
        # Create encrypted record
        encrypted_record = {
            "hash": testimony_hash,
            "timestamp": datetime.now().isoformat(),
            "sender": message.sender,
            "encrypted": True,
            "security_level": self.determine_security_level(testimony_data),
            "content_summary": self.create_secure_summary(testimony_data)
        }
        
        # Store encrypted testimony
        self.encrypted_testimonies[testimony_hash] = encrypted_record
        
        logging.info(f"Testimony secured with hash: {testimony_hash[:8]}...")
        
        # Send to Cherubim for archiving
        return self.send_message(
            "IAM-C1",
            {
                "action": "archive_secure_testimony",
                "testimony_hash": testimony_hash,
                "security_metadata": encrypted_record
            },
            "secure_archival",
            8
        )
    
    def assess_threat(self, message: Message) -> Optional[Message]:
        """Assess and categorize threats"""
        threat_data = message.content
        threat_id = f"THREAT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Analyze threat level
        threat_assessment = {
            "threat_id": threat_id,
            "source": message.sender,
            "timestamp": datetime.now().isoformat(),
            "threat_level": self.calculate_threat_level(threat_data),
            "risk_factors": self.identify_risk_factors(threat_data),
            "recommended_actions": self.recommend_security_actions(threat_data),
            "escalation_required": False
        }
        
        # Determine if escalation is needed
        if threat_assessment["threat_level"] >= 8:
            threat_assessment["escalation_required"] = True
            self.security_alerts.append(threat_assessment)
            
            # Send urgent alert to central hub
            return self.send_message(
                "IAM-0",
                {
                    "alert_type": "HIGH_THREAT",
                    "threat_assessment": threat_assessment,
                    "immediate_action_required": True
                },
                "urgent_alert",
                10
            )
        
        # Store threat assessment
        self.threat_assessments[threat_id] = threat_assessment
        
        return self.send_message(
            "IAM-0",
            threat_assessment,
            "threat_report",
            threat_assessment["threat_level"]
        )
    
    def perform_security_check(self, message: Message) -> Optional[Message]:
        """Perform comprehensive security check"""
        check_results = {
            "timestamp": datetime.now().isoformat(),
            "encrypted_testimonies_count": len(self.encrypted_testimonies),
            "active_threats": len([t for t in self.threat_assessments.values() 
                                 if t["threat_level"] >= 5]),
            "security_alerts": len(self.security_alerts),
            "system_integrity": "SECURE",
            "recommendations": []
        }
        
        # Check for security issues
        if check_results["active_threats"] > 10:
            check_results["recommendations"].append("High threat count - review security protocols")
        
        if len(self.security_alerts) > 5:
            check_results["recommendations"].append("Multiple security alerts - investigate patterns")
        
        return self.send_message(
            message.sender,
            check_results,
            "security_report",
            6
        )
    
    def handle_urgent_security(self, message: Message) -> Optional[Message]:
        """Handle urgent security situations"""
        urgent_data = message.content
        
        # Immediate security response
        response = {
            "response_id": f"SEC_RESP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "original_alert": urgent_data,
            "security_measures_activated": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Activate appropriate security measures
        if "encryption" in str(urgent_data).lower():
            response["security_measures_activated"].append("Enhanced encryption protocols")
        
        if "breach" in str(urgent_data).lower():
            response["security_measures_activated"].append("Breach containment procedures")
            response["security_measures_activated"].append("Audit trail analysis")
        
        if "testimony" in str(urgent_data).lower():
            response["security_measures_activated"].append("Testimony protection lockdown")
        
        logging.warning(f"Michael urgent response activated: {response['response_id']}")
        
        return self.send_message(
            "IAM-0",
            response,
            "security_response",
            10
        )
    
    def apply_security_filter(self, message: Message) -> Optional[Message]:
        """Apply general security filtering to any message"""
        # Check message for security concerns
        security_score = self.calculate_message_security_score(message)
        
        if security_score < 5:
            # Message has security concerns
            return self.send_message(
                "IAM-S1",  # Send to Seraphim for purity check
                {
                    "security_concern": True,
                    "original_message": message.content,
                    "security_score": security_score,
                    "sender": message.sender
                },
                "security_review",
                7
            )
        
        return None
    
    def determine_security_level(self, data: Any) -> int:
        """Determine security level for data (1-10)"""
        security_level = 5  # Default
        
        data_str = str(data).lower()
        
        # Increase security level based on content
        if any(word in data_str for word in ["child", "family", "abuse", "threat"]):
            security_level += 2
        
        if any(word in data_str for word in ["urgent", "immediate", "danger"]):
            security_level += 2
        
        if any(word in data_str for word in ["confidential", "sensitive", "private"]):
            security_level += 1
        
        return min(security_level, 10)
    
    def create_secure_summary(self, data: Any) -> str:
        """Create a secure summary that doesn't expose sensitive details"""
        data_str = str(data)
        
        # Create summary without exposing sensitive information
        summary_parts = []
        
        if "testimony" in data_str.lower():
            summary_parts.append("Testimony data")
        if "family" in data_str.lower():
            summary_parts.append("Family-related")
        if "urgent" in data_str.lower():
            summary_parts.append("Urgent matter")
        
        return " | ".join(summary_parts) if summary_parts else "Protected content"
    
    def calculate_threat_level(self, threat_data: Any) -> int:
        """Calculate threat level (1-10)"""
        threat_level = 1
        threat_str = str(threat_data).lower()
        
        # Threat level indicators
        high_risk_words = ["immediate", "danger", "violence", "threat", "harm"]
        medium_risk_words = ["concern", "issue", "problem", "risk"]
        
        for word in high_risk_words:
            if word in threat_str:
                threat_level += 3
        
        for word in medium_risk_words:
            if word in threat_str:
                threat_level += 1
        
        return min(threat_level, 10)
    
    def identify_risk_factors(self, threat_data: Any) -> List[str]:
        """Identify specific risk factors in threat data"""
        risk_factors = []
        threat_str = str(threat_data).lower()
        
        risk_indicators = {
            "physical_threat": ["violence", "harm", "attack", "assault"],
            "privacy_breach": ["leak", "exposure", "breach", "unauthorized"],
            "system_threat": ["hack", "malware", "virus", "intrusion"],
            "family_threat": ["separation", "custody", "removal", "taken"]
        }
        
        for risk_type, indicators in risk_indicators.items():
            if any(indicator in threat_str for indicator in indicators):
                risk_factors.append(risk_type)
        
        return risk_factors
    
    def recommend_security_actions(self, threat_data: Any) -> List[str]:
        """Recommend security actions based on threat"""
        actions = []
        risk_factors = self.identify_risk_factors(threat_data)
        
        if "physical_threat" in risk_factors:
            actions.append("Contact law enforcement")
            actions.append("Implement physical security measures")
        
        if "privacy_breach" in risk_factors:
            actions.append("Enhance encryption protocols")
            actions.append("Conduct security audit")
        
        if "system_threat" in risk_factors:
            actions.append("Isolate affected systems")
            actions.append("Run malware scan")
        
        if "family_threat" in risk_factors:
            actions.append("Alert family support network")
            actions.append("Document all evidence")
        
        return actions
    
    def calculate_message_security_score(self, message: Message) -> int:
        """Calculate security score for a message (1-10, 10 being most secure)"""
        score = 10  # Start with highest security
        
        content_str = str(message.content).lower()
        
        # Reduce score for concerning content
        if any(word in content_str for word in ["password", "key", "secret"]):
            score -= 3
        
        if any(word in content_str for word in ["unsecure", "public", "open"]):
            score -= 2
        
        if message.priority >= 8:  # High priority messages need more security
            score -= 1
        
        return max(score, 1)
    
    def get_protection_status(self) -> Dict[str, Any]:
        """Get current protection status"""
        return {
            "encrypted_testimonies": len(self.encrypted_testimonies),
            "active_threats": len([t for t in self.threat_assessments.values() 
                                 if t["threat_level"] >= 5]),
            "security_alerts": len(self.security_alerts),
            "protection_protocols": self.protection_protocols,
            "last_security_check": datetime.now().isoformat()
        }
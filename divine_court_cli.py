#!/usr/bin/env python3
"""
Divine Court CLI - Command line interface for the I·AM Companions system
"""

import json
import argparse
import logging
from datetime import datetime
from typing import Dict, Any

from divine_court import DivineCourtSystem


class DivineCourtCLI:
    """Command line interface for Divine Court system"""
    
    def __init__(self, config_path: str = "companions.json"):
        self.system = DivineCourtSystem(config_path)
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('divine_court.log')
            ]
        )
    
    def status(self):
        """Display system status"""
        print("🌟 Divine Court System Status")
        print("=" * 50)
        
        status = self.system.get_system_status()
        
        if "error" in status:
            print(f"❌ Error: {status['error']}")
            return
        
        # Central Hub Status
        hub_status = status.get("central_hub", {})
        print(f"📊 Central Hub (IAM-0): {'🟢 Active' if hub_status.get('active') else '🔴 Inactive'}")
        print(f"   Queue Length: {hub_status.get('queue_length', 0)}")
        print(f"   Processed Messages: {hub_status.get('processed_count', 0)}")
        
        # Metrics
        metrics = status.get("metrics", {})
        print(f"\n📈 System Metrics:")
        print(f"   FSI Score: {metrics.get('fsi_score', 0):.2f}")
        print(f"   DDI Score: {metrics.get('ddi_score', 0):.2f}")
        print(f"   Total Messages: {metrics.get('total_messages', 0)}")
        print(f"   Active Companions: {metrics.get('active_companions', 0)}")
        print(f"   Urgent Alerts: {metrics.get('urgent_alerts', 0)}")
        
        # Companions Status
        companions = status.get("companions", {})
        print(f"\n👥 Companions Status ({len(companions)} total):")
        
        # Group by tiers
        tier1 = ["IAM-M1", "IAM-G1", "IAM-R1", "IAM-U1", "IAM-S1"]
        tier2 = ["IAM-C1", "IAM-V1", "IAM-D1"]
        tier3 = ["IAM-W1", "IAM-I1", "IAM-B1"]
        
        self._display_tier_status("🔥 Tier 1 (Archangel Nodes)", tier1, companions)
        self._display_tier_status("⚔️ Tier 2 (Guardian Nodes)", tier2, companions)
        self._display_tier_status("📡 Tier 3 (Messenger Nodes)", tier3, companions)
    
    def _display_tier_status(self, tier_name: str, tier_codes: list, companions: Dict[str, Any]):
        """Display status for a specific tier"""
        print(f"\n   {tier_name}:")
        for code in tier_codes:
            if code in companions:
                comp = companions[code]
                active_icon = "🟢" if comp.get("active") else "🔴"
                print(f"     {code}: {active_icon} Queue: {comp.get('queue_length', 0)} | Processed: {comp.get('processed_count', 0)}")
            else:
                print(f"     {code}: ❓ Not found")
    
    def send_message(self, recipient: str, content: str, message_type: str = "standard", priority: int = 5):
        """Send a message to a specific companion"""
        print(f"📤 Sending message to {recipient}...")
        
        try:
            # Parse content as JSON if possible
            try:
                content_data = json.loads(content)
            except json.JSONDecodeError:
                content_data = {"message": content}
            
            self.system.inject_message(recipient, content_data, message_type, priority)
            print(f"✅ Message sent successfully to {recipient}")
            
            # Run a cycle to process the message
            print("🔄 Processing message...")
            status = self.system.run_cycle()
            
            print(f"📊 System processed {status.get('metrics', {}).get('total_messages', 0)} total messages")
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
    
    def simulate_testimony(self, content: str, urgency: str = "normal"):
        """Simulate receiving a testimony"""
        print(f"📝 Simulating testimony reception...")
        
        urgency_levels = {
            "low": 3,
            "normal": 5,
            "high": 7,
            "urgent": 9,
            "emergency": 10
        }
        
        priority = urgency_levels.get(urgency.lower(), 5)
        
        testimony_data = {
            "testimony": content,
            "timestamp": datetime.now().isoformat(),
            "urgency": urgency,
            "source": "CLI_simulation"
        }
        
        # Send to Gabriel for testimony processing
        self.send_message("IAM-G1", json.dumps(testimony_data), "raw_testimony", priority)
    
    def simulate_threat(self, threat_description: str, severity: str = "medium"):
        """Simulate a security threat"""
        print(f"🚨 Simulating threat assessment...")
        
        severity_levels = {
            "low": 3,
            "medium": 6,
            "high": 8,
            "critical": 10
        }
        
        priority = severity_levels.get(severity.lower(), 6)
        
        threat_data = {
            "threat_description": threat_description,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "source": "CLI_simulation"
        }
        
        # Send to Michael for threat assessment
        self.send_message("IAM-M1", json.dumps(threat_data), "threat_assessment", priority)
    
    def analyze_patterns(self):
        """Request pattern analysis from Uriel"""
        print("🔍 Requesting pattern analysis...")
        
        analysis_request = {
            "analysis_type": "comprehensive",
            "period": "last_30_days",
            "timestamp": datetime.now().isoformat()
        }
        
        self.send_message("IAM-U1", json.dumps(analysis_request), "pattern_request", 7)
    
    def run_cycle(self):
        """Run one coordination cycle"""
        print("🔄 Running system coordination cycle...")
        
        status = self.system.run_cycle()
        
        print("✅ Coordination cycle completed")
        print(f"📊 Current system status:")
        print(f"   Active companions: {status.get('metrics', {}).get('active_companions', 0)}")
        print(f"   Total messages processed: {status.get('metrics', {}).get('total_messages', 0)}")
        print(f"   FSI Score: {status.get('metrics', {}).get('fsi_score', 0):.2f}")
        print(f"   DDI Score: {status.get('metrics', {}).get('ddi_score', 0):.2f}")
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("🌟 Divine Court Interactive Mode")
        print("Type 'help' for commands or 'exit' to quit")
        print("=" * 50)
        
        while True:
            try:
                command = input("\nDivine Court> ").strip()
                
                if command.lower() in ['exit', 'quit']:
                    print("👋 Exiting Divine Court CLI")
                    break
                
                elif command.lower() == 'help':
                    self._show_help()
                
                elif command.lower() == 'status':
                    self.status()
                
                elif command.lower() == 'cycle':
                    self.run_cycle()
                
                elif command.lower() == 'patterns':
                    self.analyze_patterns()
                
                elif command.startswith('testimony '):
                    content = command[10:]  # Remove 'testimony '
                    self.simulate_testimony(content)
                
                elif command.startswith('threat '):
                    content = command[7:]  # Remove 'threat '
                    self.simulate_threat(content)
                
                elif command.startswith('send '):
                    parts = command[5:].split(' ', 2)  # Remove 'send '
                    if len(parts) >= 2:
                        recipient = parts[0]
                        message_content = parts[1] if len(parts) == 2 else ' '.join(parts[1:])
                        self.send_message(recipient, message_content)
                    else:
                        print("❌ Usage: send <recipient> <message>")
                
                elif command.strip():
                    print(f"❓ Unknown command: {command}")
                    print("Type 'help' for available commands")
                
            except KeyboardInterrupt:
                print("\n👋 Exiting Divine Court CLI")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_help(self):
        """Show help information"""
        print("""
🌟 Divine Court CLI Commands:

Basic Commands:
  status          - Show system status
  cycle           - Run one coordination cycle
  patterns        - Request pattern analysis
  help            - Show this help message
  exit/quit       - Exit the CLI

Message Commands:
  send <recipient> <message>     - Send message to specific companion
  testimony <content>            - Simulate testimony input
  threat <description>           - Simulate threat assessment

Examples:
  testimony "Family separated by court order without justification"
  threat "Unauthorized access to testimony database"
  send IAM-G1 "{"test": "message"}"

Available Recipients:
  IAM-0   - Central Hub
  IAM-M1  - Michael (Protection)
  IAM-G1  - Gabriel (Testimony)
  IAM-R1  - Raphael (Healing)
  IAM-U1  - Uriel (Analytics)
  IAM-S1  - Seraphim (Purity)
  IAM-C1  - Cherubim (Archive)
  IAM-V1  - Virtues (Connections)
  IAM-D1  - Dominions (Legal)
  IAM-W1  - Watchers (Intelligence)
  IAM-I1  - Intercessors (Prayer)
  IAM-B1  - Builders (Infrastructure)
        """)


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Divine Court I·AM Companions CLI")
    parser.add_argument("--config", default="companions.json", help="Configuration file path")
    parser.add_argument("--command", choices=["status", "cycle", "patterns", "interactive"], 
                       default="interactive", help="Command to run")
    parser.add_argument("--send-to", help="Send message to specific companion")
    parser.add_argument("--message", help="Message content to send")
    parser.add_argument("--testimony", help="Simulate testimony input")
    parser.add_argument("--threat", help="Simulate threat assessment")
    
    args = parser.parse_args()
    
    try:
        cli = DivineCourtCLI(args.config)
        
        if args.command == "status":
            cli.status()
        elif args.command == "cycle":
            cli.run_cycle()
        elif args.command == "patterns":
            cli.analyze_patterns()
        elif args.send_to and args.message:
            cli.send_message(args.send_to, args.message)
        elif args.testimony:
            cli.simulate_testimony(args.testimony)
        elif args.threat:
            cli.simulate_threat(args.threat)
        else:
            cli.interactive_mode()
            
    except FileNotFoundError:
        print("❌ Configuration file not found. Please ensure companions.json exists.")
    except Exception as e:
        print(f"❌ Error initializing Divine Court: {e}")


if __name__ == "__main__":
    main()
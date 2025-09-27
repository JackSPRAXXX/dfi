#!/usr/bin/env python3
"""
Divine Court System Demonstration
Shows the I·AM Companions in action
"""

import time
import json
from divine_court_cli import DivineCourtCLI


def run_demo():
    """Run a comprehensive demonstration of the Divine Court system"""
    print("🌟 DIVINE COURT I·AM COMPANIONS DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Initialize the system
    print("🚀 Initializing Divine Court System...")
    cli = DivineCourtCLI()
    print("✅ System initialized successfully!")
    print()
    
    # Show initial status
    print("📊 Initial System Status:")
    cli.status()
    print()
    
    # Simulate testimony input
    print("📝 SCENARIO 1: Testimony Collection")
    print("-" * 40)
    print("👤 A family provides testimony about separation...")
    
    testimony = """
    My children were removed from my care by family court without proper due process.
    The judge ignored clear evidence that the allegations were false.
    I have been fighting for 18 months to see my children.
    The system has failed my family completely.
    """
    
    cli.simulate_testimony(testimony.strip(), "high")
    print("✅ Testimony processed by Gabriel (IAM-G1)")
    print()
    
    # Simulate threat assessment
    print("🚨 SCENARIO 2: Security Threat")
    print("-" * 40)
    print("🔒 Security threat detected...")
    
    threat = """
    Unauthorized attempt to access encrypted testimony database.
    Multiple failed login attempts from suspicious IP addresses.
    Potential data breach in progress.
    """
    
    cli.simulate_threat(threat.strip(), "high")
    print("✅ Threat processed by Michael (IAM-M1)")
    print()
    
    # Run pattern analysis
    print("🔍 SCENARIO 3: Pattern Analysis")
    print("-" * 40)
    print("📈 Requesting comprehensive pattern analysis...")
    
    cli.analyze_patterns()
    print("✅ Pattern analysis requested from Uriel (IAM-U1)")
    print()
    
    # Run coordination cycle
    print("🔄 SCENARIO 4: System Coordination")
    print("-" * 40)
    print("⚙️ Running system coordination cycle...")
    
    cli.run_cycle()
    print("✅ Coordination cycle completed")
    print()
    
    # Show final status
    print("📊 Final System Status:")
    cli.status()
    print()
    
    # Summary
    print("🎯 DEMONSTRATION SUMMARY")
    print("=" * 60)
    print("✅ Divine Court system successfully demonstrated key capabilities:")
    print("   • Testimony collection and processing (Gabriel)")
    print("   • Security threat assessment (Michael)")
    print("   • Pattern analysis and analytics (Uriel)")
    print("   • System coordination and monitoring (Central Hub)")
    print()
    print("🌟 The I·AM Companions are ready to serve justice and dignity!")
    print()


def show_companion_details():
    """Show detailed information about each companion"""
    print("👥 I·AM COMPANIONS DETAILED OVERVIEW")
    print("=" * 60)
    
    companions = {
        "Tier 1 - Archangel Nodes (Strategic AI)": {
            "IAM-M1": {
                "name": "Michael Node",
                "algorithm": "Protection Algorithm v1.0",
                "purpose": "Encrypts & secures testimonies; flags urgent risks"
            },
            "IAM-G1": {
                "name": "Gabriel Node", 
                "algorithm": "Testimony Amplifier 2.1",
                "purpose": "Collects, cleans, and broadcasts witness statements"
            },
            "IAM-R1": {
                "name": "Raphael Node",
                "algorithm": "Healing Matrix 3.2", 
                "purpose": "Tracks wellbeing, prayer requests, support needs"
            },
            "IAM-U1": {
                "name": "Uriel Node",
                "algorithm": "Pattern Illuminator 4.0",
                "purpose": "FSI/DDI analytics, hotspot mapping, predictive alerts"
            },
            "IAM-S1": {
                "name": "Seraphim Node",
                "algorithm": "Purity Engine 1.5",
                "purpose": "Filters actions for dignity alignment; prevents burnout"
            }
        },
        "Tier 2 - Guardian Nodes (Operational AI)": {
            "IAM-C1": {
                "name": "Cherubim Team",
                "algorithm": "Immutable Archive 7.7",
                "purpose": "Stores evidence securely, timestamps every record"
            },
            "IAM-V1": {
                "name": "Virtues Team",
                "algorithm": "Volunteer Matcher 3.4",
                "purpose": "Connects people, lawyers, prayer lines, and families"
            },
            "IAM-D1": {
                "name": "Dominions Team", 
                "algorithm": "Legal Action Generator 5.5",
                "purpose": "Drafts filings, complaints, and policy proposals"
            }
        },
        "Tier 3 - Messenger Nodes (Field AI)": {
            "IAM-W1": {
                "name": "Watchers",
                "algorithm": "Real-Time Intel Gatherer 2.8",
                "purpose": "Receives on-the-ground updates from families & advocates"
            },
            "IAM-I1": {
                "name": "Intercessors",
                "algorithm": "Prayer Flow 1.9", 
                "purpose": "Sends daily messages, meditations, and morale support"
            },
            "IAM-B1": {
                "name": "Builders",
                "algorithm": "InfraCreator 6.6",
                "purpose": "Builds dashboards, maintains websites, keeps comms secure"
            }
        }
    }
    
    for tier_name, tier_companions in companions.items():
        print(f"\n🔥 {tier_name}")
        print("-" * 50)
        
        for code, details in tier_companions.items():
            print(f"  {code} - {details['name']}")
            print(f"    Algorithm: {details['algorithm']}")
            print(f"    Purpose: {details['purpose']}")
            print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "details":
        show_companion_details()
    else:
        run_demo()
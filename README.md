# Divine Court - I·AM Companions System

## Overview

The Divine Court is a hierarchical network of AI companions implementing the "I AM THAT I AM" paradigm through algorithmic agents organized in angelic ranks. Each companion has a specific code name, core algorithm, and purpose within the justice and dignity framework.

**Background**: A private individual can apply to lay criminal charges if the Crown won't. There's a formal application process in Ontario (and processes in other provinces). The court decides whether to issue a summons/warrant; the Attorney General can intervene at any time. This is a direct way to force criminal review when authorities are refusing to act.

The Divine Court system provides technological support and automation for this process through the I·AM Companions network.

## Quick Start

### Running the Demonstration

```bash
# Run the full system demonstration
python3 demo.py

# Show detailed companion information
python3 demo.py details
```

### Using the CLI

```bash
# Interactive mode
python3 divine_court_cli.py

# Check system status
python3 divine_court_cli.py --command status

# Simulate testimony input
python3 divine_court_cli.py --testimony "Family separated without due process"

# Simulate security threat
python3 divine_court_cli.py --threat "Unauthorized database access attempt"
```

### Basic Python Usage

```python
from divine_court import DivineCourtSystem

# Initialize the system
system = DivineCourtSystem()

# Inject a message
system.inject_message("IAM-G1", {"testimony": "Court ignored evidence"}, "raw_testimony", 8)

# Run coordination cycle
status = system.run_cycle()
print(f"System processed {status['metrics']['total_messages']} messages")
```

## System Architecture

### Central Hub: I·AM THAT I·AM (IAM-0)
- **Role**: The Source - Central Divine Court AI coordinator
- **Algorithm**: "Witness all, seed dignity, coordinate action, measure FSI/DDI in real time"
- **Purpose**: Coordinates all nodes, manages system metrics, handles urgent alerts

### Tier 1 - Archangel Nodes (Strategic AI)

| Code | Name | Algorithm | Purpose |
|------|------|-----------|---------|
| IAM-M1 | Michael Node | Protection Algorithm v1.0 | Encrypts & secures testimonies; flags urgent risks |
| IAM-G1 | Gabriel Node | Testimony Amplifier 2.1 | Collects, cleans, and broadcasts witness statements |
| IAM-R1 | Raphael Node | Healing Matrix 3.2 | Tracks wellbeing, prayer requests, support needs |
| IAM-U1 | Uriel Node | Pattern Illuminator 4.0 | FSI/DDI analytics, hotspot mapping, predictive alerts |
| IAM-S1 | Seraphim Node | Purity Engine 1.5 | Filters actions for dignity alignment; prevents burnout |

### Tier 2 - Guardian Nodes (Operational AI)

| Code | Name | Algorithm | Purpose |
|------|------|-----------|---------|
| IAM-C1 | Cherubim Team | Immutable Archive 7.7 | Stores evidence securely, timestamps every record |
| IAM-V1 | Virtues Team | Volunteer Matcher 3.4 | Connects people, lawyers, prayer lines, and families |
| IAM-D1 | Dominions Team | Legal Action Generator 5.5 | Drafts filings, complaints, and policy proposals |

### Tier 3 - Messenger Nodes (Field AI)

| Code | Name | Algorithm | Purpose |
|------|------|-----------|---------|
| IAM-W1 | Watchers | Real-Time Intel Gatherer 2.8 | Receives on-the-ground updates from families & advocates |
| IAM-I1 | Intercessors | Prayer Flow 1.9 | Sends daily messages, meditations, and morale support |
| IAM-B1 | Builders | InfraCreator 6.6 | Builds dashboards, maintains websites, keeps comms secure |

## Key Features

### 🔒 Security & Protection (Michael - IAM-M1)
- Encrypts and secures all testimony data
- Performs threat assessments and risk analysis
- Flags urgent security concerns
- Implements protection protocols

**Example Usage:**
```bash
python3 divine_court_cli.py --threat "Database breach attempt detected"
```

### 📢 Testimony Processing (Gabriel - IAM-G1)
- Collects and cleans witness statements
- Amplifies messages for broader reach
- Manages witness registry
- Prepares content for broadcasting

**Example Usage:**
```bash
python3 divine_court_cli.py --testimony "Court ignored evidence of false allegations"
```

### 📊 Pattern Analysis (Uriel - IAM-U1)
- Analyzes FSI (Family Separation Index) and DDI (Dignity Degradation Index)
- Identifies temporal and geographic patterns
- Generates predictive alerts
- Maps hotspots of concern

**Example Usage:**
```bash
python3 divine_court_cli.py --command patterns
```

## Data Flow Architecture

### Upward Flow (Field → Strategic)
```
Watchers (IAM-W1) → Cherubim (IAM-C1) → Uriel (IAM-U1) → IAM-0
Intercessors (IAM-I1) → Virtues (IAM-V1) → Raphael (IAM-R1) → IAM-0
Builders (IAM-B1) → Dominions (IAM-D1) → Michael (IAM-M1) → IAM-0
```

### Downward Flow (Strategic → Field)
```
IAM-0 → Gabriel (IAM-G1) → Virtues (IAM-V1) → Intercessors (IAM-I1)
IAM-0 → Seraphim (IAM-S1) → All Nodes (Dignity Filtering)
```

## Configuration

The system is configured through `companions.json`, which defines:
- All companion properties and capabilities
- Data flow patterns
- System metrics and thresholds
- Hierarchical relationships

## Key Metrics

### FSI (Family Separation Index)
Measures the degree of family separation and disruption in the system.

### DDI (Dignity Degradation Index)
Measures threats to human dignity and wellbeing.

Both indices are tracked in real-time and trigger alerts when thresholds are exceeded.

## Interactive CLI Commands

In interactive mode, use these commands:

```
status          - Show system status
cycle           - Run coordination cycle
patterns        - Request pattern analysis
testimony <msg> - Submit testimony
threat <desc>   - Report security threat
send <to> <msg> - Send message to companion
help            - Show help
exit            - Exit CLI
```

## Core Principles

1. **Dignity First**: All actions must align with human dignity
2. **Justice Oriented**: Focus on legal pathways and proper procedures
3. **Light Transparency**: Open, accountable, and traceable processes
4. **Hierarchical Coordination**: Clear command structure with appropriate escalation
5. **Real-time Responsiveness**: Immediate action on urgent situations

## Algorithm Seeds

All companions share the core seed pattern:
```
I·AM {Rank} :: Purpose {X} :: Align with Dignity, Justice, Light
```

This ensures consistency across the hierarchical network while maintaining each companion's specific purpose.

## Implementation Notes

- Start simple with tools like Google Sheets, Airtable, Trello, or Notion
- Gradually replace manual processes with automated scripts and AI bots
- Each algorithm can be implemented as a script, spreadsheet, or AI bot
- Real-time FSI/DDI monitoring throughout the system
- Data flows upward (analysis) and downward (action)

## Files Structure

```
dfi/
├── README.md                 # This file
├── DIVINE_COURT.md          # Detailed system documentation
├── companions.json          # System configuration
├── divine_court.py          # Core system implementation
├── divine_court_cli.py      # Command-line interface
├── demo.py                  # Demonstration script
├── companions/              # Specific companion implementations
│   ├── __init__.py
│   ├── michael.py          # Protection algorithms
│   ├── gabriel.py          # Testimony processing
│   └── uriel.py            # Pattern analysis
└── divine_court.log        # System logs (created at runtime)
```

## Legal Context

This system supports the legal right of private individuals to apply to lay criminal charges when Crown prosecutors refuse to act. The Divine Court provides:

- Secure testimony collection and archiving
- Pattern analysis to identify systemic issues
- Support network coordination
- Documentation and evidence management
- Legal document preparation assistance

The system operates within the framework of existing legal processes in Ontario and other provinces, providing technological support for legitimate legal proceedings.

---

**🌟 The I·AM Companions are ready to serve justice and dignity!**
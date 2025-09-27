"""
Uriel Node (IAM-U1) - Pattern Illuminator 4.0
FSI/DDI analytics, hotspot mapping, predictive alerts
"""

import logging
import statistics
from typing import Any, Optional, Dict, List, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from divine_court import ArchangelNode, Message


class UrielNode(ArchangelNode):
    """IAM-U1: Uriel Node - Pattern Analysis and Illumination"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
        # Analytics data stores
        self.case_data = []
        self.geographic_data = defaultdict(list)
        self.temporal_patterns = defaultdict(list)
        self.system_metrics_history = []
        
        # Current indices
        self.fsi_data = []  # Family Separation Index data points
        self.ddi_data = []  # Dignity Degradation Index data points
        
        # Pattern recognition results
        self.identified_patterns = []
        self.hotspots = {}
        self.predictive_alerts = []
        
        # Analytics configuration
        self.analytics_config = {
            "fsi_threshold": 7.0,
            "ddi_threshold": 8.0,
            "hotspot_threshold": 5,
            "pattern_confidence_threshold": 0.7,
            "prediction_horizon_days": 30
        }
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process incoming messages for pattern analysis"""
        logging.info(f"Uriel processing: {message.message_type} from {message.sender}")
        
        if message.message_type == "case_data":
            return self.analyze_case_data(message)
        elif message.message_type == "geographic_data":
            return self.process_geographic_data(message)
        elif message.message_type == "metric_update":
            return self.update_indices(message)
        elif message.message_type == "pattern_request":
            return self.generate_pattern_report(message)
        elif message.message_type == "hotspot_analysis":
            return self.analyze_hotspots(message)
        elif message.message_type == "predictive_analysis":
            return self.generate_predictions(message)
        
        # Default: extract patterns from any data
        return self.extract_patterns_from_message(message)
    
    def analyze_case_data(self, message: Message) -> Optional[Message]:
        """Analyze case data for patterns"""
        case_data = message.content
        
        # Create case record
        case_record = {
            "case_id": f"CASE_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "data": case_data,
            "timestamp": datetime.now().isoformat(),
            "source": message.sender,
            "analyzed": False,
            "patterns_found": []
        }
        
        self.case_data.append(case_record)
        
        # Perform analysis
        analysis_results = self.perform_case_analysis(case_record)
        
        # Update FSI/DDI if case indicates family separation or dignity issues
        if "family_separation" in analysis_results.get("indicators", []):
            self.update_fsi(case_record, analysis_results)
        
        if "dignity_degradation" in analysis_results.get("indicators", []):
            self.update_ddi(case_record, analysis_results)
        
        # Check for urgent patterns
        if analysis_results.get("urgency_level", 0) >= 8:
            return self.send_message(
                "IAM-0",
                {
                    "alert_type": "URGENT_PATTERN",
                    "case_id": case_record["case_id"],
                    "analysis": analysis_results,
                    "recommended_action": "immediate_review"
                },
                "urgent_alert",
                10
            )
        
        # Send analysis to central hub
        return self.send_message(
            "IAM-0",
            {
                "case_analysis": analysis_results,
                "patterns_identified": len(analysis_results.get("patterns", [])),
                "recommendations": analysis_results.get("recommendations", [])
            },
            "analysis_report",
            7
        )
    
    def process_geographic_data(self, message: Message) -> Optional[Message]:
        """Process geographic data for hotspot mapping"""
        geo_data = message.content
        
        location = geo_data.get("location", "unknown")
        incident_type = geo_data.get("incident_type", "general")
        severity = geo_data.get("severity", 5)
        
        # Store geographic data
        geo_record = {
            "location": location,
            "incident_type": incident_type,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "coordinates": geo_data.get("coordinates"),
            "details": geo_data.get("details", {})
        }
        
        self.geographic_data[location].append(geo_record)
        
        # Check for hotspot formation
        hotspot_analysis = self.check_hotspot_formation(location)
        
        if hotspot_analysis["is_hotspot"]:
            return self.send_message(
                "IAM-0",
                {
                    "alert_type": "HOTSPOT_DETECTED",
                    "location": location,
                    "hotspot_data": hotspot_analysis,
                    "recommended_action": "increased_monitoring"
                },
                "hotspot_alert",
                8
            )
        
        return None
    
    def update_indices(self, message: Message) -> Optional[Message]:
        """Update FSI/DDI indices with new data"""
        metric_data = message.content
        
        current_time = datetime.now()
        
        if "fsi" in metric_data:
            fsi_point = {
                "value": metric_data["fsi"],
                "timestamp": current_time.isoformat(),
                "source": message.sender,
                "context": metric_data.get("context", {})
            }
            self.fsi_data.append(fsi_point)
            
            # Trim old data (keep last 1000 points)
            if len(self.fsi_data) > 1000:
                self.fsi_data = self.fsi_data[-1000:]
        
        if "ddi" in metric_data:
            ddi_point = {
                "value": metric_data["ddi"],
                "timestamp": current_time.isoformat(),
                "source": message.sender,
                "context": metric_data.get("context", {})
            }
            self.ddi_data.append(ddi_point)
            
            # Trim old data
            if len(self.ddi_data) > 1000:
                self.ddi_data = self.ddi_data[-1000:]
        
        # Calculate trends
        trends = self.calculate_index_trends()
        
        # Generate alerts if indices exceed thresholds
        alerts = []
        
        current_fsi = self.get_current_fsi()
        current_ddi = self.get_current_ddi()
        
        if current_fsi >= self.analytics_config["fsi_threshold"]:
            alerts.append({
                "type": "FSI_THRESHOLD_EXCEEDED",
                "current_value": current_fsi,
                "threshold": self.analytics_config["fsi_threshold"],
                "trend": trends.get("fsi_trend", "stable")
            })
        
        if current_ddi >= self.analytics_config["ddi_threshold"]:
            alerts.append({
                "type": "DDI_THRESHOLD_EXCEEDED",
                "current_value": current_ddi,
                "threshold": self.analytics_config["ddi_threshold"],
                "trend": trends.get("ddi_trend", "stable")
            })
        
        if alerts:
            return self.send_message(
                "IAM-0",
                {
                    "metric_alerts": alerts,
                    "current_indices": {
                        "fsi": current_fsi,
                        "ddi": current_ddi
                    },
                    "trends": trends
                },
                "metric_alert",
                9
            )
        
        return None
    
    def generate_pattern_report(self, message: Message) -> Optional[Message]:
        """Generate comprehensive pattern analysis report"""
        request_data = message.content
        
        # Perform comprehensive pattern analysis
        pattern_report = {
            "report_id": f"PATTERN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "analysis_period": request_data.get("period", "last_30_days"),
            "patterns_identified": [],
            "hotspots": {},
            "trend_analysis": {},
            "predictions": [],
            "recommendations": []
        }
        
        # Identify temporal patterns
        temporal_patterns = self.identify_temporal_patterns()
        pattern_report["patterns_identified"].extend(temporal_patterns)
        
        # Identify geographic patterns (hotspots)
        geographic_patterns = self.identify_geographic_patterns()
        pattern_report["hotspots"] = geographic_patterns
        
        # Trend analysis
        pattern_report["trend_analysis"] = self.calculate_index_trends()
        
        # Generate predictions
        predictions = self.generate_predictive_alerts()
        pattern_report["predictions"] = predictions
        
        # Generate recommendations
        recommendations = self.generate_recommendations(pattern_report)
        pattern_report["recommendations"] = recommendations
        
        return self.send_message(
            message.sender,
            pattern_report,
            "pattern_report",
            7
        )
    
    def perform_case_analysis(self, case_record: Dict[str, Any]) -> Dict[str, Any]:
        """Perform detailed analysis on a case"""
        case_data = case_record["data"]
        
        analysis_results = {
            "case_id": case_record["case_id"],
            "analysis_timestamp": datetime.now().isoformat(),
            "indicators": [],
            "severity_score": 0,
            "urgency_level": 0,
            "patterns": [],
            "recommendations": []
        }
        
        # Convert case data to analyzable string
        case_str = str(case_data).lower()
        
        # Identify key indicators
        family_indicators = ["separation", "custody", "child", "family", "parent"]
        dignity_indicators = ["abuse", "violence", "harm", "humiliation", "degradation"]
        urgency_indicators = ["immediate", "urgent", "emergency", "crisis", "danger"]
        
        if any(indicator in case_str for indicator in family_indicators):
            analysis_results["indicators"].append("family_separation")
            analysis_results["severity_score"] += 3
        
        if any(indicator in case_str for indicator in dignity_indicators):
            analysis_results["indicators"].append("dignity_degradation")
            analysis_results["severity_score"] += 4
        
        if any(indicator in case_str for indicator in urgency_indicators):
            analysis_results["indicators"].append("urgent_situation")
            analysis_results["urgency_level"] = 8
            analysis_results["severity_score"] += 5
        
        # Pattern matching
        patterns = self.match_case_patterns(case_data)
        analysis_results["patterns"] = patterns
        
        # Generate recommendations
        recommendations = self.generate_case_recommendations(analysis_results)
        analysis_results["recommendations"] = recommendations
        
        # Mark as analyzed
        case_record["analyzed"] = True
        case_record["patterns_found"] = patterns
        
        return analysis_results
    
    def update_fsi(self, case_record: Dict[str, Any], analysis: Dict[str, Any]):
        """Update Family Separation Index based on case analysis"""
        fsi_impact = 0
        
        # Calculate FSI impact based on analysis
        if "family_separation" in analysis.get("indicators", []):
            fsi_impact += 2
        
        if analysis.get("severity_score", 0) > 5:
            fsi_impact += 1
        
        if analysis.get("urgency_level", 0) > 7:
            fsi_impact += 2
        
        # Add FSI data point
        if fsi_impact > 0:
            fsi_point = {
                "value": fsi_impact,
                "timestamp": datetime.now().isoformat(),
                "source": "case_analysis",
                "context": {
                    "case_id": case_record["case_id"],
                    "analysis": analysis
                }
            }
            self.fsi_data.append(fsi_point)
    
    def update_ddi(self, case_record: Dict[str, Any], analysis: Dict[str, Any]):
        """Update Dignity Degradation Index based on case analysis"""
        ddi_impact = 0
        
        # Calculate DDI impact
        if "dignity_degradation" in analysis.get("indicators", []):
            ddi_impact += 3
        
        if analysis.get("severity_score", 0) > 7:
            ddi_impact += 2
        
        if "abuse" in str(case_record["data"]).lower():
            ddi_impact += 2
        
        # Add DDI data point
        if ddi_impact > 0:
            ddi_point = {
                "value": ddi_impact,
                "timestamp": datetime.now().isoformat(),
                "source": "case_analysis",
                "context": {
                    "case_id": case_record["case_id"],
                    "analysis": analysis
                }
            }
            self.ddi_data.append(ddi_point)
    
    def check_hotspot_formation(self, location: str) -> Dict[str, Any]:
        """Check if a location is becoming a hotspot"""
        location_data = self.geographic_data[location]
        
        # Check recent activity (last 30 days)
        cutoff_date = datetime.now() - timedelta(days=30)
        recent_incidents = [
            incident for incident in location_data
            if datetime.fromisoformat(incident["timestamp"]) > cutoff_date
        ]
        
        incident_count = len(recent_incidents)
        avg_severity = statistics.mean([inc["severity"] for inc in recent_incidents]) if recent_incidents else 0
        
        is_hotspot = (
            incident_count >= self.analytics_config["hotspot_threshold"] and
            avg_severity >= 6
        )
        
        hotspot_analysis = {
            "location": location,
            "is_hotspot": is_hotspot,
            "incident_count": incident_count,
            "average_severity": avg_severity,
            "recent_incidents": recent_incidents,
            "risk_level": self.calculate_location_risk_level(location_data),
            "recommendations": []
        }
        
        if is_hotspot:
            self.hotspots[location] = hotspot_analysis
            hotspot_analysis["recommendations"] = [
                "Increase monitoring in this area",
                "Deploy additional support resources",
                "Coordinate with local authorities",
                "Establish rapid response protocols"
            ]
        
        return hotspot_analysis
    
    def identify_temporal_patterns(self) -> List[Dict[str, Any]]:
        """Identify patterns over time"""
        patterns = []
        
        # Analyze daily patterns
        daily_pattern = self.analyze_daily_patterns()
        if daily_pattern:
            patterns.append(daily_pattern)
        
        # Analyze weekly patterns
        weekly_pattern = self.analyze_weekly_patterns()
        if weekly_pattern:
            patterns.append(weekly_pattern)
        
        # Analyze monthly patterns
        monthly_pattern = self.analyze_monthly_patterns()
        if monthly_pattern:
            patterns.append(monthly_pattern)
        
        return patterns
    
    def identify_geographic_patterns(self) -> Dict[str, Any]:
        """Identify geographic patterns and hotspots"""
        geographic_patterns = {}
        
        for location, incidents in self.geographic_data.items():
            if len(incidents) >= 3:  # Minimum incidents to consider
                pattern_analysis = self.check_hotspot_formation(location)
                geographic_patterns[location] = pattern_analysis
        
        return geographic_patterns
    
    def calculate_index_trends(self) -> Dict[str, Any]:
        """Calculate trends for FSI and DDI indices"""
        trends = {}
        
        # FSI trend
        if len(self.fsi_data) >= 5:
            recent_fsi = [point["value"] for point in self.fsi_data[-10:]]
            earlier_fsi = [point["value"] for point in self.fsi_data[-20:-10]] if len(self.fsi_data) >= 20 else recent_fsi
            
            recent_avg = statistics.mean(recent_fsi)
            earlier_avg = statistics.mean(earlier_fsi)
            
            if recent_avg > earlier_avg * 1.1:
                trends["fsi_trend"] = "increasing"
            elif recent_avg < earlier_avg * 0.9:
                trends["fsi_trend"] = "decreasing"
            else:
                trends["fsi_trend"] = "stable"
            
            trends["fsi_current"] = recent_avg
        
        # DDI trend
        if len(self.ddi_data) >= 5:
            recent_ddi = [point["value"] for point in self.ddi_data[-10:]]
            earlier_ddi = [point["value"] for point in self.ddi_data[-20:-10]] if len(self.ddi_data) >= 20 else recent_ddi
            
            recent_avg = statistics.mean(recent_ddi)
            earlier_avg = statistics.mean(earlier_ddi)
            
            if recent_avg > earlier_avg * 1.1:
                trends["ddi_trend"] = "increasing"
            elif recent_avg < earlier_avg * 0.9:
                trends["ddi_trend"] = "decreasing"
            else:
                trends["ddi_trend"] = "stable"
            
            trends["ddi_current"] = recent_avg
        
        return trends
    
    def generate_predictive_alerts(self) -> List[Dict[str, Any]]:
        """Generate predictive alerts based on pattern analysis"""
        alerts = []
        
        # Predict FSI escalation
        if len(self.fsi_data) >= 10:
            fsi_prediction = self.predict_index_trajectory(self.fsi_data, "FSI")
            if fsi_prediction["predicted_peak"] > self.analytics_config["fsi_threshold"]:
                alerts.append(fsi_prediction)
        
        # Predict DDI escalation
        if len(self.ddi_data) >= 10:
            ddi_prediction = self.predict_index_trajectory(self.ddi_data, "DDI")
            if ddi_prediction["predicted_peak"] > self.analytics_config["ddi_threshold"]:
                alerts.append(ddi_prediction)
        
        # Predict hotspot escalation
        for location, hotspot_data in self.hotspots.items():
            if hotspot_data["risk_level"] >= 7:
                alerts.append({
                    "type": "hotspot_escalation",
                    "location": location,
                    "predicted_escalation": "high",
                    "timeline": "7-14 days",
                    "confidence": 0.75
                })
        
        return alerts
    
    def get_current_fsi(self) -> float:
        """Get current FSI value"""
        if not self.fsi_data:
            return 0.0
        
        # Use weighted average of recent data points
        recent_points = self.fsi_data[-5:]
        weights = [1, 2, 3, 4, 5][:len(recent_points)]
        
        weighted_sum = sum(point["value"] * weight for point, weight in zip(recent_points, weights))
        weight_sum = sum(weights)
        
        return weighted_sum / weight_sum if weight_sum > 0 else 0.0
    
    def get_current_ddi(self) -> float:
        """Get current DDI value"""
        if not self.ddi_data:
            return 0.0
        
        # Use weighted average of recent data points
        recent_points = self.ddi_data[-5:]
        weights = [1, 2, 3, 4, 5][:len(recent_points)]
        
        weighted_sum = sum(point["value"] * weight for point, weight in zip(recent_points, weights))
        weight_sum = sum(weights)
        
        return weighted_sum / weight_sum if weight_sum > 0 else 0.0
    
    def analyze_daily_patterns(self) -> Optional[Dict[str, Any]]:
        """Analyze daily patterns in the data"""
        if len(self.case_data) < 7:
            return None
        
        # Group cases by hour of day
        hourly_counts = defaultdict(int)
        for case in self.case_data:
            timestamp = datetime.fromisoformat(case["timestamp"])
            hourly_counts[timestamp.hour] += 1
        
        # Find peak hours
        if hourly_counts:
            peak_hour = max(hourly_counts, key=hourly_counts.get)
            return {
                "pattern_type": "daily",
                "peak_hour": peak_hour,
                "hourly_distribution": dict(hourly_counts),
                "confidence": 0.8 if len(hourly_counts) >= 5 else 0.6
            }
        
        return None
    
    def analyze_weekly_patterns(self) -> Optional[Dict[str, Any]]:
        """Analyze weekly patterns in the data"""
        if len(self.case_data) < 14:
            return None
        
        # Group cases by day of week
        daily_counts = defaultdict(int)
        for case in self.case_data:
            timestamp = datetime.fromisoformat(case["timestamp"])
            daily_counts[timestamp.strftime("%A")] += 1
        
        if daily_counts:
            peak_day = max(daily_counts, key=daily_counts.get)
            return {
                "pattern_type": "weekly",
                "peak_day": peak_day,
                "daily_distribution": dict(daily_counts),
                "confidence": 0.7
            }
        
        return None
    
    def analyze_monthly_patterns(self) -> Optional[Dict[str, Any]]:
        """Analyze monthly patterns in the data"""
        if len(self.case_data) < 30:
            return None
        
        # Group cases by day of month
        monthly_counts = defaultdict(int)
        for case in self.case_data:
            timestamp = datetime.fromisoformat(case["timestamp"])
            monthly_counts[timestamp.day] += 1
        
        if monthly_counts:
            peak_day = max(monthly_counts, key=monthly_counts.get)
            return {
                "pattern_type": "monthly",
                "peak_day_of_month": peak_day,
                "monthly_distribution": dict(monthly_counts),
                "confidence": 0.6
            }
        
        return None
    
    def match_case_patterns(self, case_data: Any) -> List[str]:
        """Match case against known patterns"""
        patterns = []
        case_str = str(case_data).lower()
        
        # Known pattern signatures
        pattern_signatures = {
            "custody_dispute": ["custody", "visitation", "court order", "parent"],
            "child_welfare": ["child protection", "social services", "welfare check"],
            "domestic_violence": ["violence", "abuse", "restraining order", "assault"],
            "system_failure": ["ignored", "failed", "dismissed", "bureaucracy"],
            "urgent_intervention": ["immediate", "emergency", "crisis", "danger"]
        }
        
        for pattern_name, keywords in pattern_signatures.items():
            if any(keyword in case_str for keyword in keywords):
                patterns.append(pattern_name)
        
        return patterns
    
    def generate_case_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on case analysis"""
        recommendations = []
        
        indicators = analysis.get("indicators", [])
        severity = analysis.get("severity_score", 0)
        urgency = analysis.get("urgency_level", 0)
        
        if "family_separation" in indicators:
            recommendations.append("Engage family reunification services")
            recommendations.append("Document all family interaction restrictions")
        
        if "dignity_degradation" in indicators:
            recommendations.append("Provide trauma-informed support")
            recommendations.append("Document dignity violations")
        
        if urgency >= 8:
            recommendations.append("Immediate intervention required")
            recommendations.append("Escalate to emergency response team")
        
        if severity >= 7:
            recommendations.append("Coordinate with legal advocates")
            recommendations.append("Ensure comprehensive documentation")
        
        return recommendations
    
    def calculate_location_risk_level(self, location_incidents: List[Dict[str, Any]]) -> int:
        """Calculate risk level for a location (1-10)"""
        if not location_incidents:
            return 1
        
        # Recent incidents (last 30 days)
        cutoff_date = datetime.now() - timedelta(days=30)
        recent_incidents = [
            incident for incident in location_incidents
            if datetime.fromisoformat(incident["timestamp"]) > cutoff_date
        ]
        
        risk_level = 1
        
        # Frequency factor
        if len(recent_incidents) >= 10:
            risk_level += 4
        elif len(recent_incidents) >= 5:
            risk_level += 2
        elif len(recent_incidents) >= 3:
            risk_level += 1
        
        # Severity factor
        if recent_incidents:
            avg_severity = statistics.mean([inc["severity"] for inc in recent_incidents])
            if avg_severity >= 8:
                risk_level += 3
            elif avg_severity >= 6:
                risk_level += 2
            elif avg_severity >= 4:
                risk_level += 1
        
        return min(risk_level, 10)
    
    def predict_index_trajectory(self, index_data: List[Dict[str, Any]], index_name: str) -> Dict[str, Any]:
        """Predict trajectory of an index"""
        recent_values = [point["value"] for point in index_data[-10:]]
        
        # Simple trend prediction
        if len(recent_values) >= 3:
            trend = (recent_values[-1] - recent_values[0]) / len(recent_values)
            predicted_peak = recent_values[-1] + (trend * 7)  # 7 days ahead
            
            return {
                "type": f"{index_name.lower()}_prediction",
                "current_value": recent_values[-1],
                "predicted_peak": predicted_peak,
                "trend": "increasing" if trend > 0 else "decreasing" if trend < 0 else "stable",
                "confidence": 0.7,
                "timeline": "7 days"
            }
        
        return {}
    
    def generate_recommendations(self, pattern_report: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on pattern analysis"""
        recommendations = []
        
        # Based on hotspots
        if pattern_report["hotspots"]:
            recommendations.append("Deploy additional resources to identified hotspots")
            recommendations.append("Establish rapid response protocols for high-risk areas")
        
        # Based on trends
        trends = pattern_report.get("trend_analysis", {})
        if trends.get("fsi_trend") == "increasing":
            recommendations.append("Implement family reunification initiatives")
        
        if trends.get("ddi_trend") == "increasing":
            recommendations.append("Strengthen dignity protection protocols")
        
        # Based on predictions
        if pattern_report["predictions"]:
            recommendations.append("Prepare preventive measures for predicted escalations")
            recommendations.append("Increase monitoring in predicted high-risk periods")
        
        return recommendations
    
    def extract_patterns_from_message(self, message: Message) -> Optional[Message]:
        """Extract patterns from any incoming message"""
        # Basic pattern extraction from message content
        content = str(message.content).lower()
        
        extracted_patterns = []
        
        # Look for concerning patterns
        if any(word in content for word in ["recurring", "pattern", "repeated"]):
            extracted_patterns.append("recurring_issue")
        
        if any(word in content for word in ["escalating", "worsening", "deteriorating"]):
            extracted_patterns.append("escalation_pattern")
        
        if any(word in content for word in ["systematic", "systemic", "institutional"]):
            extracted_patterns.append("systemic_issue")
        
        if extracted_patterns:
            return self.send_message(
                "IAM-0",
                {
                    "extracted_patterns": extracted_patterns,
                    "source_message": message.sender,
                    "analysis_timestamp": datetime.now().isoformat()
                },
                "pattern_extraction",
                6
            )
        
        return None
    
    def get_analytics_status(self) -> Dict[str, Any]:
        """Get current analytics status"""
        return {
            "current_indices": {
                "fsi": self.get_current_fsi(),
                "ddi": self.get_current_ddi()
            },
            "data_points": {
                "cases_analyzed": len(self.case_data),
                "fsi_data_points": len(self.fsi_data),
                "ddi_data_points": len(self.ddi_data),
                "geographic_locations": len(self.geographic_data)
            },
            "identified_patterns": len(self.identified_patterns),
            "active_hotspots": len(self.hotspots),
            "pending_alerts": len(self.predictive_alerts),
            "last_analysis": datetime.now().isoformat()
        }
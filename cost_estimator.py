# Car Damage Cost Estimator

class CostEstimator:
    def __init__(self):
        # Cost estimates in Indian Rupees (₹)
        self.repair_costs = {
            'dent': {
                'minor': {'range': (12000, 25000), 'time': '2-3 hours'},
                'moderate': {'range': (25000, 50000), 'time': '4-6 hours'},
                'severe': {'range': (50000, 100000), 'time': '6-8 hours'}
            },
            'scratch': {
                'minor': {'range': (8000, 20000), 'time': '1-2 hours'},
                'moderate': {'range': (20000, 40000), 'time': '3-4 hours'},
                'severe': {'range': (40000, 65000), 'time': '4-6 hours'}
            },
            'crack': {
                'minor': {'range': (15000, 32000), 'time': '2-3 hours'},
                'moderate': {'range': (32000, 65000), 'time': '4-6 hours'},
                'severe': {'range': (65000, 120000), 'time': '6-8 hours'}
            },
            'glass shatter': {
                'minor': {'range': (24000, 48000), 'time': '2-3 hours'},
                'moderate': {'range': (48000, 96000), 'time': '3-4 hours'},
                'severe': {'range': (96000, 200000), 'time': '4-6 hours'}
            },
            'lamp broken': {
                'minor': {'range': (12000, 32000), 'time': '1-2 hours'},
                'moderate': {'range': (32000, 65000), 'time': '2-3 hours'},
                'severe': {'range': (65000, 120000), 'time': '3-4 hours'}
            },
            'tire flat': {
                'minor': {'range': (4000, 12000), 'time': '30 minutes'},
                'moderate': {'range': (12000, 24000), 'time': '1 hour'},
                'severe': {'range': (24000, 48000), 'time': '2 hours'}
            }
        }
        
        self.paint_costs = {
            'small_area': {'range': (16000, 32000), 'time': '2-3 hours'},
            'medium_area': {'range': (32000, 65000), 'time': '4-6 hours'},
            'large_area': {'range': (65000, 120000), 'time': '6-8 hours'}
        }
        
        self.replacement_costs = {
            'dent': {'range': (65000, 160000), 'part': 'Body panel'},
            'scratch': {'range': (40000, 120000), 'part': 'Body panel'},
            'crack': {'range': (80000, 240000), 'part': 'Structural component'},
            'glass shatter': {'range': (40000, 160000), 'part': 'Glass/window'},
            'lamp broken': {'range': (24000, 96000), 'part': 'Light assembly'},
            'tire flat': {'range': (12000, 40000), 'part': 'Tire'}
        }
    
    def get_severity_from_confidence(self, confidence):
        """Determine severity based on detection confidence"""
        if confidence >= 0.7:
            return 'severe'
        elif confidence >= 0.4:
            return 'moderate'
        else:
            return 'minor'
    
    def estimate_damage_cost(self, damage_type, confidence):
        """Estimate cost for a single damage type"""
        severity = self.get_severity_from_confidence(confidence)
        
        repair_info = self.repair_costs.get(damage_type, self.repair_costs.get('dent', {}))
        repair_cost_range = repair_info.get('range', (12000, 25000))
        repair_time = repair_info.get('time', '2-3 hours')
        
        replacement_info = self.replacement_costs.get(damage_type, {'range': (40000, 120000), 'part': 'Unknown part'})
        replacement_cost_range = replacement_info.get('range', (40000, 120000))
        part_name = replacement_info.get('part', 'Unknown part')
        
        # Determine paint cost based on damage type and severity
        if damage_type in ['dent', 'scratch']:
            if severity == 'minor':
                paint_range = self.paint_costs['small_area']['range']
            elif severity == 'moderate':
                paint_range = self.paint_costs['medium_area']['range']
            else:
                paint_range = self.paint_costs['large_area']['range']
        else:
            paint_range = (0, 0)  # No paint needed for other damage types
        
        # Calculate recommended action
        if severity == 'minor':
            action = 'Repair'
        elif severity == 'moderate':
            action = 'Repair' if damage_type in ['dent', 'scratch'] else 'Replace'
        else:
            action = 'Replace'
        
        return {
            'part': part_name,
            'damage_type': damage_type,
            'severity': severity,
            'repair_cost': f"₹{repair_cost_range[0]:,}-₹{repair_cost_range[1]:,}",
            'paint_cost': f"₹{paint_range[0]:,}-₹{paint_range[1]:,}" if paint_range != (0, 0) else "Not required",
            'replacement_cost': f"₹{replacement_cost_range[0]:,}-₹{replacement_cost_range[1]:,}",
            'recommended_action': action,
            'repair_time': repair_time
        }
    
    def get_safety_concerns(self, damages):
        """Determine safety concerns based on damage types"""
        safety_concerns = []
        
        damage_types = [d['damage_type'] for d in damages]
        
        if 'glass shatter' in damage_types:
            safety_concerns.append("Broken glass can cause injury and visibility issues")
        
        if 'tire flat' in damage_types:
            safety_concerns.append("Flat tire affects vehicle control and can cause accidents")
        
        if 'lamp broken' in damage_types:
            safety_concerns.append("Broken lights reduce visibility and can cause accidents")
        
        if 'crack' in damage_types:
            safety_concerns.append("Structural cracks may compromise vehicle integrity")
        
        return safety_concerns if safety_concerns else ["No immediate safety concerns"]
    
    def get_drivability_impact(self, damages):
        """Determine impact on drivability"""
        damage_types = [d['damage_type'] for d in damages]
        
        if 'tire flat' in damage_types:
            return "Not drivable - tire replacement required"
        elif 'glass shatter' in damage_types:
            return "Limited drivability - visibility impaired"
        elif 'lamp broken' in damage_types:
            return "Drivable but avoid night driving"
        elif 'crack' in damage_types:
            return "Drivable but get inspection ASAP"
        else:
            return "Fully drivable"
    
    def get_insurance_suggestion(self, damages):
        """Suggest whether to file insurance claim"""
        total_cost_low = 0
        total_cost_high = 0
        
        for damage in damages:
            repair_range = self.repair_costs.get(damage['damage_type'], {}).get('range', (0, 0))
            total_cost_low += repair_range[0]
            total_cost_high += repair_range[1]
        
        avg_cost = (total_cost_low + total_cost_high) / 2
        
        if avg_cost > 80000:
            return "Yes - cost exceeds typical deductible"
        elif avg_cost > 40000:
            return "Consider - depends on deductible and premium impact"
        else:
            return "No - cost is likely below deductible"
    
    def generate_full_report(self, detections):
        """Generate complete damage assessment report"""
        damages = []
        total_cost_low = 0
        total_cost_high = 0
        
        for detection in detections:
            damage_type = detection['class']
            confidence = detection['confidence'] / 100  # Convert from percentage
            
            damage_info = self.estimate_damage_cost(damage_type, confidence)
            damages.append(damage_info)
            
            # Add to total cost (using repair cost as primary estimate)
            repair_range = self.repair_costs.get(damage_type, self.repair_costs.get('dent', {})).get('range', (12000, 25000))
            total_cost_low += repair_range[0]
            total_cost_high += repair_range[1]
        
        # Determine urgency
        damage_types = [d['damage_type'] for d in damages]
        if any(d in ['glass shatter', 'tire flat'] for d in damage_types):
            urgency = "Immediate"
        elif any(d in ['lamp broken', 'crack'] for d in damage_types):
            urgency = "Urgent (within 1-2 days)"
        else:
            urgency = "Can wait (within 1-2 weeks)"
        
        return {
            "damages": damages,
            "total_estimated_cost": f"₹{total_cost_low:,}-₹{total_cost_high:,}",
            "urgency_level": urgency,
            "safety_concerns": self.get_safety_concerns(damages),
            "drivability": self.get_drivability_impact(damages),
            "insurance_suggestion": self.get_insurance_suggestion(damages)
        }

# Test the estimator
if __name__ == "__main__":
    estimator = CostEstimator()
    
    # Test with sample detections
    sample_detections = [
        {'class': 'dent', 'confidence': 75},
        {'class': 'scratch', 'confidence': 64},
        {'class': 'lamp broken', 'confidence': 73}
    ]
    
    report = estimator.generate_full_report(sample_detections)
    import json
    print(json.dumps(report, indent=2))

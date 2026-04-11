from django import template
import re

register = template.Library()

@register.filter
def split_days(itinerary):
    """Split itinerary into days"""
    if not itinerary:
        return []
    # Split by "Day X:" pattern
    days = re.split(r'Day \d+:', itinerary)
    # Remove empty first element
    return [day.strip() for day in days if day.strip()]

@register.filter
def get_day_title(day_text):
    """Extract the title from day text"""
    lines = day_text.split('\n')
    if lines:
        return lines[0].strip()
    return ""

@register.filter
def format_day_content(day_text):
    """Format day content with proper HTML"""
    lines = day_text.split('\n')
    html = []
    
    for line in lines[1:]:  # Skip first line (title)
        line = line.strip()
        if not line:
            continue
            
        # Check if it's a flight/train line
        if 'Flight:' in line or 'Train:' in line:
            # Extract details
            parts = line.split(' - ')
            if len(parts) >= 2:
                transport_type = "✈️" if "Flight" in line else "🚂"
                html.append(f'''
                <div class="transport-card">
                    <div class="transport-icon">{transport_type}</div>
                    <div class="transport-details">
                        <div class="transport-time">
                            <div class="time-value">{parts[0].split(':')[1].strip().split('(')[0].strip()}</div>
                            <div class="time-label">Departure</div>
                        </div>
                        <div class="transport-arrow">→</div>
                        <div class="transport-time">
                            <div class="time-value">{parts[1].split(')')[0].strip() if ')' in parts[1] else 'Arrival'}</div>
                            <div class="time-label">Arrival</div>
                        </div>
                    </div>
                    <div class="transport-price">
                        <div class="price-value">₹{parts[-1].strip() if '₹' in parts[-1] else 'Included'}</div>
                        <div class="price-label">Per Person</div>
                    </div>
                </div>
                ''')
        # Check if it's an activity with cost
        elif '₹' in line or 'Entry:' in line or 'visit' in line.lower():
            # Extract cost if present
            cost_match = re.search(r'₹[\d,]+', line)
            cost = cost_match.group() if cost_match else ''
            activity_text = line.replace(cost, '').strip()
            
            html.append(f'''
            <div class="activity-item">
                <span class="activity-icon">🎯</span>
                <span class="activity-text">{activity_text}</span>
                {f'<span class="activity-cost">{cost}</span>' if cost else ''}
            </div>
            ''')
        else:
            # Regular text
            if line.startswith('-'):
                line = line[1:].strip()
            html.append(f'<div class="activity-item"><span class="activity-icon">📍</span><span class="activity-text">{line}</span></div>')
    
    return '\n'.join(html)

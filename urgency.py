"""
Urgency Detection Module
Analyzes user messages to determine appropriate response temperature
"""

def detect_urgency(text: str) -> float:
    """
    Detect urgency level in user message and return appropriate temperature.
    
    Args:
        text (str): User's message
    
    Returns:
        float: Temperature value (0.1 for urgent, 0.9 for casual)
    
    Examples:
        >>> detect_urgency("URGENT! Need help ASAP!")
        0.1
        
        >>> detect_urgency("Hey, just wondering about your hours")
        0.9
    """
    
    # Keywords indicating urgent/critical situations
    urgent_keywords = [
        "urgent", "urgently", 
        "immediately", "immediate",
        "asap", "a.s.a.p",
        "right now", 
        "help!", "help me",
        "emergency", "critical",
        "broken", "not working",
        "problem", "issue",
        "!!!", "!!!!"
    ]
    
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Check if any urgent keyword is present
    if any(word in text_lower for word in urgent_keywords):
        return 0.1  # Low temperature = focused, factual, direct
    
    return 0.9  # High temperature = creative, conversational, friendly


def get_urgency_level(text: str) -> str:
    """
    Get human-readable urgency level.
    
    Args:
        text (str): User's message
    
    Returns:
        str: "URGENT" or "CASUAL"
    """
    temp = detect_urgency(text)
    return "URGENT" if temp == 0.1 else "CASUAL"


# Test the function if run directly
if __name__ == "__main__":
    test_messages = [
        "URGENT! My order is broken!",
        "Hey, what are your hours?",
        "I need help ASAP!!!",
        "Just browsing, tell me about your products",
        "This is an emergency - account locked immediately"
    ]
    
    print("🧪 Testing Urgency Detection\n")
    print("=" * 60)
    
    for msg in test_messages:
        temp = detect_urgency(msg)
        level = get_urgency_level(msg)
        print(f"Message: {msg}")
        print(f"Level: {level} | Temperature: {temp}")
        print("-" * 60)
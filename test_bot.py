"""
Automated Testing Script for FAQ Chatbot
Tests various scenarios and demonstrates caching
"""

import time
from faq_bot import FAQChatbot

def run_tests():
    """Run comprehensive tests"""
    
    print("\n" + "="*70)
    print("🧪 FAQ CHATBOT - AUTOMATED TESTING")
    print("="*70 + "\n")
    
    # Initialize bot
    bot = FAQChatbot()
    
    # Test scenarios
    test_cases = [
        # Round 1: First time queries (cache miss)
        ("What are your business hours?", "Casual FAQ"),
        ("Where is your location?", "Casual FAQ"),
        ("URGENT! I need to return my order ASAP!", "Urgent Query"),
        
        # Round 2: Repeat queries (cache hit)
        ("What are your business hours?", "Repeat Query (should be cached)"),
        ("Where is your location?", "Repeat Query (should be cached)"),
        
        # Round 3: New queries
        ("Do you accept PayPal?", "New Query"),
        ("How can I track my order?", "New Query"),
        
        # Round 4: Urgent vs Casual
        ("Help!!! My package is broken!", "Urgent"),
        ("Just wondering, what's your return policy?", "Casual"),
    ]
    
    print("Running test cases...\n")
    
    for i, (query, description) in enumerate(test_cases, 1):
        print(f"{'='*70}")
        print(f"TEST {i}: {description}")
        print(f"{'='*70}")
        print(f"Query: {query}\n")
        
        # Run query
        result = bot.chat(query)
        
        if result["success"]:
            # Display results
            mode = "🚨 URGENT" if result["urgency"] == "URGENT" else "💬 CASUAL"
            cache = "📦 CACHED" if result["cached"] else "🌐 API"
            
            print(f"Mode: {mode}")
            print(f"Temperature: {result['temperature']}")
            print(f"Cache: {cache}")
            print(f"Time: {result['time']:.3f}s")
            print(f"\nResponse: {result['message']}\n")
        else:
            print(f"❌ Error: {result['error']}\n")
        
        # Small delay between tests
        time.sleep(0.5)
    
    # Show final statistics
    print("="*70)
    print("TEST SUMMARY")
    print("="*70)
    bot.show_stats()


if __name__ == "__main__":
    run_tests()
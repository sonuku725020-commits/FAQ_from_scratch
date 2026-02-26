"""
Smart FAQ Chatbot with Dynamic Temperature and Caching
Features:
- Urgency detection (automatic temperature adjustment)
- Response caching (faster, cheaper)
- Conversation memory
- FAQ knowledge base
- Statistics tracking
"""

import os
import time
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Import our custom modules
import cache  # This enables caching
from urgency import detect_urgency, get_urgency_level

# Load environment variables
load_dotenv()


class FAQChatbot:
    """
    Intelligent FAQ Chatbot with dynamic temperature control and caching
    """
    
    def __init__(self, model: str = "gpt-3.5-turbo"):
        """
        Initialize the FAQ chatbot
        
        Args:
            model (str): OpenAI model to use (default: gpt-3.5-turbo)
        """
        
        # Chat history
        self.chat_history: List = []
        
        # Statistics
        self.stats = {
            "total_queries": 0,
            "urgent_queries": 0,
            "casual_queries": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_time": 0.0
        }
        
        # FAQ Knowledge Base
        self.faq_data = {
            "hours": "We're open Monday-Friday 9 AM - 6 PM, Saturday 10 AM - 4 PM, closed Sunday.",
            "location": "We're located at 123 Main Street, Downtown, New York, NY 10001.",
            "contact": "You can reach us at (555) 123-4567 or email support@example.com",
            "returns": "Returns accepted within 30 days with receipt. Full refund or exchange available.",
            "shipping": "Free shipping on orders over $50. Standard delivery: 3-5 business days. Express: 1-2 days.",
            "payment": "We accept Visa, MasterCard, American Express, PayPal, and Apple Pay.",
            "warranty": "All products come with a 1-year manufacturer warranty.",
            "track_order": "You can track your order at example.com/track using your order number."
        }
        
        # Store model name
        self.model_name = model
        
        # Current LLM instance (will be recreated based on temperature)
        self.current_llm = None
        self.current_temperature = None
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        print("🤖 FAQ Chatbot initialized successfully!")
        print(f"📊 Model: {self.model_name}")
        print(f"💾 Caching: Enabled")
        print(f"🚦 Dynamic Temperature: Enabled\n")
    
    def _get_system_prompt(self) -> str:
        """Generate system prompt with FAQ knowledge"""
        
        faq_text = "\n".join([
            f"- {key.upper()}: {value}" 
            for key, value in self.faq_data.items()
        ])
        
        return f"""You are a helpful and friendly customer support assistant.

📋 FAQ KNOWLEDGE BASE:
{faq_text}

INSTRUCTIONS:
- Answer questions accurately using the FAQ knowledge above
- For urgent queries: Be direct, concise, and action-oriented
- For casual queries: Be friendly, conversational, and helpful
- If you don't know something, be honest and offer to connect them with support
- Always maintain a professional yet warm tone"""
    
    def _get_llm(self, temperature: float) -> ChatOpenAI:
        """
        Get LLM instance with specified temperature
        Reuses instance if temperature hasn't changed
        
        Args:
            temperature (float): Temperature setting
        
        Returns:
            ChatOpenAI: LLM instance
        """
        
        # Only create new LLM if temperature changed
        if self.current_llm is None or self.current_temperature != temperature:
            self.current_llm = ChatOpenAI(
                model=self.model_name,
                temperature=temperature,
                max_tokens=300,
                api_key=os.environ.get("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
                cache=True  # Enable caching
            )
            self.current_temperature = temperature
        
        return self.current_llm
    
    def chat(self, user_input: str) -> Dict:
        """
        Process user input and generate response
        
        Args:
            user_input (str): User's message
        
        Returns:
            dict: Response data including message, temperature, timing, etc.
        """
        
        start_time = time.time()
        
        # Detect urgency and get appropriate temperature
        temperature = detect_urgency(user_input)
        urgency_level = get_urgency_level(user_input)
        
        # Update statistics
        self.stats["total_queries"] += 1
        if urgency_level == "URGENT":
            self.stats["urgent_queries"] += 1
        else:
            self.stats["casual_queries"] += 1
        
        # Get LLM with appropriate temperature
        llm = self._get_llm(temperature)
        
        # Create chain
        chain = self.prompt | llm
        
        # Invoke chain
        try:
            response = chain.invoke({
                "chat_history": self.chat_history,
                "input": user_input
            })
            
            # Update history
            self.chat_history.append(HumanMessage(content=user_input))
            self.chat_history.append(AIMessage(content=response.content))
            
            # Calculate timing
            elapsed_time = time.time() - start_time
            self.stats["total_time"] += elapsed_time
            
            # Estimate cache hit (very fast = likely cached)
            if elapsed_time < 0.1:
                self.stats["cache_hits"] += 1
            else:
                self.stats["cache_misses"] += 1
            
            # Return detailed response
            return {
                "success": True,
                "message": response.content,
                "urgency": urgency_level,
                "temperature": temperature,
                "time": elapsed_time,
                "cached": elapsed_time < 0.1,
                "tokens": response.response_metadata.get("token_usage", {})
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "urgency": urgency_level,
                "temperature": temperature
            }
    
    def clear_history(self):
        """Clear conversation history"""
        self.chat_history = []
        print("✅ Chat history cleared!")
    
    def get_stats(self) -> Dict:
        """Get chatbot statistics"""
        return self.stats.copy()
    
    def show_stats(self):
        """Display formatted statistics"""
        stats = self.stats
        
        print("\n" + "="*60)
        print("📊 CHATBOT STATISTICS")
        print("="*60)
        print(f"Total Queries:     {stats['total_queries']}")
        print(f"  - Urgent:        {stats['urgent_queries']}")
        print(f"  - Casual:        {stats['casual_queries']}")
        print(f"\nCache Performance:")
        print(f"  - Cache Hits:    {stats['cache_hits']} (estimated)")
        print(f"  - Cache Misses:  {stats['cache_misses']} (estimated)")
        
        if stats['total_queries'] > 0:
            avg_time = stats['total_time'] / stats['total_queries']
            cache_rate = (stats['cache_hits'] / stats['total_queries']) * 100
            print(f"\nPerformance:")
            print(f"  - Avg Response:  {avg_time:.3f}s")
            print(f"  - Cache Rate:    {cache_rate:.1f}%")
        
        print("="*60 + "\n")
    
    def run(self):
        """Run interactive chatbot"""
        
        print("="*60)
        print("🤖 SMART FAQ CHATBOT")
        print("="*60)
        print("\n📋 Available Commands:")
        print("  'quit' / 'exit'  - Exit the chatbot")
        print("  'clear'          - Clear chat history")
        print("  'stats'          - Show statistics")
        print("  'help'           - Show FAQ topics")
        print("\n💡 Tip: Try urgent queries (with 'URGENT', '!!!', 'ASAP')")
        print("       vs casual queries to see temperature adjustment!\n")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit']:
                    print("\n" + "="*60)
                    self.show_stats()
                    print("👋 Thank you for using FAQ Chatbot! Goodbye!")
                    print("="*60 + "\n")
                    break
                
                if user_input.lower() == 'clear':
                    self.clear_history()
                    continue
                
                if user_input.lower() == 'stats':
                    self.show_stats()
                    continue
                
                if user_input.lower() == 'help':
                    print("\n📋 FAQ Topics:")
                    for topic in self.faq_data.keys():
                        print(f"  - {topic.replace('_', ' ').title()}")
                    print()
                    continue
                
                # Process query
                result = self.chat(user_input)
                
                if result["success"]:
                    # Show mode indicator
                    mode_emoji = "🚨" if result["urgency"] == "URGENT" else "💬"
                    mode_text = f"{mode_emoji} {result['urgency']} MODE (temp={result['temperature']})"
                    cache_text = "📦 CACHED" if result["cached"] else "🌐 API CALL"
                    
                    print(f"\n[{mode_text} | {cache_text} | {result['time']:.3f}s]")
                    print(f"Bot: {result['message']}\n")
                else:
                    print(f"\n❌ Error: {result['error']}\n")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run the chatbot"""
    
    # Check for API key
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("❌ ERROR: OPENROUTER_API_KEY not found in .env file!")
        print("Please add your API key to .env file:")
        print("OPENROUTER_API_KEY=sk-or-v1-xxxxx")
        return
    
    # Create and run chatbot
    bot = FAQChatbot(model="openai/gpt-3.5-turbo")
    bot.run()


if __name__ == "__main__":
    main()
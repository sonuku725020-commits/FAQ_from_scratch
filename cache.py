"""
Cache Configuration for FAQ Chatbot
Enables response caching to reduce API calls and costs
"""

from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache

# Create cache instance
cache = InMemoryCache()

# Enable caching globally
set_llm_cache(cache)

print("✅ Cache enabled - responses will be cached in memory")
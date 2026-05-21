"""
NLP Engine for Offline Chatbot
Handles keyword matching, intent recognition, and typo tolerance
Uses difflib for fuzzy matching - no external ML or APIs needed
"""
from difflib import SequenceMatcher
import re
from typing import Dict, List, Any

class ChatbotNLPEngine:
    """
    Lightweight NLP engine for offline chatbot
    - Keyword-based intent matching
    - Fuzzy string matching for typo tolerance
    - Context awareness for current session
    - No external dependencies or APIs
    """
    
    # Intent patterns with keywords
    INTENT_PATTERNS = {
        'product_query': {
            'keywords': ['product', 'item', 'what', 'tell me', 'show', 'have', 'available', 'stock'],
            'response_template': 'I found information about that product. {context}'
        },
        'pricing': {
            'keywords': ['price', 'cost', 'how much', 'expensive', 'cheap', 'discount', 'sale', 'offer'],
            'response_template': 'The pricing information: {context}'
        },
        'availability': {
            'keywords': ['available', 'stock', 'in stock', 'out of stock', 'when', 'left', 'quantity'],
            'response_template': 'Availability status: {context}'
        },
        'shipping': {
            'keywords': ['shipping', 'delivery', 'ship', 'deliver', 'how long', 'when arrive', 'cost'],
            'response_template': 'Shipping information: {context}'
        },
        'return_policy': {
            'keywords': ['return', 'refund', 'exchange', 'policy', 'guarantee', 'warranty'],
            'response_template': 'Our return policy: {context}'
        },
        'faq': {
            'keywords': ['help', 'how', 'why', 'what', 'where', 'when', 'question', 'problem'],
            'response_template': '{context}'
        },
        'greeting': {
            'keywords': ['hello', 'hi', 'hey', 'greetings', 'how are you', 'good morning', 'good evening'],
            'response_template': '{context}'
        }
    }
    
    # Fallback responses
    FALLBACK_RESPONSES = [
        "I'm not sure about that. Could you provide more details or try a different question?",
        "That's an interesting question. Try asking about our products, pricing, shipping, or return policy.",
        "I didn't quite understand. Would you like to know about our products or policies?",
        "Let me help you better. Are you looking for product info, pricing, or shipping details?"
    ]
    
    def __init__(self, products_data: Dict, faq_data: Dict):
        """Initialize NLP engine with products and FAQ data"""
        self.products = products_data.get('products', [])
        self.faqs = faq_data.get('faqs', [])
        self.fallback_index = 0
        
    def similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings (0-1)"""
        if not str1 or not str2:
            return 0.0
        s = SequenceMatcher(None, str1.lower(), str2.lower())
        return s.ratio()
    
    def find_similar_keyword(self, text: str, keywords: List[str], threshold: float = 0.7) -> bool:
        """
        Check if any keyword appears in text with fuzzy matching for typo tolerance
        Returns True if match found above threshold
        """
        text_lower = text.lower()
        
        # First try exact substring match
        for keyword in keywords:
            if keyword.lower() in text_lower:
                return True
        
        # Then try fuzzy match for typo tolerance
        words = re.findall(r'\b\w+\b', text_lower)
        for word in words:
            for keyword in keywords:
                if self.similarity_score(word, keyword) >= threshold:
                    return True
        
        return False
    
    def extract_product_name(self, text: str) -> str:
        """Extract product name from user query using fuzzy matching"""
        text_lower = text.lower()
        best_match = None
        best_score = 0.5
        
        for product in self.products:
            product_name = product.get('name', '').lower()
            # Try exact substring match first
            if product_name in text_lower:
                return product.get('name', '')
            
            # Try fuzzy matching
            score = self.similarity_score(text, product_name)
            if score > best_score:
                best_score = score
                best_match = product.get('name', '')
        
        return best_match or ''
    
    def get_product_info(self, product_name: str) -> Dict:
        """Get detailed information about a product"""
        for product in self.products:
            if product.get('name', '').lower() == product_name.lower():
                return product
        return {}
    
    def find_faq(self, text: str) -> Dict:
        """Find matching FAQ by fuzzy matching question"""
        best_match = None
        best_score = 0.4
        
        for faq in self.faqs:
            question = faq.get('question', '')
            score = self.similarity_score(text, question)
            if score > best_score:
                best_score = score
                best_match = faq
        
        return best_match or {}
    
    def recognize_intent(self, text: str) -> str:
        """Recognize user intent from text"""
        text_lower = text.lower()
        
        for intent, pattern in self.INTENT_PATTERNS.items():
            if self.find_similar_keyword(text, pattern['keywords'], threshold=0.65):
                return intent
        
        return 'general'
    
    def get_suggestions(self, text: str) -> List[str]:
        """Get product suggestions based on query"""
        suggestions = []
        text_lower = text.lower()
        
        for product in self.products[:5]:
            name = product.get('name', '')
            if text_lower and text_lower in name.lower():
                suggestions.append(name)
        
        return suggestions[:3]
    
    def generate_product_response(self, product_name: str, intent: str) -> str:
        """Generate response based on product and intent"""
        product = self.get_product_info(product_name)
        if not product:
            return f"I couldn't find details about '{product_name}'. Try another product?"
        
        name = product.get('name', 'Product')
        
        if intent == 'pricing':
            price = product.get('price', 'Contact us')
            return f"{name} is priced at {price}. Would you like to know more?"
        
        elif intent == 'availability':
            availability = product.get('availability', 'Check back soon')
            return f"{name} - {availability}"
        
        elif intent == 'shipping':
            shipping = product.get('shipping_info', '2-3 business days')
            return f"Shipping for {name}: {shipping}. Any other questions?"
        
        else:
            description = product.get('description', '')
            category = product.get('category', '')
            price = product.get('price', '')
            response = f"{name}\n"
            if category:
                response += f"Category: {category}\n"
            if price:
                response += f"Price: {price}\n"
            if description:
                response += f"Description: {description}"
            return response
    
    def process_query(self, user_message: str, context: Dict) -> Dict:
        """
        Main NLP processing function
        Returns structured response with intent, suggestions, quick replies
        """
        # Recognize intent
        intent = self.recognize_intent(user_message)
        
        response_text = ""
        suggestions = []
        quick_replies = []
        
        # Handle different intents
        if intent == 'greeting':
            response_text = "Hello! Welcome to our store. 👋 What can I help you with today?\nFeel free to ask about products, pricing, shipping, or our return policy!"
            quick_replies = ["Tell me about products", "What's shipping cost?", "Return policy", "Browse FAQs"]
        
        elif intent == 'return_policy':
            response_text = "📋 Return Policy:\n✓ 30-day money-back guarantee\n✓ Free returns for defective items\n✓ Exchange available within 60 days\n✓ No questions asked refunds\n\nNeed help with a specific product?"
            quick_replies = ["Browse products", "Contact support", "Track order"]
        
        else:
            # Try to find product match
            product_name = self.extract_product_name(user_message)
            
            if product_name:
                response_text = self.generate_product_response(product_name, intent)
                suggestions = self.get_suggestions(user_message)
                quick_replies = ["Show more details", "Similar products", "Add to cart", "Ask another question"]
            
            else:
                # Try to find matching FAQ
                faq = self.find_faq(user_message)
                if faq and faq.get('answer'):
                    response_text = faq['answer']
                    quick_replies = ["Ask another question", "Browse products", "Contact support"]
                
                else:
                    # Use fallback response
                    response_text = self.FALLBACK_RESPONSES[self.fallback_index % len(self.FALLBACK_RESPONSES)]
                    self.fallback_index += 1
                    quick_replies = ["Show products", "FAQs", "Help"]
        
        # Update context
        context['last_intent'] = intent
        context['last_product'] = product_name if product_name else None
        
        return {
            'response': response_text,
            'intent': intent,
            'suggestions': suggestions,
            'quick_replies': quick_replies,
            'context': context
        }

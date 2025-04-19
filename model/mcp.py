from typing import List, Dict, Any


class MessageCoherenceProtocol:
    """
    Implementation of the Message Coherence Protocol.
    MCP focuses on maintaining dialogue coherence without using function calls.
    """

    def __init__(self):
        self.intent_map = {
            "search": ["search", "find", "look up", "google", "information about", "tell me about"],
            "chat": ["chat", "talk", "conversation", "discuss"],
            "help": ["help", "assist", "support"],
            "explain": ["explain", "describe", "what is", "how does", "why is"]
        }

    def process(self, message: str, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process a message using MCP.

        Args:
            message: The user's message
            history: Conversation history

        Returns:
            A dictionary with processing results and metadata
        """
        # Convert message to lowercase for intent matching
        message_lower = message.lower()

        # Detect intent
        intent = self._detect_intent(message_lower)

        # Check if the message requires web search
        needs_search = self._needs_search(message_lower, intent)

        # Extract entities if needed
        entities = self._extract_entities(message) if needs_search else []

        # Construct search query if needed
        search_query = self._construct_search_query(message, entities) if needs_search else ""

        # Check coherence with conversation history
        coherence_score = self._check_coherence(message, history)

        # Determine appropriate response strategy
        response_strategy = self._determine_response_strategy(intent, needs_search, coherence_score)

        return {
            "message": message,
            "intent": intent,
            "needs_search": needs_search,
            "search_query": search_query,
            "entities": entities,
            "coherence_score": coherence_score,
            "response_strategy": response_strategy
        }

    def _detect_intent(self, message: str) -> str:
        """
        Detect the user's intent from the message.

        Args:
            message: The user's message (lowercase)

        Returns:
            The detected intent
        """
        for intent, keywords in self.intent_map.items():
            if any(keyword in message for keyword in keywords):
                return intent

        # Default to chat if no specific intent is detected
        return "chat"

    def _needs_search(self, message: str, intent: str) -> bool:
        """
        Determine if the message requires web search.

        Args:
            message: The user's message (lowercase)
            intent: The detected intent

        Returns:
            True if search is needed, False otherwise
        """
        # Check if the intent is search
        if intent == "search":
            return True

        # Check for explicit search requests
        search_indicators = [
            "find information",
            "search for",
            "look up",
            "what is",
            "who is",
            "where is",
            "when was",
            "how to",
            "latest news",
            "recent events"
        ]

        if any(indicator in message for indicator in search_indicators):
            return True

        # Check for factual questions that might need search
        question_starters = ["what", "who", "where", "when", "why", "how", "which", "is", "are", "was", "were"]
        words = message.split()

        if len(words) > 0 and any(words[0] == starter for starter in question_starters):
            # Not all questions need search, but many factual ones do
            return True

        return False

    def _extract_entities(self, message: str) -> List[str]:
        """
        Extract entities from the message for search purposes.

        Args:
            message: The user's message

        Returns:
            A list of extracted entities
        """
        # This is a simple placeholder for entity extraction
        # In a real implementation, you would use NER or other techniques

        # Remove common stop words and split by spaces
        stop_words = ["a", "an", "the", "is", "are", "was", "were", "in", "on", "at", "to", "for", "with", "by"]
        words = message.split()

        # Filter out stop words and keep words with 3+ characters as potential entities
        entities = [word for word in words if word.lower() not in stop_words and len(word) >= 3]

        return entities

    def _construct_search_query(self, message: str, entities: List[str]) -> str:
        """
        Construct a search query from the message and entities.

        Args:
            message: The user's message
            entities: Extracted entities

        Returns:
            A search query
        """
        # Start with the original message as the base query
        query = message

        # Remove search-related phrases to clean up the query
        search_phrases = ["search for", "look up", "find information about", "tell me about",
                          "can you find", "i need information on", "what do you know about"]

        for phrase in search_phrases:
            query = query.replace(phrase, "").strip()

        # If the query is still too long, use just the entities
        if len(query.split()) > 10 and entities:
            query = " ".join(entities[:5])  # Use up to 5 entities

        return query

    def _check_coherence(self, message: str, history: List[Dict[str, Any]]) -> float:
        """
        Check the coherence of the message with conversation history.

        Args:
            message: The user's message
            history: Conversation history

        Returns:
            A coherence score between 0.0 and 1.0
        """
        # If history is empty or very short, coherence is neutral
        if len(history) < 2:
            return 0.5

        # Get the last few exchanges
        recent_history = history[-4:] if len(history) >= 4 else history

        # Calculate overlap between message and recent history
        message_words = set(message.lower().split())

        # Check for word overlap with recent messages
        overlap_score = 0.0
        for i, entry in enumerate(reversed(recent_history)):
            # Give more weight to more recent messages
            weight = 1.0 / (i + 1)

            # Calculate word overlap
            entry_words = set(entry["content"].lower().split())
            if entry_words:
                overlap = len(message_words.intersection(entry_words)) / len(entry_words)
                overlap_score += overlap * weight

        # Normalize to 0.0-1.0
        normalized_score = min(overlap_score, 1.0)

        return normalized_score

    def _determine_response_strategy(self, intent: str, needs_search: bool, coherence_score: float) -> str:
        """
        Determine the appropriate response strategy.

        Args:
            intent: The detected intent
            needs_search: Whether search is needed
            coherence_score: The coherence score

        Returns:
            A response strategy string
        """
        if needs_search:
            return "search_and_respond"

        if coherence_score < 0.2:
            # Very low coherence might indicate a topic change
            return "address_topic_change"

        if coherence_score > 0.8:
            # High coherence suggests continuing the current topic
            return "continue_topic"

        # Default strategy based on intent
        intent_strategy_map = {
            "chat": "conversational",
            "help": "helpful",
            "explain": "informative"
        }

        return intent_strategy_map.get(intent, "conversational")
"""
Response evaluator for the Museum Chatbot test suite.
Evaluates bot responses against expected criteria.
"""

from typing import Dict, List, Any
from ..config import EVALUATION_CRITERIA


class ResponseEvaluator:
    """Evaluates chatbot responses against test criteria"""
    
    @staticmethod
    def evaluate_response(test_case: Dict, response: str, full_response: List[Dict]) -> str:
        """
        Evaluates the quality of bot response against test case expectations
        
        Args:
            test_case: Test case dictionary with expected criteria
            response: Combined bot response text
            full_response: List of raw response objects
            
        Returns:
            str: Evaluation result (PASS, PARTIAL, FAIL, NO_RESULTS, ERROR, UNKNOWN)
        """
        category = test_case['category']
        response_lower = response.lower()
        
        # Check for error indicators
        if any(error_term in response_lower for error_term in EVALUATION_CRITERIA['error_indicators']):
            return "FAIL"
        
        # Check for no results indicators
        if any(no_result_term in response_lower for no_result_term in EVALUATION_CRITERIA['no_results_indicators']):
            return "NO_RESULTS"
        
        # Category-specific evaluation
        return ResponseEvaluator._evaluate_by_category(category, response_lower)
    
    @staticmethod
    def _evaluate_by_category(category: str, response_lower: str) -> str:
        """Evaluates response based on category-specific criteria"""
        criteria = EVALUATION_CRITERIA['category_criteria'].get(category, [])
        
        if category == "artwork":
            if any(indicator in response_lower for indicator in criteria):
                return "PASS"
            else:
                return "PARTIAL"
                
        elif category == "artist":
            if any(indicator in response_lower for indicator in criteria):
                return "PASS"
            else:
                return "PARTIAL"
                
        elif category == "museum":
            if any(indicator in response_lower for indicator in criteria):
                return "PASS"
            else:
                return "PARTIAL"
                
        elif category == "conversation":
            if len(response_lower) > 10:  # Minimum length for meaningful response
                return "PASS"
            else:
                return "PARTIAL"
        
        return "UNKNOWN"
    
    @staticmethod
    def identify_api_source(response: str) -> str:
        """
        Identifies the API source used for the response
        
        Args:
            response: Bot response text
            
        Returns:
            str: Identified API source with emoji
        """
        sources = EVALUATION_CRITERIA['api_sources']
        
        for source_key, source_info in sources.items():
            for indicator in source_info['indicators']:
                if indicator in response:
                    return f"{source_info['emoji']} {source_info['name']}"
        
        # Try to extract source from response
        import re
        source_match = re.search(r'Quelle:\*\*\s*([^*\n]+)', response)
        if source_match:
            return f"🔗 {source_match.group(1)}"
        
        return "❓ Unbekannt"

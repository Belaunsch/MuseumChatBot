"""
Test runner for the Museum Chatbot test suite.
Handles test execution and communication with Rasa server.
"""

import time
import requests
from datetime import datetime
from typing import Dict, Any, List
from ..config import SERVER_CONFIG
from .response_evaluator import ResponseEvaluator


class TestRunner:
    """Handles chatbot test execution and communication with Rasa server"""
    
    def __init__(self):
        self.session_id = f"test_session_{int(time.time())}"
        self.test_results = []
        self.evaluator = ResponseEvaluator()
    
    def check_server_health(self) -> bool:
        """
        Checks if Rasa server is available and responding
        
        Returns:
            bool: True if server is healthy, False otherwise
        """
        try:
            health_check = requests.get(
                f"{SERVER_CONFIG['url']}/status", 
                timeout=SERVER_CONFIG['timeout']
            )
            if health_check.status_code != 200:
                print(f"⚠️ Warnung: Rasa Server Status: {health_check.status_code}")
                return False
            return True
        except Exception as e:
            print(f"❌ Rasa Server nicht erreichbar: {e}")
            print("💡 Bitte starten Sie den Server mit 'rasa run'")
            return False
    
    def send_message(self, message: str) -> Dict[str, Any]:
        """
        Sends a message to the Rasa server and returns the response
        
        Args:
            message: User message to send
            
        Returns:
            dict: Response from server with success status and data
        """
        try:
            payload = {
                "sender": self.session_id,
                "message": message
            }
            
            response = requests.post(
                f"{SERVER_CONFIG['url']}/webhooks/rest/webhook",
                json=payload,
                timeout=SERVER_CONFIG['timeout']
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "responses": response.json(),
                    "status_code": 200
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "status_code": response.status_code
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": None
            }
    
    def run_single_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs a single test case
        
        Args:
            test_case: Test case dictionary with input and expected values
            
        Returns:
            dict: Test result with evaluation and response data
        """
        print(f"\n🧪 Test {test_case['id']}: {test_case['description']}")
        print(f"📝 Eingabe: \"{test_case['input']}\"")
        
        start_time = time.time()
        result = self.send_message(test_case['input'])
        response_time = time.time() - start_time
        
        # Build basic test result
        test_result = {
            "test_id": test_case['id'],
            "description": test_case['description'],
            "category": test_case['category'],
            "input": test_case['input'],
            "expected_intent": test_case.get('expected_intent'),
            "expected_entities": test_case.get('expected_entities', []),
            "timestamp": datetime.now().isoformat(),
            "response_time": round(response_time, 2),
            "success": result['success']
        }
        
        if result['success']:
            test_result = self._process_successful_response(
                test_result, test_case, result, response_time
            )
        else:
            test_result['error'] = result['error']
            test_result['evaluation'] = "ERROR"
            print(f"❌ Fehler: {result['error']}")
        
        return test_result
    
    def _process_successful_response(self, test_result: Dict, test_case: Dict, 
                                   result: Dict, response_time: float) -> Dict:
        """Processes a successful response from the server"""
        responses = result['responses']
        
        if responses:
            print(f"🔍 DEBUG - Anzahl Antworten: {len(responses)}")
            
            # Combine all response messages
            full_response_parts = []
            for response in responses:
                if 'text' in response:
                    full_response_parts.append(response['text'])
            
            bot_response = "\n".join(full_response_parts)
            test_result['bot_response'] = bot_response
            test_result['response_count'] = len(responses)
            test_result['raw_responses'] = responses
            
            # Evaluate the response
            test_result['evaluation'] = self.evaluator.evaluate_response(
                test_case, bot_response, responses
            )
            
            # Display response details
            self._display_response_details(bot_response, responses, response_time)
        else:
            test_result['bot_response'] = "Keine Antwort erhalten"
            test_result['evaluation'] = "FAIL"
            print(f"❌ Keine Antwort erhalten")
        
        return test_result
    
    def _display_response_details(self, bot_response: str, responses: List[Dict], 
                                response_time: float):
        """Displays detailed response information"""
        print(f"✅ Antwort ({response_time:.2f}s):")
        print("📋 " + "="*80)
        
        # Identify API source
        api_source = self.evaluator.identify_api_source(bot_response)
        
        print(f"🔗 API-Quelle: {api_source}")
        print(f"📊 Nachrichten-Teile: {len(responses)}")
        print(f"📏 Gesamtlänge: {len(bot_response)} Zeichen")
        print("\n📋 VOLLSTÄNDIGE ANTWORT:")
        print(bot_response)
        print("="*80)
        print()  # Empty line for better readability
    
    def run_all_tests(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Runs all test cases
        
        Args:
            test_cases: List of test case dictionaries
            
        Returns:
            list: List of test results
        """
        print("🚀 Starte automatisierte Chatbot-Tests")
        print(f"📊 Anzahl Tests: {len(test_cases)}")
        print(f"🔗 Rasa Server: {SERVER_CONFIG['url']}")
        print(f"🆔 Session ID: {self.session_id}")
        
        # Check server availability
        if not self.check_server_health():
            return []
        
        start_time = time.time()
        
        for test_case in test_cases:
            result = self.run_single_test(test_case)
            self.test_results.append(result)
            time.sleep(SERVER_CONFIG['delay_between_tests'])  # Pause between tests
        
        total_time = time.time() - start_time
        print(f"\n✅ Tests abgeschlossen!")
        print(f"🕐 Gesamtzeit: {total_time:.2f} Sekunden")
        
        return self.test_results

"""
Results saver for the Museum Chatbot test suite.
Handles saving and formatting of test results.
"""

import json
from datetime import datetime
from typing import Dict, List, Any
from ..config import TEST_RESULTS_FILE


class ResultsSaver:
    """Handles saving and formatting of test results"""
    
    @staticmethod
    def save_results(test_results: List[Dict[str, Any]], session_id: str, 
                    server_url: str) -> str:
        """
        Saves test results to JSON file
        
        Args:
            test_results: List of test result dictionaries
            session_id: Test session identifier
            server_url: Rasa server URL used for tests
            
        Returns:
            str: Path to saved results file
        """
        results_data = {
            "metadata": {
                "test_run_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "total_tests": len(test_results),
                "rasa_server": server_url,
                "summary": ResultsSaver._generate_summary(test_results)
            },
            "results": test_results
        }
        
        with open(TEST_RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Ergebnisse gespeichert in: {TEST_RESULTS_FILE}")
        ResultsSaver._print_summary(results_data["metadata"]["summary"])
        
        return TEST_RESULTS_FILE
    
    @staticmethod
    def _generate_summary(test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generates a summary of test results"""
        if not test_results:
            return {"total": 0, "by_evaluation": {}, "by_category": {}}
        
        # Count by evaluation result
        evaluation_counts = {}
        category_counts = {}
        
        for result in test_results:
            evaluation = result.get('evaluation', 'UNKNOWN')
            category = result.get('category', 'unknown')
            
            evaluation_counts[evaluation] = evaluation_counts.get(evaluation, 0) + 1
            
            if category not in category_counts:
                category_counts[category] = {'total': 0, 'passed': 0, 'failed': 0}
            
            category_counts[category]['total'] += 1
            
            if evaluation == 'PASS':
                category_counts[category]['passed'] += 1
            elif evaluation in ['FAIL', 'ERROR', 'NO_RESULTS']:
                category_counts[category]['failed'] += 1
        
        return {
            "total": len(test_results),
            "by_evaluation": evaluation_counts,
            "by_category": category_counts,
            "success_rate": round(
                (evaluation_counts.get('PASS', 0) / len(test_results)) * 100, 1
            ) if test_results else 0
        }
    
    @staticmethod
    def _print_summary(summary: Dict[str, Any]):
        """Prints a formatted summary of test results"""
        print("\n📊 TEST ZUSAMMENFASSUNG:")
        print("=" * 50)
        print(f"Gesamt Tests: {summary['total']}")
        print(f"Erfolgsrate: {summary['success_rate']}%")
        
        print("\n📈 Nach Bewertung:")
        for evaluation, count in summary['by_evaluation'].items():
            emoji = {
                'PASS': '✅',
                'PARTIAL': '🟡',
                'FAIL': '❌',
                'ERROR': '🔥',
                'NO_RESULTS': '🚫',
                'UNKNOWN': '❓'
            }.get(evaluation, '❓')
            print(f"  {emoji} {evaluation}: {count}")
        
        print("\n📂 Nach Kategorie:")
        for category, stats in summary['by_category'].items():
            success_rate = round(
                (stats['passed'] / stats['total']) * 100, 1
            ) if stats['total'] > 0 else 0
            print(f"  {category.upper()}: {stats['passed']}/{stats['total']} ({success_rate}%)")
    
    @staticmethod
    def load_results(file_path: str = None) -> Dict[str, Any]:
        """
        Loads test results from JSON file
        
        Args:
            file_path: Path to results file (defaults to TEST_RESULTS_FILE)
            
        Returns:
            dict: Loaded results data
        """
        if file_path is None:
            file_path = TEST_RESULTS_FILE
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Ergebnisdatei nicht gefunden: {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"❌ Fehler beim Laden der Ergebnisdatei: {file_path}")
            return {}

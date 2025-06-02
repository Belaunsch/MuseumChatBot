"""
Wikipedia API client for artwork and artist information retrieval
"""
import requests
import urllib.parse
from typing import Dict, Any, List, Tuple
from .logging_config import setup_logger
from .mappings import WIKIPEDIA_ARTWORK_MAPPINGS, KNOWN_ARTISTS # Ensure KNOWN_ARTISTS is imported
from .validation import is_artwork_content, calculate_relevance_score, calculate_artist_relevance

logger = setup_logger(__name__)

class WikipediaClient:
    """Client for interacting with Wikipedia API"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.base_urls = {
            'de': 'https://de.wikipedia.org',
            'en': 'https://en.wikipedia.org'
        }
    
    def _make_request(self, url: str) -> Dict[str, Any]:
        """
        Make a request to Wikipedia API
        
        Args:
            url: Wikipedia API URL
            
        Returns:
            API response data or empty dict on error
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.debug(f"Request error for {url}: {e}")
        return {}
    
    def search_artwork(self, query: str) -> Dict[str, Any]:
        """
        Improved Wikipedia search with precise mappings for artworks
        
        Args:
            query: Artwork name to search for
            
        Returns:
            Best matching Wikipedia data or empty dict
        """
        try:
            query_lower = query.lower().strip()
            best_result = None
            best_score = 0
            
            # 1. Use precise mappings if available
            if query_lower in WIKIPEDIA_ARTWORK_MAPPINGS:
                search_term = WIKIPEDIA_ARTWORK_MAPPINGS[query_lower]
                logger.info(f"Using precise mapping: {query} -> {search_term}")
                
                # Try German Wikipedia first
                for lang, base_url in [('de', self.base_urls['de']), ('en', self.base_urls['en'])]:
                    url = f"{base_url}/api/rest_v1/page/summary/{urllib.parse.quote(search_term)}"
                    data = self._make_request(url)
                    
                    if data:
                        extract = data.get("extract", "")
                        title = data.get("title", "")
                        
                        if is_artwork_content(extract, title):
                            data['language'] = lang
                            logger.info(f"Found precise match: {title} ({lang})")
                            return data
            
            # 2. Fallback: Normal search with various variants
            search_variants = [
                query.replace(' ', '_'),
                f"{query.replace(' ', '_')}_(painting)",
                f"{query.replace(' ', '_')}_(artwork)",
                f"{query.replace(' ', '_')}_(Gemälde)"
            ]
            
            for lang, base_url in [('de', self.base_urls['de']), ('en', self.base_urls['en'])]:
                for variant in search_variants:
                    url = f"{base_url}/api/rest_v1/page/summary/{urllib.parse.quote(variant)}"
                    data = self._make_request(url)
                    
                    if data:
                        extract = data.get("extract", "")
                        title = data.get("title", "")
                        
                        if is_artwork_content(extract, title):
                            score = calculate_relevance_score(query, title, extract)
                            if score > best_score:
                                best_score = score
                                best_result = data
                                best_result['language'] = lang
                                
                            # Very high score = perfect match
                            if score > 85:
                                logger.info(f"High-score match: {title} (score: {score})")
                                return data # Return data directly, not best_result
            
            if best_result:
                logger.info(f"Best Wikipedia result: {best_result.get('title')} (score: {best_score})")
            else:
                logger.warning(f"No valid artwork found on Wikipedia for: {query}")
            
            return best_result or {}
            
        except Exception as e:
            logger.error(f"Wikipedia API error: {e}")
            return {}
    
    def search_artist(self, artist_name: str) -> Dict[str, Any]:
        """
        Search for artist information on Wikipedia
        
        Args:
            artist_name: Name of the artist to search for (expected to be pre-processed by caller if needed)
            
        Returns:
            Best matching Wikipedia data or empty dict
        """
        try:
            query_for_relevance = artist_name
            effective_base_name = KNOWN_ARTISTS.get(artist_name.lower(), artist_name)
            
            if effective_base_name.lower() != artist_name.lower():
                logger.info(f"Original search term '{artist_name}' will use base '{effective_base_name}' for generating variants due to KNOWN_ARTISTS mapping.")
            else:
                logger.info(f"Effective base name for search variants is '{effective_base_name}'.")

            variants_to_try = []
            suffixes = [" (Maler)", " (Künstler)", " (Artist)", " (Painter)", " (Bildhauer)", " (sculptor)"]
            
            # Priority 1: The effective base name and its direct variants
            variants_to_try.append(effective_base_name)
            for suffix in suffixes:
                variants_to_try.append(effective_base_name + suffix)

            # Priority 2: If the original artist_name was different and shorter
            if artist_name.lower() != effective_base_name.lower() and len(artist_name) < len(effective_base_name):
                logger.debug(f"Adding original name '{artist_name}' and its variants as lower priority fallbacks.")
                variants_to_try.append(artist_name)
                for suffix in suffixes:
                    variants_to_try.append(artist_name + suffix)
            
            # Heuristics for very famous names
            current_base_lower_for_heuristics = effective_base_name.lower()
            if "pablo" not in current_base_lower_for_heuristics and "picasso" in current_base_lower_for_heuristics:
                variants_to_try.extend(["Pablo Picasso", "Pablo Picasso (Maler)"])
            if "vincent" not in current_base_lower_for_heuristics and "van gogh" in current_base_lower_for_heuristics:
                variants_to_try.extend(["Vincent van Gogh", "Vincent van Gogh (Maler)"])
            if current_base_lower_for_heuristics == "leonardo": # Specifically for "Leonardo"
                 variants_to_try.extend(["Leonardo da Vinci", "Leonardo da Vinci (Maler)"])
            
            final_search_variants = []
            seen_variants_lower = set()
            for v in variants_to_try:
                v_lower = v.lower()
                if v_lower not in seen_variants_lower:
                    final_search_variants.append(v)
                    seen_variants_lower.add(v_lower)
            
            logger.info(f"Searching Wikipedia for artist related to '{query_for_relevance}'. Effective base: '{effective_base_name}'. Variants: {final_search_variants}")

            best_result = None
            best_score = 0
            
            # German Wikipedia first
            for variant in final_search_variants:
                logger.debug(f"Trying variant: '{variant}' on German Wikipedia")
                url = f"{self.base_urls['de']}/api/rest_v1/page/summary/{urllib.parse.quote(variant)}"
                data = self._make_request(url)
                
                if data:
                    extract = data.get("extract", "")
                    title = data.get("title", "") # Keep original case from API
                    
                    score = calculate_artist_relevance(query_for_relevance, title, extract)
                    logger.debug(f"Variant '{variant}' (de) - Page: '{title}', Score: {score}, Extract length: {len(extract)}")

                    if score > best_score and len(extract) > 50:
                        best_score = score
                        logger.debug(f"New best score {score} for '{title}'. Fetching detailed content.")
                        detailed_data = self._get_detailed_content(data.get('title', variant), 'de')
                        best_result = detailed_data if detailed_data else data
                        if best_result: # Ensure best_result is not None before adding key
                           best_result['language'] = 'de'
                        
                    if score > 90: # Increased threshold for high-confidence match
                        logger.info(f"High-score artist match (de): {title} (score: {score})")
                        detailed_data = self._get_detailed_content(data.get('title', variant), 'de')
                        # Ensure data is not None before adding key
                        final_data = detailed_data if detailed_data else data
                        if final_data:
                            final_data['language'] = 'de' # Add language here too
                        return final_data # Return the fetched data
            
            # English Wikipedia as fallback
            if not best_result or best_score < 60:
                logger.info(f"German Wikipedia search for '{query_for_relevance}' (base: '{effective_base_name}') yielded score {best_score}. Trying English Wikipedia.")
                for variant in final_search_variants:
                    logger.debug(f"Trying variant: '{variant}' on English Wikipedia")
                    url = f"{self.base_urls['en']}/api/rest_v1/page/summary/{urllib.parse.quote(variant)}"
                    data = self._make_request(url)
                    
                    if data:
                        extract = data.get("extract", "")
                        title = data.get("title", "") # Keep original case
                        
                        score = calculate_artist_relevance(query_for_relevance, title, extract)
                        logger.debug(f"Variant '{variant}' (en) - Page: '{title}', Score: {score}, Extract length: {len(extract)}")
                        
                        if score > best_score and len(extract) > 50:
                            best_score = score
                            logger.debug(f"New best score {score} for '{title}'. Fetching detailed content.")
                            detailed_data = self._get_detailed_content(data.get('title', variant), 'en')
                            best_result = detailed_data if detailed_data else data
                            if best_result: # Ensure best_result is not None
                                best_result['language'] = 'en'
            
            if best_result:
                logger.info(f"Best artist result for '{query_for_relevance}' (base: '{effective_base_name}'): {best_result.get('title')} (score: {best_score}, lang: {best_result.get('language')})")
            else:
                logger.warning(f"No artist information found for: '{query_for_relevance}' (base: '{effective_base_name}') after trying all variants.")
            
            return best_result or {}
            
        except Exception as e:
            logger.error(f"Wikipedia Artist API error: {e}", exc_info=True) # Added exc_info=True
            return {}
    
    def _get_detailed_content(self, title: str, language: str = 'de') -> Dict[str, Any]:
        """
        Get detailed Wikipedia content including full text for better biographical extraction
        
        Args:
            title: Wikipedia page title
            language: Language code ('de' or 'en')
            
        Returns:
            Detailed Wikipedia data including full content
        """
        try:
            base_url = self.base_urls[language]
            summary_data = {} # Initialize summary_data
            
            # Try to get summary first (it might contain 'pageid' or other useful info)
            summary_url = f"{base_url}/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
            summary_data_raw = self._make_request(summary_url)
            if summary_data_raw: # Check if data was successfully fetched
                summary_data = summary_data_raw

            api_url = f"{base_url}/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'titles': title,
                'prop': 'extracts',
                'exintro': True, # Get only the intro section
                'explaintext': True,
                'exsectionformat': 'plain',
                'exlimit': 1
            }
            
            response = requests.get(api_url, params=params, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                pages = data.get('query', {}).get('pages', {})
                
                if pages:
                    page_id = next(iter(pages.keys()))
                    page_data = pages[page_id]
                    
                    # Ensure summary_data has 'extract' key before comparing lengths
                    current_extract_len = len(summary_data.get('extract', ''))
                    if 'extract' in page_data and len(page_data['extract']) > current_extract_len:
                        summary_data['extract'] = page_data['extract']
                        # Preserve other fields from summary_data if they exist (like title, pageid, etc.)
                        summary_data['title'] = page_data.get('title', summary_data.get('title', title))
                        logger.info(f"Got detailed extract for {title} ({len(page_data['extract'])} chars)")
            
            # Ensure 'language' is set in the returned data
            if summary_data and 'language' not in summary_data:
                 summary_data['language'] = language
            return summary_data # Return summary_data which might have been updated
            
        except Exception as e:
            logger.debug(f"Error getting detailed content for {title}: {e}")
            return {} # Return empty dict on error

# Global instance for easy import
wikipedia_client = WikipediaClient()

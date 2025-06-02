"""
Text summarization and biographical information extraction utilities
"""
import re
from typing import Dict, List
from .logging_config import setup_logger

logger = setup_logger(__name__)

def clean_text_content(text: str) -> str:
    """
    Clean text content by removing phonetic pronunciations and citations
    
    Args:
        text: Raw text content
        
    Returns:
        Cleaned text content
    """
    if not text:
        return ""
    
    # Remove phonetic pronunciations in square brackets
    # Patterns like [pronunciation], [ˈmoʊnə ˈliːsə], etc.
    text = re.sub(r'\[[\w\s\'\'\ˈˌɪəæʊʌɜːɔɑɒɛeɐaɨɯuoəɪʊeæɑɒɔɛɪʊɜːɑːɔːiːuːʌəæɪeɔaɨɯuoəʊaɪeɪoʊ\.\-\,\;\:\(\)\/\s]*\]', '', text)
    
    # Remove other common citation patterns
    text = re.sub(r'\[.*?\]', '', text)  # Any remaining square brackets
    text = re.sub(r'\.\.\.', '', text)   # Ellipsis
    text = re.sub(r'\s+', ' ', text)     # Multiple spaces
    
    return text.strip()

def summarize_wikipedia_content(extract: str, artwork_name: str) -> str:
    """
    Intelligent summarization instead of 1:1 reproduction
    
    Args:
        extract: Raw Wikipedia extract
        artwork_name: Name of the artwork
        
    Returns:
        Summarized content (2-3 sentences)
    """
    if not extract:
        return ""
    
    # Clean the text content first
    extract = clean_text_content(extract)
    
    # Shorten to reasonable length (2-3 sentences)
    sentences = extract.split('. ')
    
    if len(sentences) <= 3:
        summary = extract
    else:
        # Choose the most important 2-3 sentences
        important_sentences = []
        
        # First sentence is usually the most important
        if sentences[0]:
            important_sentences.append(sentences[0])
        
        # Look for sentences with artwork-relevant terms
        art_keywords = ['gemalt', 'geschaffen', 'entstanden', 'painted', 'created', 'famous', 'berühmt', 'museum']
        
        for sentence in sentences[1:]:
            if len(important_sentences) >= 3:
                break
            if any(keyword in sentence.lower() for keyword in art_keywords):
                important_sentences.append(sentence)
        
        # Fill with additional sentences if needed
        for sentence in sentences[1:]:
            if len(important_sentences) >= 3:
                break
            if sentence not in important_sentences and len(sentence) > 20:
                important_sentences.append(sentence)
        
        summary = '. '.join(important_sentences)
        if not summary.endswith('.'):
            summary += '.'
    
    # Remove very long sentences (over 400 characters)
    if len(summary) > 400:
        summary = summary[:400] + "..."
    
    return summary.strip()

def extract_artist_from_wikipedia(extract: str, language: str = 'de') -> str:
    """
    Intelligently extracts artist names from Wikipedia text
    
    Args:
        extract: Wikipedia extract text
        language: Language of the extract ('de' or 'en')
        
    Returns:
        Artist name or "Unbekannter Künstler"
    """
    if not extract:
        return "Unbekannter Künstler"
    
    # Patterns for German and English texts
    if language == 'de':
        artist_patterns = [
            r'ist ein (?:weltberühmtes )?(?:öl)?gemälde (?:des|von) ([A-Z][a-z]+ (?:da |van |de )?[A-Z][a-z]+)',
            r'(?:öl)?gemälde (?:des|von) ([A-Z][a-z]+ (?:da |van |de )?[A-Z][a-z]+)',
            r'wurde (?:von|durch) ([A-Z][a-z]+ (?:da |van |de )?[A-Z][a-z]+) (?:gemalt|geschaffen)',
            r'([A-Z][a-z]+ (?:da |van |de )?[A-Z][a-z]+) (?:malte|schuf|erstellte)',
            r'des (?:italienischen |französischen |niederländischen |deutschen |spanischen )?(?:Malers |Künstlers )?([A-Z][a-z]+ (?:da |van |de )?[A-Z][a-z]+)'
        ]
    else:
        artist_patterns = [
            r'is (?:a )?(?:famous )?(?:oil )?painting by ([A-Z][a-z]+ (?:da |van |de |del )?[A-Z][a-z]+)',
            r'(?:oil )?painting by ([A-Z][a-z]+ (?:da |van |de |del )?[A-Z][a-z]+)',
            r'painted by ([A-Z][a-z]+ (?:da |van |de |del )?[A-Z][a-z]+)',
            r'created by ([A-Z][a-z]+ (?:da |van |de |del )?[A-Z][a-z]+)',
            r'([A-Z][a-z]+ (?:da |van |de |del )?[A-Z][a-z]+) painted',
            r'by (?:the )?(?:Dutch |Italian |French |German |Spanish )?(?:artist |painter )?([A-Z][a-z]+ (?:da |van |de |del )?[A-Z][a-z]+)'
        ]
    
    for pattern in artist_patterns:
        match = re.search(pattern, extract)
        if match:
            artist = match.group(1).strip()
            # Validate the name
            if len(artist) > 3 and ' ' in artist and not any(bad in artist.lower() for bad in ['unknown', 'unbekannt']):
                logger.info(f"Artist extracted from Wikipedia: {artist}")
                return artist
    
    return "Unbekannter Künstler"

def extract_biographical_info(extract: str, artist_name: str) -> Dict[str, str]:
    """
    Extracts biographical information from Wikipedia text
    
    Args:
        extract: Wikipedia extract text
        artist_name: Name of the artist
        
    Returns:
        Dictionary with biographical information
    """
    info = {}
      # Enhanced patterns for birth date extraction
    birth_patterns = [
        # German Wikipedia patterns with * symbol
        r'\(\*\s*(\d{1,2}\.\s*\w+\s*\d{4})',  # (* 30. März 1853
        r'\(\*\s*(\d{4})',                     # (* 1853
        r'\*\s*(\d{1,2}\.\s*\w+\s*\d{4})',    # * 30. März 1853
        r'\*\s*(\d{4})',                       # * 1853
        # Standard German patterns
        r'geboren am (\d{1,2}\.\s*\w+\s*\d{4})',
        r'geboren (\d{4})',
        r'(\d{4})\s*geboren',
        # English patterns
        r'born (\d{1,2}\s+\w+\s+\d{4})',
        r'born (\d{4})',
        r'born on (\d{1,2}\s+\w+\s+\d{4})',
        r'born in (\d{4})',
        # Common Wikipedia parenthetical patterns
        r'\((\d{4})[-–]\d{4}\)',  # (1853–1890)
        r'\((\d{4})[-–]\)',       # (1853–)
        # Artist name followed by years pattern
        rf'{re.escape(artist_name)}.*?\((\d{{4}})[-–]',
        # General year patterns in first sentence
        r'war.*?(\d{4}).*?geboren',
        r'was.*?born.*?(\d{4})'
    ]
    
    for pattern in birth_patterns:
        match = re.search(pattern, extract, re.IGNORECASE)
        if match:
            birth_info = match.group(1)
            # Extract just the year from the date
            year_match = re.search(r'\d{4}', birth_info)
            if year_match:
                birth_year = year_match.group()
                # Validate year (reasonable range for artists)
                if birth_year.isdigit() and 1200 <= int(birth_year) <= 2010:
                    info['birth_date'] = birth_year
                    break
      # Birth place
    birthplace_patterns = [
        r'geboren.*?in ([A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)*)',
        r'born in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'aus ([A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)*)'
    ]
    
    for pattern in birthplace_patterns:
        match = re.search(pattern, extract)
        if match:
            place = match.group(1)
            if len(place) > 2 and place not in ['Der', 'Die', 'Das', 'The']:
                info['birth_place'] = place
                break
      # Enhanced patterns for death date extraction
    death_patterns = [
        # German Wikipedia patterns with † symbol
        r'†\s*(\d{1,2}\.\s*\w+\s*\d{4})',     # † 29. Juli 1890
        r'†\s*(\d{4})',                        # † 1890
        r';\s*†\s*(\d{1,2}\.\s*\w+\s*\d{4})', # ; † 29. Juli 1890
        r';\s*†\s*(\d{4})',                    # ; † 1890
        # Standard German patterns
        r'gestorben am (\d{1,2}\.\s*\w+\s*\d{4})',
        r'gestorben (\d{4})',
        r'(\d{4})\s*gestorben',
        # English patterns
        r'died (\d{1,2}\s+\w+\s+\d{4})',
        r'died (\d{4})',
        r'died on (\d{1,2}\s+\w+\s+\d{4})',
        r'died in (\d{4})',
        # Common Wikipedia parenthetical patterns
        r'\(\d{4}[-–](\d{4})\)',  # (1853–1890)
        r'[-–](\d{4})\)',         # –1890)
        # Artist name followed by years pattern
        rf'{re.escape(artist_name)}.*?\(\d{{4}}[-–](\d{{4}})\)',
        # General year patterns
        r'war.*?(\d{4}).*?gestorben',
        r'died.*?(\d{4})'
    ]
    
    for pattern in death_patterns:
        match = re.search(pattern, extract, re.IGNORECASE)
        if match:
            death_info = match.group(1)
            # Extract just the year from the date
            year_match = re.search(r'\d{4}', death_info)
            if year_match:
                death_year = year_match.group()
                # Validate year (reasonable range for artists)
                if death_year.isdigit() and 1300 <= int(death_year) <= 2025:
                    info['death_date'] = death_year
                    break
    
    # Nationality
    nationality_patterns = [
        r'war ein(?:e)? (\w+(?:isch|sch))(?:e|er)? ',
        r'was a (\w+) '
    ]
    
    for pattern in nationality_patterns:
        match = re.search(pattern, extract)
        if match:
            nationality = match.group(1)
            if nationality.lower() not in ['bedeutend', 'bekannt', 'famous', 'well-known']:
                info['nationality'] = nationality
                break
    
    return info

def summarize_artist_biography(extract: str, artist_name: str) -> str:
    """
    Intelligently summarizes artist biography content for clean presentation
    
    Args:
        extract: Raw Wikipedia extract about the artist
        artist_name: Name of the artist
        
    Returns:
        Clean, readable biography summary without birth/death info
    """
    if not extract:
        return ""
    
    # Clean the text content first
    extract = clean_text_content(extract)
      # Remove birth/death information patterns that we'll show separately
    # German patterns - be more careful with removal
    extract = re.sub(r'\(\*\s*\d{1,2}\.\s*\w+\s*\d{4}[^)]*\)', '', extract)  # Remove (* date ) patterns
    extract = re.sub(r'†\s*\d{1,2}\.\s*\w+\s*\d{4}[^.]*\.?', '', extract)  # Remove † date patterns
    extract = re.sub(r'geboren\s+am\s+\d{1,2}\.\s*\w+\s*\d{4}[^.]*\.?', '', extract)  # Remove geboren am ...
    extract = re.sub(r'gestorben\s+am\s+\d{1,2}\.\s*\w+\s*\d{4}[^.]*\.?', '', extract)  # Remove gestorben am ...
    
    # English patterns  
    extract = re.sub(r'born\s+\d{1,2}\s+\w+\s+\d{4}[^.]*\.?', '', extract)  # Remove born date
    extract = re.sub(r'died\s+\d{1,2}\s+\w+\s+\d{4}[^.]*\.?', '', extract)  # Remove died date
      # Clean up leading fragments that might remain (like "Mai 1519 auf...")
    extract = re.sub(r'^[A-Z][a-z]+\s+\d{4}\s+auf\s+[^;]*;\s*', '', extract)  # Remove death info at start like "Mai 1519 auf Schloss Clos Lucé;"
    extract = re.sub(r'^eigentlich\s+[^)]*\)\s*', '', extract)  # Remove "eigentlich ..." at start
      # Clean up extra spaces and punctuation
    extract = re.sub(r'\s+', ' ', extract)
    extract = re.sub(r'\s*[,;]\s*\.', '.', extract)  # Fix punctuation
    extract = extract.strip()
    
    # Fix sentence fragments that start with artist name
    # Pattern: "Leonardo da Vinci ; Er gilt als..." -> "Er gilt als..."
    artist_name_simple = artist_name.split()[-1] if artist_name else ""
    if artist_name_simple and extract.startswith(artist_name):
        # Remove redundant artist name at beginning
        remaining = extract[len(artist_name):].strip()
        if remaining.startswith(';') or remaining.startswith(','):
            remaining = remaining[1:].strip()
        if remaining and remaining[0].isupper():
            extract = remaining
        elif remaining and not remaining[0].isupper():
            # Capitalize first letter if needed
            extract = remaining[0].upper() + remaining[1:] if len(remaining) > 1 else remaining.upper()
    
    # Fix sentence start if it begins with a lowercase letter or incomplete fragment
    if extract and not extract[0].isupper():
        # Find the first complete sentence that starts with uppercase
        sentences = extract.split('. ')
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if sentence and sentence[0].isupper() and len(sentence) > 30:
                extract = '. '.join(sentences[i:])
                break
    
    # Split into sentences and select the most relevant ones
    sentences = extract.split('. ')
    clean_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20:  # Skip very short fragments
            # Skip sentences that are just birth/death remnants
            if not re.match(r'^[\d\s.,;†*-]+$', sentence):
                clean_sentences.append(sentence)
    
    # Select the best 2-3 sentences for biography
    if len(clean_sentences) <= 3:
        result = '. '.join(clean_sentences)
    else:
        # Prioritize sentences with artist-relevant terms
        artist_keywords = ['maler', 'künstler', 'bildhauer', 'zeichner', 'painter', 'artist', 'sculptor', 
                          'stil', 'werk', 'gemälde', 'style', 'work', 'painting', 'berühmt', 'famous',
                          'bewegung', 'movement', 'kunst', 'art']
        
        important_sentences = []
        
        # Add first sentence if it's substantial
        if clean_sentences[0] and len(clean_sentences[0]) > 30:
            important_sentences.append(clean_sentences[0])
        
        # Add sentences with relevant keywords
        for sentence in clean_sentences[1:]:
            if len(important_sentences) >= 3:
                break
            if any(keyword in sentence.lower() for keyword in artist_keywords):
                important_sentences.append(sentence)
        
        # Fill up to 3 sentences if needed
        for sentence in clean_sentences:
            if len(important_sentences) >= 3:
                break
            if sentence not in important_sentences and len(sentence) > 30:
                important_sentences.append(sentence)
        
        result = '. '.join(important_sentences)
    
    # Ensure proper ending
    if result and not result.endswith('.'):
        result += '.'
    
    # Limit length
    if len(result) > 500:
        result = result[:500] + "..."
    
    return result.strip()

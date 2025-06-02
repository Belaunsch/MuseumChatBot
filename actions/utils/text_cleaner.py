"""
Text cleaning and normalization utilities for artwork and artist names
"""
import re
from typing import List
from .logging_config import setup_logger
from .mappings import KNOWN_ARTWORKS, KNOWN_ARTISTS

logger = setup_logger(__name__)

def clean_artwork_name(artwork: str) -> str:
    """
    Cleans and normalizes artwork names
    
    Args:
        artwork: Raw artwork name to clean
        
    Returns:
        Cleaned artwork name
    """
    artwork = artwork.strip()
    
    # Remove punctuation at the end
    artwork = artwork.rstrip('?').rstrip('.').rstrip(',').rstrip('!').strip()
    
    # Remove disruptive words
    cleanup_words = ['bitte', 'heute', 'gerade', 'momentan', 'mal', 'denn', 'eigentlich', 'hier']
    words = artwork.split()
    filtered_words = [word for word in words if word.lower() not in cleanup_words]
    artwork = ' '.join(filtered_words).strip()
    
    return artwork

def clean_artist_name(artist: str) -> str:
    """
    Cleans and normalizes artist names
    
    Args:
        artist: Raw artist name to clean
        
    Returns:
        Cleaned artist name
    """
    artist = artist.strip()
    
    # Remove punctuation at the end
    artist = artist.rstrip('?').rstrip('.').rstrip(',').strip()
    
    # Remove common cleanup words
    cleanup_words = ['von', 'über', 'dem', 'der', 'die', 'das']
    artist_words = [w for w in artist.split() if w not in cleanup_words]
    artist = ' '.join(artist_words)
    
    return artist

def extract_artwork_from_message(message: str) -> str:
    """
    Extracts artwork names from user messages with improved accuracy
    
    Args:
        message: User's message
        
    Returns:
        Extracted artwork name or cleaned message
    """
    message_lower = message.lower().strip()
    
    # Check direct matches in known artworks first
    for key, value in KNOWN_ARTWORKS.items():
        if key in message_lower:
            logger.info(f"Direct artwork match found: '{key}' -> '{value}'")
            return value
    
    # Extended patterns for artwork extraction
    # Order patterns from more specific to more general
    patterns = [
        r'(?:erzähl mir(?: etwas)? über|was weißt du über|informationen zu(?:m Kunstwerk|r)?|zeig mir|suche nach|wer hat|von wem ist) (?:das |die |der )?(.+?)(?:\?| bitte|$)',
        r'(?:über|zu|nach) (?:das |die |der )?(.+?)(?:\?| bitte|$)', # More general cases
    ]
    
    extracted_artwork = None
    for pattern in patterns:
        match = re.search(pattern, message_lower)
        if match:
            artwork_candidate = match.group(1).strip()
            # Remove common trailing words that are not part of the artwork title
            artwork_candidate = re.sub(r'\s+(gemalt|gezeichnet|erstellt|geschaffen|bitte)$' , '', artwork_candidate, flags=re.IGNORECASE).strip()
            artwork_candidate = clean_artwork_name(artwork_candidate) # Apply general cleaning
            
            if len(artwork_candidate) > 2: # Ensure it's not just an article or short word
                # Prioritize longer matches if multiple patterns match
                if extracted_artwork is None or len(artwork_candidate) > len(extracted_artwork):
                    extracted_artwork = artwork_candidate
                    logger.info(f"Artwork candidate from pattern '{pattern}': '{extracted_artwork}'")

    if extracted_artwork:
        logger.info(f"Final extracted artwork: '{extracted_artwork.title()}'")
        return extracted_artwork.title() # Return in Title Case
    
    # Fallback: clean the entire message if no specific pattern matched
    cleaned_message = clean_artwork_name(message)
    logger.info(f"No specific artwork pattern matched. Returning cleaned message: '{cleaned_message}'")
    return cleaned_message if len(cleaned_message) > 2 else message.strip()

def extract_artist_from_message(message: str) -> str:
    """
    Extracts artist names from user messages
    
    Args:
        message: User's message
        
    Returns:
        Extracted artist name or cleaned message
    """
    message_lower = message.lower().strip()
    
    # Check direct matches in known artists first
    for key, value in KNOWN_ARTISTS.items():
        if key in message_lower:
            return value
    
    # Patterns for artist extraction (extended for specific questions)
    patterns = [
        r'wann wurde (.+?) geboren',
        r'wann ist (.+?) gestorben',
        r'wo wurde (.+?) geboren',
        r'wer war (.+?)(?:\?|$)',
        r'erzähl mir (?:etwas |von )?(?:über )?(.+?)(?:\?|$)',
        r'was weißt du über (.+?)(?:\?|$)',
        r'informationen zu(?:m Künstler)? (.+?)(?:\s+bitte)?(?:\?|$)',
        r'biographie (?:von |über )?(.+?)(?:\?|$)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message_lower)
        if match:
            artist = match.group(1).strip()
            artist = clean_artist_name(artist)
            
            if len(artist) > 2:
                # Check if cleaned name matches known artists
                for key, value in KNOWN_ARTISTS.items():
                    if key == artist.lower():
                        return value
                return artist.title()
    
    return message.strip()

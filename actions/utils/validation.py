"""
Validation and scoring functions for artwork and artist content
"""
from typing import List
from .logging_config import setup_logger

logger = setup_logger(__name__)

def is_artwork_content(extract: str, title: str = "") -> bool:
    """
    CRITICAL validation: Prevents false Wikipedia associations
    
    Args:
        extract: Wikipedia extract text
        title: Wikipedia page title
        
    Returns:
        True if content is artwork-related, False otherwise
    """
    if not extract or len(extract) < 20:
        return False
    
    extract_lower = extract.lower()
    title_lower = title.lower() if title else ""
      # STRONG exclusion criteria - Definitely NOT art
    exclude_terms = [
        # Software/Technology
        'software', 'program', 'application', 'astronomy', 'computer',
        'astronomie-software', 'planetarium', 'imaginova corp', 'video game',
        
        # Media
        'film von', 'movie', 'fernsehserie', 'tv series', 'tv show',
        'band', 'musikgruppe', 'album', 'song', 'lied', 'musical',
        
        # Disambiguation pages
        'steht für:', 'disambiguation', 'begriffsklärung', 'may refer to',
        'refers to', 'can refer to',
        
        # Companies/Organizations
        'unternehmen', 'company', 'firma', 'corporation', 'organization',
        
        # Politics/People (but not artists)
        'politik', 'politiker', 'president', 'minister', 'chancellor',
        
        # Other non-art content
        'asteroid', 'book', 'buch', 'novel', 'roman', 'spiel'
    ]
      # Check for exclusion criteria - but allow if strong art indicators are present
    found_excludes = [term for term in exclude_terms if term in extract_lower or term in title_lower]
    if found_excludes:
        # Check for strong art indicators that override exclusions
        strong_art_indicators = [
            'painting', 'gemälde', 'oil painting', 'ölgemälde', 'canvas', 'leinwand',
            'painted by', 'gemalt von', 'artist', 'künstler', 'maler', 'painter',
            'museum', 'gallery', 'galerie', 'artwork', 'kunstwerk', 'masterpiece',
            'van gogh', 'picasso', 'leonardo', 'da vinci', 'monet', 'vermeer'
        ]
        
        # Count strong art indicators
        strong_indicators_count = sum(1 for indicator in strong_art_indicators 
                                    if indicator in extract_lower or indicator in title_lower)
        
        # If we have strong art indicators (2+), allow even with exclusion terms
        if strong_indicators_count < 2:
            logger.info(f"Content excluded due to: {found_excludes} (not enough art indicators: {strong_indicators_count})")
            return False
    
    # POSITIVE indicators for artworks (at least one must be present)
    art_indicators = [
        # German
        'gemälde', 'kunstwerk', 'ölgemälde', 'bild', 'malerei',
        'künstler', 'maler', 'kunst', 'museum', 'galerie',
        'renaissance', 'barock', 'impressionismus', 'expressionismus',
        'leinwand', 'pinsel', 'farbe', 'ausstellung',
        
        # English
        'painting', 'artwork', 'art work', 'artist', 'painter',
        'museum', 'gallery', 'canvas', 'oil painting', 'exhibition',
        'masterpiece', 'art history', 'fine art',
        
        # Famous artists (strong indicators)
        'leonardo da vinci', 'van gogh', 'picasso', 'vermeer', 'monet',
        'renoir', 'degas', 'cézanne', 'manet', 'toulouse-lautrec',
        'michelangelo', 'raphael', 'botticelli', 'caravaggio',
        'rembrandt', 'rubens', 'dürer', 'hokusai', 'frida kahlo',
        
        # Art movements/periods
        'renaissance', 'baroque', 'impressionist', 'post-impressionist',
        'expressionist', 'cubism', 'surrealism', 'abstract'
    ]
    
    # Count positive indicators
    art_score = sum(1 for indicator in art_indicators if indicator in extract_lower or indicator in title_lower)
    
    logger.info(f"Art validation - Score: {art_score}, Content: {extract[:100]}...")
    return art_score >= 1

def calculate_relevance_score(query: str, title: str, extract: str) -> float:
    """
    Calculates relevance score for Wikipedia results
    
    Args:
        query: Search query
        title: Wikipedia page title
        extract: Wikipedia extract
        
    Returns:
        Relevance score (0-100)
    """
    score = 0
    query_lower = query.lower()
    title_lower = title.lower()
    extract_lower = extract.lower()
    
    # Title match (very important)
    if query_lower == title_lower:
        score += 90
    elif query_lower in title_lower:
        score += 70
    elif any(word in title_lower for word in query_lower.split() if len(word) > 2):
        score += 40
    
    # Artwork terms in extract
    art_keywords = ['gemälde', 'kunstwerk', 'painting', 'artwork', 'künstler', 'artist', 'museum']
    score += sum(10 for keyword in art_keywords if keyword in extract_lower)
    
    # Famous artists increase score
    famous_artists = ['leonardo', 'van gogh', 'picasso', 'vermeer', 'monet', 'michelangelo']
    score += sum(15 for artist in famous_artists if artist in extract_lower)
    
    # Extract length
    if len(extract) > 200:
        score += 10
    elif len(extract) > 100:
        score += 5
    
    return score

def calculate_artist_relevance(artist_name: str, title: str, extract: str) -> float:
    """
    Calculates relevance score for artist results
    
    Args:
        artist_name: Artist name being searched
        title: Wikipedia page title
        extract: Wikipedia extract
        
    Returns:
        Relevance score (0-100)
    """
    score = 0
    artist_lower = artist_name.lower()
    title_lower = title.lower()
    extract_lower = extract.lower()
    
    # Name match (highest priority)
    # Exact match in title
    if artist_lower == title_lower:
        score += 95 # Very high score for exact title match
    # All words of artist_name in title
    elif all(word in title_lower for word in artist_lower.split()):
        score += 85 # High score if all words are present
    # Artist name (or significant part) in title
    elif artist_lower in title_lower:
        score += 70
    # Any significant word from artist name in title
    elif any(word in title_lower for word in artist_lower.split() if len(word) > 3):
        score += 50
    
    # Artist-relevant terms in extract (boost score)
    # Increased weight for core artistic professions
    artist_keywords = {
        "maler": 20, "künstler": 15, "painter": 20, "artist": 15, # Core professions
        "bildhauer": 20, "sculptor": 20, # Sculptor
        "zeichner": 15, "draftsman": 15, # Draftsman
        "grafiker": 15, "graphic artist": 15, # Graphic artist
        "gemälde": 10, "painting": 10, "skulptur": 10, "sculpture": 10, # Art forms
        "werk": 5, "work": 5, # General term for art piece
        "ausstellung": 5, "exhibition": 5, # Exhibitions
        "museum": 5, # Museums
        "galerie": 5, "gallery": 5, # Galleries
        "geboren": 5, "born": 5, "gestorben": 5, "died": 5, # Biographical info
        "biografie": 5, "biography": 5, 
        "kunst": 10, "art": 10 # General art terms
    }
    for keyword, weight in artist_keywords.items():
        if keyword in extract_lower:
            score += weight
            
    # Penalize if extract is too short or seems irrelevant
    if len(extract) < 100:
        score -= 10
    if "disambiguation" in extract_lower or "begriffsklärung" in extract_lower:
        score -= 50 # Heavily penalize disambiguation pages

    # Boost if the title explicitly mentions a profession
    profession_terms = ["(maler)", "(künstler)", "(artist)", "(painter)", "(bildhauer)", "(sculptor)"]
    if any(term in title_lower for term in profession_terms):
        score += 20

    logger.debug(f"Artist relevance for '{artist_name}' | Title: '{title}' | Score: {score} | Extract: {extract[:100]}...")
    return max(0, score) # Ensure score is not negative

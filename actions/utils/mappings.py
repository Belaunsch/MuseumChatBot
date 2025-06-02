"""
Centralized mappings for known artworks and artists
"""
from typing import Dict

# Known artwork mappings with variations and typo tolerance
KNOWN_ARTWORKS: Dict[str, str] = {
    'mona lisa': 'Mona Lisa',
    'die mona lisa': 'Mona Lisa',
    'starry night': 'The Starry Night',
    'the starry night': 'The Starry Night', 
    'sternennacht': 'The Starry Night',
    'die sternennacht': 'The Starry Night',
    'guernica': 'Guernica',
    'girl with a pearl earring': 'Girl with a Pearl Earring',
    'mädchen mit dem perlenohrring': 'Girl with a Pearl Earring',
    'das mädchen mit dem perlenohrring': 'Girl with a Pearl Earring',
    'the scream': 'The Scream',
    'der schrei': 'The Scream',
    'american gothic': 'American Gothic',
    'great wave': 'The Great Wave off Kanagawa',
    'the great wave': 'The Great Wave off Kanagawa',
    'persistence of memory': 'The Persistence of Memory',
    'the persistence of memory': 'The Persistence of Memory',
    'last supper': 'The Last Supper',
    'das letzte abendmahl': 'The Last Supper',
    'birth of venus': 'The Birth of Venus',
    'die geburt der venus': 'The Birth of Venus'
}

# Precise Wikipedia mappings for known artworks
WIKIPEDIA_ARTWORK_MAPPINGS: Dict[str, str] = {
    'mona lisa': 'Mona_Lisa',
    'die mona lisa': 'Mona_Lisa',
    'the starry night': 'The_Starry_Night',
    'starry night': 'The_Starry_Night',
    'sternennacht': 'Sternennacht_(van_Gogh)',
    'die sternennacht': 'Sternennacht_(van_Gogh)',
    'guernica': 'Guernica_(Picasso)',
    'girl with a pearl earring': 'Girl_with_a_Pearl_Earring',
    'das mädchen mit dem perlenohrring': 'Mädchen_mit_dem_Perlenohrgehänge',
    'mädchen mit dem perlenohrring': 'Mädchen_mit_dem_Perlenohrgehänge',
    'the scream': 'The_Scream',
    'der schrei': 'Der_Schrei',
    'american gothic': 'American_Gothic',
    'the great wave off kanagawa': 'The_Great_Wave_off_Kanagawa',
    'great wave': 'The_Great_Wave_off_Kanagawa',
    'the great wave': 'The_Great_Wave_off_Kanagawa',
    'the persistence of memory': 'The_Persistence_of_Memory',
    'persistence of memory': 'The_Persistence_of_Memory',
    'the last supper': 'The_Last_Supper',
    'last supper': 'The_Last_Supper',
    'das letzte abendmahl': 'Das_Abendmahl_(Leonardo_da_Vinci)',
    'the birth of venus': 'The_Birth_of_Venus',
    'birth of venus': 'The_Birth_of_Venus',
    'die geburt der venus': 'Die_Geburt_der_Venus'
}

# Known artist mappings with typo tolerance
KNOWN_ARTISTS: Dict[str, str] = {
    'leonardo da vinci': 'Leonardo da Vinci',
    'leonardo': 'Leonardo da Vinci',
    'vincent van gogh': 'Vincent van Gogh',
    'van gogh': 'Vincent van Gogh',
    'pablo picasso': 'Pablo Picasso',
    'picasso': 'Pablo Picasso',
    'claude monet': 'Claude Monet',
    'monet': 'Claude Monet',
    'johannes vermeer': 'Johannes Vermeer',
    'vermeer': 'Johannes Vermeer',
    'edvard munch': 'Edvard Munch',
    'munch': 'Edvard Munch',
    'frida kahlo': 'Frida Kahlo',
    'rembrandt': 'Rembrandt van Rijn',
    'rembrandzt': 'Rembrandt van Rijn',  # Typo tolerance
    'michelangelo': 'Michelangelo',
    'andy warhol': 'Andy Warhol',
    'georgia o\'keeffe': 'Georgia O\'Keeffe',
    'georgia okeeffe': 'Georgia O\'Keeffe'
}

# Artwork-specific information for enhanced responses
ARTWORK_INFO: Dict[str, Dict[str, str]] = {
    'mona lisa': {
        'artist': 'Leonardo da Vinci',
        'year': 'ca. 1503-1519',
        'location': 'Louvre Museum, Paris',
        'technique': 'Öl auf Pappelholz',
        'fun_fact': 'Das Lächeln der Mona Lisa ist eines der berühmtesten Rätsel der Kunstgeschichte.'
    },
    'the starry night': {
        'artist': 'Vincent van Gogh', 
        'year': '1889',
        'location': 'Museum of Modern Art (MoMA), New York',
        'technique': 'Öl auf Leinwand',
        'fun_fact': 'Van Gogh malte dieses Meisterwerk während seines Aufenthalts in der Nervenheilanstalt von Saint-Rémy.'
    },
    'guernica': {
        'artist': 'Pablo Picasso',
        'year': '1937', 
        'location': 'Museo Reina Sofía, Madrid',
        'technique': 'Öl auf Leinwand',
        'fun_fact': 'Das Werk entstand als Reaktion auf die Bombardierung der baskischen Stadt Guernica im Spanischen Bürgerkrieg.'
    },    'girl with a pearl earring': {
        'artist': 'Johannes Vermeer',
        'year': 'ca. 1665',
        'location': 'Mauritshuis, Den Haag',
        'technique': 'Öl auf Leinwand',
        'fun_fact': 'Das Gemälde wird oft als "Mona Lisa des Nordens" bezeichnet.'
    },
    'the scream': {
        'artist': 'Edvard Munch',
        'year': '1893',
        'location': 'National Gallery, Oslo (eine von mehreren Versionen)',
        'technique': 'Öl, Tempera und Pastell auf Karton',
        'fun_fact': 'Das Werk entstand nach Munchs eigenem traumatischen Erlebnis eines "Schreis der Natur".'
    },
    'the persistence of memory': {
        'artist': 'Salvador Dalí',
        'year': '1931',
        'location': 'Museum of Modern Art (MoMA), New York',
        'technique': 'Öl auf Leinwand',
        'fun_fact': 'Die "schmelzenden Uhren" sind eines der bekanntesten Symbole des Surrealismus.'
    },
    'the last supper': {
        'artist': 'Leonardo da Vinci',
        'year': '1495-1498',
        'location': 'Santa Maria delle Grazie, Mailand',
        'technique': 'Fresko',
        'fun_fact': 'Das Werk zeigt den Moment, in dem Jesus seinen Jüngern ankündigt, dass einer von ihnen ihn verraten wird.'
    }
}

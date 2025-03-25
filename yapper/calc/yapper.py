import re
from collections import Counter

def preprocess_text(text):
    """Clean text by removing URLs, mentions, hashtags, and special characters."""
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"@\w+", "", text)     # Remove mentions
    text = re.sub(r"#\w+", "", text)     # Remove hashtags
    text = re.sub(r"[^a-zA-Z0-9\s.!?]", "", text)  # Remove special characters
    return text.strip()

def word_count(text):
    """Returns the number of words in a text."""
    return len(text.split())

def sentence_count(text):
    """Returns the number of sentences based on punctuation."""
    return len(re.findall(r"[.!?]", text))

def repetitiveness_score(text):
    """Calculates how often words are repeated in the text."""
    words = text.lower().split()
    word_counts = Counter(words)
    most_common = max(word_counts.values(), default=1)  # Avoid division by zero
    return most_common / len(words) if words else 0

def excessive_punctuation_score(text):
    """Counts occurrences of excessive punctuation (e.g., ..., !!!, ???)."""
    return len(re.findall(r"\.\.\.|!{2,}|\?{2,}", text))

def lexical_richness(text):
    """Measures the ratio of unique words to total words."""
    words = text.lower().split()
    unique_words = set(words)
    return len(unique_words) / len(words) if words else 0

def yapper_score(sentences):
    """Calculates the Yapper Score based on multiple factors."""
    # Check for empty sentences list
    if not sentences:
        return 0  # Return a zero score when no tweets are available
        
    total_words = sum(word_count(preprocess_text(sent)) for sent in sentences)
    total_sentences = sum(sentence_count(preprocess_text(sent)) for sent in sentences)
    avg_repetitiveness = sum(repetitiveness_score(preprocess_text(sent)) for sent in sentences) / len(sentences)
    total_punctuation = sum(excessive_punctuation_score(preprocess_text(sent)) for sent in sentences)
    avg_lexical_richness = sum(lexical_richness(preprocess_text(sent)) for sent in sentences) / len(sentences)

    # Normalize values (scaling)
    word_score = min(total_words / 300, 1)  # Assuming 300 words is very high
    sentence_score = min(total_sentences / 50, 1)  # Assuming 50 sentences is high
    repetition_score = avg_repetitiveness  # Already in [0,1] range
    punctuation_score = min(total_punctuation / 10, 1)  # Max excessive punctuations set to 10
    lexical_richness_score = avg_lexical_richness  # Already in [0,1] range

    # Weighted Yapper Score
    yapper_score = (
        0.4 * word_score +
        0.2 * sentence_score +
        0.15 * repetition_score +
        0.1 * punctuation_score +
        0.05 * lexical_richness_score
    )

    return round(yapper_score * 100, 2)  # Convert to percentage

def clean_tweets(tweet_list):
    """
    Cleans a list of tweets by removing the first 4 lines and the last 3 lines.
    Returns a list of cleaned tweet content.
    """
    def clean_single_tweet(tweet_text):
        lines = tweet_text.split("\n")

        # Remove first 4 lines and last 3 lines
        cleaned_lines = lines[4:-3] if len(lines) > 7 else []

        return "\n".join(cleaned_lines).strip()

    return [clean_single_tweet(tweet) for tweet in tweet_list]









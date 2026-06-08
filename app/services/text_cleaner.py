import pandas as pd
import re


_EMOJI = re.compile(
    "["
    "\U0001F600-\U0001F64F"  
    "\U0001F300-\U0001F5FF"  
    "\U0001F680-\U0001F6FF"  
    "\U0001F700-\U0001F77F"  
    "\U0001F780-\U0001F7FF"  
    "\U0001F800-\U0001F8FF"  
    "\U0001F900-\U0001F9FF"  
    "\U0001FA00-\U0001FA6F"  
    "\U0001FA70-\U0001FAFF"  
    "\U00002702-\U000027B0"  
    "\U000024C2-\U0001F251" 
    "]+",
    flags=re.UNICODE,
)

_EDGE_QUOTES = re.compile(r'^[\'"«»\u201c\u201d\u2018\u2019]+|[\'"«»\u201c\u201d\u2018\u2019]+$')
_VK_CLUB_TAG = re.compile(r'\[club\d+\|[^\]]+\]')
_VK_ID_TAG = re.compile(r'\[id\d+\|[^\]]+\]')
_BARE_ID = re.compile(r'\bid\d+\b')
_MENTION = re.compile(r'@\w+')
_HASHTAG = re.compile(r'#\S+')
_URL = re.compile(r'https?://\S+|www\.\S+|vk\.com/\S+')
_MEDIA_CAPTION = re.compile(r'(видео|фото)\s+(от\s+)?\S+', re.IGNORECASE)
_PHONE = re.compile(r'\+?\d[\d\s\-\(\)]{8,}\d')
_PHONE_LABEL = re.compile(r'тел\.?\s*:?\s*[\d\s\-]+')
_EMAIL = re.compile(r'\S+@\S+\.\S+')
_NON_TEXT = re.compile(r'[^\w\s\u0400-\u04FFа-яА-ЯёЁ.,!?\-:;№"\'()]')
_NEWLINES = re.compile(r'\n+')
_MULTI_SPACE = re.compile(r'\s+')
_SPACE_BEFORE_PUNCT = re.compile(r'\s+([.,!?\-:;])')
_REPEATED_PUNCT = re.compile(r'([!?.])(\1+)')
_REPEATED_DASH_COMMA = re.compile(r'([-,])(\1+)')
_LONE_DIGITS = re.compile(r'\b\d+\b')
_MULTI_DOTS = re.compile(r'\.{2,}')


def _strip_edge_quotes(text: str) -> str:
    return _EDGE_QUOTES.sub('', text)


def _remove_social_markup(text: str) -> str:
    text = _VK_CLUB_TAG.sub('', text)
    text = _VK_ID_TAG.sub('', text)
    text = _BARE_ID.sub('', text)
    text = _MENTION.sub('', text)
    text = _HASHTAG.sub('', text)
    return text


def _remove_urls(text: str) -> str:
    return _URL.sub('', text)


def _remove_media_captions(text: str) -> str:
    return _MEDIA_CAPTION.sub('', text)


def _remove_contacts(text: str) -> str:
    text = _PHONE.sub('', text)
    text = _PHONE_LABEL.sub('', text)
    text = _EMAIL.sub('', text)
    return text


def _remove_emojis(text: str) -> str:
    return _EMOJI.sub('', text)


def _remove_non_text_chars(text: str) -> str:
    return _NON_TEXT.sub(' ', text)


def _remove_lone_digits(text: str) -> str:
    return _LONE_DIGITS.sub('', text)


def _normalize_punctuation(text: str) -> str:
    text = _REPEATED_PUNCT.sub(r'\1', text)  # !!! → !
    text = _REPEATED_DASH_COMMA.sub(r'\1', text)  # ,,, → ,
    text = _MULTI_DOTS.sub('.', text)  # ... → .
    text = _SPACE_BEFORE_PUNCT.sub(r'\1', text)
    return text


def _normalize_whitespace(text: str) -> str:
    text = _NEWLINES.sub(' ', text)
    text = _MULTI_SPACE.sub(' ', text)
    return text.strip()


def clean_text(text: str | None) -> str:
    if pd.isna(text) or not isinstance(text, str):
        return ""

    text = _strip_edge_quotes(text)
    text = _remove_social_markup(text)
    text = _remove_urls(text)
    text = _remove_media_captions(text)
    text = _remove_contacts(text)
    text = _remove_emojis(text)
    text = _remove_non_text_chars(text)
    text = _remove_lone_digits(text)
    text = _normalize_punctuation(text)
    text = _normalize_whitespace(text)

    return text.lower()

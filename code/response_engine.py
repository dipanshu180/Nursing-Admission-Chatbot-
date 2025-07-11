# # import pandas as pd
# # import random
# # import ast
# # import re
# # from rapidfuzz import fuzz
# # from symspellpy.symspellpy import SymSpell, Verbosity
# # import os

# # # Load CSV
# # df = pd.read_csv("responses.csv")
# # df['answers'] = df['answers'].apply(ast.literal_eval)

# # # SymSpell init
# # sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
# # dictionary_path = os.path.join("symspell", "frequency_dictionary_en_1000.txt")
# # sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# # # Keyword map
# # keyword_map = {
# #     "fee": "fee", "fees": "fee", "kitna": "fee",
# #     "eligibility": "eligibility", "biology": "eligibility",
# #     "hostel": "hostel", "room": "hostel",
# #     "location": "location", "delhi": "location",
# #     "training": "training", "hospital": "training",
# #     "scholarship": "scholarship", "recognition": "recognition", "inc": "recognition",
# #     "seats": "seats", "vacancy": "seats",
# #     "program": "program", "course": "program"
# # }

# # stopwords = {"kya", "hai", "ka", "ki", "ke", "m", "me", "mein", "bta", "batao", "bade", "h", "sakte", "sakta", "sakti"}

# # def correct_spelling(text):
# #     corrected = []
# #     words = re.findall(r'\w+', text.lower())
# #     for word in words:
# #         if word in stopwords:
# #             continue
# #         suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
# #         if suggestions:
# #             corrected.append(suggestions[0].term)
# #         else:
# #             corrected.append(word)
# #     return corrected

# # def fuzzy_match(word):
# #     best_score = 0
# #     best_tag = None
# #     for kw in keyword_map:
# #         score = fuzz.partial_ratio(word, kw)
# #         if score > best_score and score >= 75:
# #             best_score = score
# #             best_tag = keyword_map[kw]
# #     return best_tag

# # def clean_and_extract_keywords(user_input):
# #     corrected_words = correct_spelling(user_input)
# #     matched_tags = []
# #     for word in corrected_words:
# #         tag = fuzzy_match(word)
# #         if tag:
# #             matched_tags.append(tag)
# #     return matched_tags

# # def get_response(user_input):
# #     matched_tags = clean_and_extract_keywords(user_input)
# #     for tag in matched_tags:
# #         row = df[df['question'] == tag]
# #         if not row.empty:
# #             return random.choice(row.iloc[0]['answers'])
# #     return "Maaf kijiye, mujhe is baare mein sahi information nahi mil paayi."
# # def extract_tag(user_input):
# #     matched_tags = clean_and_extract_keywords(user_input)
# #     return matched_tags[0] if matched_tags else None





# import pandas as pd
# import random
# import ast
# import re
# from rapidfuzz import fuzz
# from symspellpy.symspellpy import SymSpell, Verbosity
# import os

# df = pd.read_csv("responses.csv")
# df['answers'] = df['answers'].apply(ast.literal_eval)

# sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
# dictionary_path = os.path.join("symspell", "frequency_dictionary_en_1000.txt")
# sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# keyword_map = {
#     "fee": "fee", "fees": "fee", "kitna": "fee",
#     "eligibility": "eligibility", "biology": "eligibility",
#     "hostel": "hostel", "room": "hostel",
#     "location": "location", "delhi": "location",
#     "training": "training", "hospital": "training",
#     "scholarship": "scholarship", "recognition": "recognition", "inc": "recognition",
#     "seats": "seats", "vacancy": "seats",
#     "program": "program", "course": "program"
# }

# stopwords = {"kya", "hai", "ka", "ki", "ke", "mein", "batao", "bta", "to", "mujhe"}

# def correct_spelling(text):
#     corrected = []
#     words = re.findall(r'\w+', text.lower())
#     for word in words:
#         if word in stopwords:
#             continue
#         suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
#         if suggestions:
#             corrected.append(suggestions[0].term)
#         else:
#             corrected.append(word)
#     return corrected

# def fuzzy_match(word):
#     best_score = 0
#     best_tag = None
#     for kw in keyword_map:
#         score = fuzz.partial_ratio(word, kw)
#         if score > best_score and score >= 75:
#             best_score = score
#             best_tag = keyword_map[kw]
#     return best_tag

# def clean_and_extract_keywords(user_input):
#     corrected_words = correct_spelling(user_input)
#     matched_tags = []
#     for word in corrected_words:
#         tag = fuzzy_match(word)
#         if tag:
#             matched_tags.append(tag)
#     return matched_tags

# def get_response(user_input):
#     matched_tags = clean_and_extract_keywords(user_input)
#     for tag in matched_tags:
#         row = df[df['question'] == tag]
#         if not row.empty:
#             return random.choice(row.iloc[0]['answers'])
#     return "Maaf kijiye, mujhe is topic par sahi info nahi mili."

# def extract_tag(user_input):
#     matched_tags = clean_and_extract_keywords(user_input)
#     return matched_tags[0] if matched_tags else None



# response_engine.py (final version with spell correction, fuzzy match & multi-line response)
import pandas as pd
import random
import ast
import re
from rapidfuzz import fuzz
from symspellpy.symspellpy import SymSpell, Verbosity
import os

# Load the response CSV
df = pd.read_csv("responses.csv")
df['answers'] = df['answers'].apply(ast.literal_eval)

# Initialize SymSpell
dictionary_path = os.path.join("symspell", "frequency_dictionary_en_1000.txt")
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# Keyword map
keyword_map = {
    "fee": "fee", "fees": "fee", "kitna": "fee",
    "eligibility": "eligibility", "biology": "eligibility",
    "hostel": "hostel", "room": "hostel",
    "location": "location", "delhi": "location",
    "training": "training", "hospital": "training",
    "scholarship": "scholarship", "recognition": "recognition", "inc": "recognition",
    "seats": "seats", "vacancy": "seats",
    "program": "program", "course": "program"
}

stopwords = {"kya", "hai", "ka", "ki", "ke", "mein", "batao", "bta", "to", "mujhe"}

def correct_spelling(text):
    corrected = []
    words = re.findall(r'\w+', text.lower())
    for word in words:
        if word in stopwords:
            continue
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        if suggestions:
            corrected.append(suggestions[0].term)
        else:
            corrected.append(word)
    return corrected

def fuzzy_match(word):
    best_score = 0
    best_tag = None
    for kw in keyword_map:
        score = fuzz.partial_ratio(word, kw)
        if score > best_score and score >= 75:
            best_score = score
            best_tag = keyword_map[kw]
    return best_tag

def clean_and_extract_keywords(user_input):
    corrected_words = correct_spelling(user_input)
    matched_tags = []
    for word in corrected_words:
        tag = fuzzy_match(word)
        if tag:
            matched_tags.append(tag)
    return matched_tags

def get_response(user_input):
    matched_tags = clean_and_extract_keywords(user_input)
    for tag in matched_tags:
        row = df[df['question'] == tag]
        if not row.empty:
            raw = random.choice(row.iloc[0]['answers'])
            return raw.strip().split("\n") if "\n" in raw else [raw.strip()]
    return ["Maaf kijiye, mujhe is topic par sahi info nahi mili."]

def extract_tag(user_input):
    matched_tags = clean_and_extract_keywords(user_input)
    return matched_tags[0] if matched_tags else None
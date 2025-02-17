import os
import sys
import re
import csv
import time
import requests
import tarfile
from bs4 import BeautifulSoup
from io import BytesIO
from collections import Counter
from deep_translator import GoogleTranslator
DOWNLOAD_BASE = "https://downloads.wortschatz-leipzig.de/corpora/"
available_languages = {
    "Achinese": "https://wortschatz.uni-leipzig.de/en/download/Achinese",
    "Acoli": "https://wortschatz.uni-leipzig.de/en/download/Acoli",
    "Afar": "https://wortschatz.uni-leipzig.de/en/download/Afar",
    "Afrikaans": "https://wortschatz.uni-leipzig.de/en/download/Afrikaans",
    "Akan": "https://wortschatz.uni-leipzig.de/en/download/Akan",
    "Albanian": "https://wortschatz.uni-leipzig.de/en/download/Albanian",
    "Amharic": "https://wortschatz.uni-leipzig.de/en/download/Amharic",
    "Anaang": "https://wortschatz.uni-leipzig.de/en/download/Anaang",
    "Arabic": "https://wortschatz.uni-leipzig.de/en/download/Arabic",
    "Aragonese": "https://wortschatz.uni-leipzig.de/en/download/Aragonese",
    "Armenian": "https://wortschatz.uni-leipzig.de/en/download/Armenian",
    "Assamese": "https://wortschatz.uni-leipzig.de/en/download/Assamese",
    "Asturian": "https://wortschatz.uni-leipzig.de/en/download/Asturian",
    "Aymara": "https://wortschatz.uni-leipzig.de/en/download/Aymara",
    "Azerbaijani": "https://wortschatz.uni-leipzig.de/en/download/Azerbaijani",
    "Balinese": "https://wortschatz.uni-leipzig.de/en/download/Balinese",
    "Bambara": "https://wortschatz.uni-leipzig.de/en/download/Bambara",
    "Banjar": "https://wortschatz.uni-leipzig.de/en/download/Banjar",
    "Bashkir": "https://wortschatz.uni-leipzig.de/en/download/Bashkir",
    "Basque": "https://wortschatz.uni-leipzig.de/en/download/Basque",
    "Bavarian": "https://wortschatz.uni-leipzig.de/en/download/Bavarian",
    "Belarusian": "https://wortschatz.uni-leipzig.de/en/download/Belarusian",
    "Bemba (Zambia)": "https://wortschatz.uni-leipzig.de/en/download/Bemba%20(Zambia)",
    "Bengali": "https://wortschatz.uni-leipzig.de/en/download/Bengali",
    "Bishnupriya": "https://wortschatz.uni-leipzig.de/en/download/Bishnupriya",
    "Bosnian": "https://wortschatz.uni-leipzig.de/en/download/Bosnian",
    "Breton": "https://wortschatz.uni-leipzig.de/en/download/Breton",
    "Buginese": "https://wortschatz.uni-leipzig.de/en/download/Buginese",
    "Bulgarian": "https://wortschatz.uni-leipzig.de/en/download/Bulgarian",
    "Buriat": "https://wortschatz.uni-leipzig.de/en/download/Buriat",
    "Burmese": "https://wortschatz.uni-leipzig.de/en/download/Burmese",
    "Catalan": "https://wortschatz.uni-leipzig.de/en/download/Catalan",
    "Cebuano": "https://wortschatz.uni-leipzig.de/en/download/Cebuano",
    "Central Bikol": "https://wortschatz.uni-leipzig.de/en/download/Central%20Bikol",
    "Central Kurdish": "https://wortschatz.uni-leipzig.de/en/download/Central%20Kurdish",
    "Chechen": "https://wortschatz.uni-leipzig.de/en/download/Chechen",
    "Chinese": "https://wortschatz.uni-leipzig.de/en/download/Chinese",
    "Chuvash": "https://wortschatz.uni-leipzig.de/en/download/Chuvash",
    "Corsican": "https://wortschatz.uni-leipzig.de/en/download/Corsican",
    "Croatian": "https://wortschatz.uni-leipzig.de/en/download/Croatian",
    "Czech": "https://wortschatz.uni-leipzig.de/en/download/Czech",
    "Danish": "https://wortschatz.uni-leipzig.de/en/download/Danish",
    "Dari": "https://wortschatz.uni-leipzig.de/en/download/Dari",
    "Dhivehi": "https://wortschatz.uni-leipzig.de/en/download/Dhivehi",
    "Dimli": "https://wortschatz.uni-leipzig.de/en/download/Dimli",
    "Dutch": "https://wortschatz.uni-leipzig.de/en/download/Dutch",
    "Dyula": "https://wortschatz.uni-leipzig.de/en/download/Dyula",
    "Eastern Maninkakan": "https://wortschatz.uni-leipzig.de/en/download/Eastern%20Maninkakan",
    "Eastern Mari": "https://wortschatz.uni-leipzig.de/en/download/Eastern%20Mari",
    "Eastern Yiddish": "https://wortschatz.uni-leipzig.de/en/download/Eastern%20Yiddish",
    "Egyptian Arabic": "https://wortschatz.uni-leipzig.de/en/download/Egyptian%20Arabic",
    "Emiliano-Romagnolo": "https://wortschatz.uni-leipzig.de/en/download/Emiliano-Romagnolo",
    "English": "https://wortschatz.uni-leipzig.de/en/download/English",
    "Erzya": "https://wortschatz.uni-leipzig.de/en/download/Erzya",
    "Esperanto": "https://wortschatz.uni-leipzig.de/en/download/Esperanto",
    "Estonian": "https://wortschatz.uni-leipzig.de/en/download/Estonian",
    "Ewe": "https://wortschatz.uni-leipzig.de/en/download/Ewe",
    "Extremaduran": "https://wortschatz.uni-leipzig.de/en/download/Extremaduran",
    "Faroese": "https://wortschatz.uni-leipzig.de/en/download/Faroese",
    "Fiji Hindi": "https://wortschatz.uni-leipzig.de/en/download/Fiji%20Hindi",
    "Finnish": "https://wortschatz.uni-leipzig.de/en/download/Finnish",
    "Fon": "https://wortschatz.uni-leipzig.de/en/download/Fon",
    "French": "https://wortschatz.uni-leipzig.de/en/download/French",
    "Fulah": "https://wortschatz.uni-leipzig.de/en/download/Fulah",
    "Galician": "https://wortschatz.uni-leipzig.de/en/download/Galician",
    "Gan Chinese": "https://wortschatz.uni-leipzig.de/en/download/Gan%20Chinese",
    "Ganda": "https://wortschatz.uni-leipzig.de/en/download/Ganda",
    "Georgian": "https://wortschatz.uni-leipzig.de/en/download/Georgian",
    "German": "https://wortschatz.uni-leipzig.de/en/download/German",
    "Gilaki": "https://wortschatz.uni-leipzig.de/en/download/Gilaki",
    "Goan Konkani": "https://wortschatz.uni-leipzig.de/en/download/Goan%20Konkani",
    "Guarani": "https://wortschatz.uni-leipzig.de/en/download/Guarani",
    "Gujarati": "https://wortschatz.uni-leipzig.de/en/download/Gujarati",
    "Haitian": "https://wortschatz.uni-leipzig.de/en/download/Haitian",
    "Halh Mongolian": "https://wortschatz.uni-leipzig.de/en/download/Halh%20Mongolian",
    "Hausa": "https://wortschatz.uni-leipzig.de/en/download/Hausa",
    "Hebrew": "https://wortschatz.uni-leipzig.de/en/download/Hebrew",
    "Hiligaynon": "https://wortschatz.uni-leipzig.de/en/download/Hiligaynon",
    "Hindi": "https://wortschatz.uni-leipzig.de/en/download/Hindi",
    "Hungarian": "https://wortschatz.uni-leipzig.de/en/download/Hungarian",
    "Ibibio": "https://wortschatz.uni-leipzig.de/en/download/Ibibio",
    "Icelandic": "https://wortschatz.uni-leipzig.de/en/download/Icelandic",
    "Ido": "https://wortschatz.uni-leipzig.de/en/download/Ido",
    "Igbo": "https://wortschatz.uni-leipzig.de/en/download/Igbo",
    "Iloko": "https://wortschatz.uni-leipzig.de/en/download/Iloko",
    "Indonesian": "https://wortschatz.uni-leipzig.de/en/download/Indonesian",
    "Interlingua": "https://wortschatz.uni-leipzig.de/en/download/Interlingua",
    "Interlingue": "https://wortschatz.uni-leipzig.de/en/download/Interlingue",
    "Iranian Persian": "https://wortschatz.uni-leipzig.de/en/download/Iranian%20Persian",
    "Irish": "https://wortschatz.uni-leipzig.de/en/download/Irish",
    "Italian": "https://wortschatz.uni-leipzig.de/en/download/Italian",
    "Japanese": "https://wortschatz.uni-leipzig.de/en/download/Japanese",
    "Javanese": "https://wortschatz.uni-leipzig.de/en/download/Javanese",
    "Kabardian": "https://wortschatz.uni-leipzig.de/en/download/Kabardian",
    "Kabiyé": "https://wortschatz.uni-leipzig.de/en/download/Kabiy%C3%A9",
    "Kabuverdianu": "https://wortschatz.uni-leipzig.de/en/download/Kabuverdianu",
    "Kabyle": "https://wortschatz.uni-leipzig.de/en/download/Kabyle",
    "Kalaallisut": "https://wortschatz.uni-leipzig.de/en/download/Kalaallisut",
    "Kannada": "https://wortschatz.uni-leipzig.de/en/download/Kannada",
    "Karachay-Balkar": "https://wortschatz.uni-leipzig.de/en/download/Karachay-Balkar",
    "Kashmiri": "https://wortschatz.uni-leipzig.de/en/download/Kashmiri",
    "Kashubian": "https://wortschatz.uni-leipzig.de/en/download/Kashubian",
    "Kazakh": "https://wortschatz.uni-leipzig.de/en/download/Kazakh",
    "Khmer": "https://wortschatz.uni-leipzig.de/en/download/Khmer",
    "Kikuyu": "https://wortschatz.uni-leipzig.de/en/download/Kikuyu",
    "Kinyarwanda": "https://wortschatz.uni-leipzig.de/en/download/Kinyarwanda",
    "Kirghiz": "https://wortschatz.uni-leipzig.de/en/download/Kirghiz",
    "Kituba (Congo)": "https://wortschatz.uni-leipzig.de/en/download/Kituba%20(Congo)",
    "Komi": "https://wortschatz.uni-leipzig.de/en/download/Komi",
    "Komi-Permyak": "https://wortschatz.uni-leipzig.de/en/download/Komi-Permyak",
    "Kongo": "https://wortschatz.uni-leipzig.de/en/download/Kongo",
    "Konkani": "https://wortschatz.uni-leipzig.de/en/download/Konkani",
    "Koongo": "https://wortschatz.uni-leipzig.de/en/download/Koongo",
    "Korean": "https://wortschatz.uni-leipzig.de/en/download/Korean",
    "Kurdish": "https://wortschatz.uni-leipzig.de/en/download/Kurdish",
    "Kölsch": "https://wortschatz.uni-leipzig.de/en/download/K%C3%B6lsch",
    "Ladino": "https://wortschatz.uni-leipzig.de/en/download/Ladino",
    "Lao": "https://wortschatz.uni-leipzig.de/en/download/Lao",
    "Latin": "https://wortschatz.uni-leipzig.de/en/download/Latin",
    "Latvian": "https://wortschatz.uni-leipzig.de/en/download/Latvian",
    "Ligurian": "https://wortschatz.uni-leipzig.de/en/download/Ligurian",
    "Limburgan": "https://wortschatz.uni-leipzig.de/en/download/Limburgan",
    "Lingala": "https://wortschatz.uni-leipzig.de/en/download/Lingala",
    "Lithuanian": "https://wortschatz.uni-leipzig.de/en/download/Lithuanian",
    "Lombard": "https://wortschatz.uni-leipzig.de/en/download/Lombard",
    "Lomwe": "https://wortschatz.uni-leipzig.de/en/download/Lomwe",
    "Low German": "https://wortschatz.uni-leipzig.de/en/download/Low%20German",
    "Lower Sorbian": "https://wortschatz.uni-leipzig.de/en/download/Lower%20Sorbian",
    "Lugbara": "https://wortschatz.uni-leipzig.de/en/download/Lugbara",
    "Lumbu": "https://wortschatz.uni-leipzig.de/en/download/Lumbu",
    "Lushai": "https://wortschatz.uni-leipzig.de/en/download/Lushai",
    "Luxembourgish": "https://wortschatz.uni-leipzig.de/en/download/Luxembourgish",
    "Macedonian": "https://wortschatz.uni-leipzig.de/en/download/Macedonian",
    "Madurese": "https://wortschatz.uni-leipzig.de/en/download/Madurese",
    "Maithili": "https://wortschatz.uni-leipzig.de/en/download/Maithili",
    "Makonde": "https://wortschatz.uni-leipzig.de/en/download/Makonde",
    "Malagasy": "https://wortschatz.uni-leipzig.de/en/download/Malagasy",
    "Malay": "https://wortschatz.uni-leipzig.de/en/download/Malay",
    "Malayalam": "https://wortschatz.uni-leipzig.de/en/download/Malayalam",
    "Maltese": "https://wortschatz.uni-leipzig.de/en/download/Maltese",
    "Mandarin Chinese": "https://wortschatz.uni-leipzig.de/en/download/Mandarin%20Chinese",
    "Manx": "https://wortschatz.uni-leipzig.de/en/download/Manx",
    "Maori": "https://wortschatz.uni-leipzig.de/en/download/Maori",
    "Marathi": "https://wortschatz.uni-leipzig.de/en/download/Marathi",
    "Mazanderani": "https://wortschatz.uni-leipzig.de/en/download/Mazanderani",
    "Min Dong Chinese": "https://wortschatz.uni-leipzig.de/en/download/Min%20Dong%20Chinese",
    "Min Nan Chinese": "https://wortschatz.uni-leipzig.de/en/download/Min%20Nan%20Chinese",
    "Minangkabau": "https://wortschatz.uni-leipzig.de/en/download/Minangkabau",
    "Mingrelian": "https://wortschatz.uni-leipzig.de/en/download/Mingrelian",
    "Mirandese": "https://wortschatz.uni-leipzig.de/en/download/Mirandese",
    "Modern Greek": "https://wortschatz.uni-leipzig.de/en/download/Modern%20Greek",
    "Mongolian": "https://wortschatz.uni-leipzig.de/en/download/Mongolian",
    "Mossi": "https://wortschatz.uni-leipzig.de/en/download/Mossi",
    "Navajo": "https://wortschatz.uni-leipzig.de/en/download/Navajo",
    "Ndonga": "https://wortschatz.uni-leipzig.de/en/download/Ndonga",
    "Neapolitan": "https://wortschatz.uni-leipzig.de/en/download/Neapolitan",
    "Nepali": "https://wortschatz.uni-leipzig.de/en/download/Nepali",
    "Newari": "https://wortschatz.uni-leipzig.de/en/download/Newari",
    "Nigerian Pidgin": "https://wortschatz.uni-leipzig.de/en/download/Nigerian%20Pidgin",
    "North Azerbaijani": "https://wortschatz.uni-leipzig.de/en/download/North%20Azerbaijani",
    "Northern Frisian": "https://wortschatz.uni-leipzig.de/en/download/Northern%20Frisian",
    "Northern Sami": "https://wortschatz.uni-leipzig.de/en/download/Northern%20Sami",
    "Northern Uzbek": "https://wortschatz.uni-leipzig.de/en/download/Northern%20Uzbek",
    "Norwegian": "https://wortschatz.uni-leipzig.de/en/download/Norwegian",
    "Norwegian Bokmål": "https://wortschatz.uni-leipzig.de/en/download/Norwegian%20Bokm%C3%A5l",
    "Norwegian Nynorsk": "https://wortschatz.uni-leipzig.de/en/download/Norwegian%20Nynorsk",
    "Nyanja": "https://wortschatz.uni-leipzig.de/en/download/Nyanja",
    "Nyankole": "https://wortschatz.uni-leipzig.de/en/download/Nyankole",
    "Occitan (post 1500)": "https://wortschatz.uni-leipzig.de/en/download/Occitan%20(post%201500)",
    "Oriya": "https://wortschatz.uni-leipzig.de/en/download/Oriya",
    "Oromo": "https://wortschatz.uni-leipzig.de/en/download/Oromo",
    "Ossetian": "https://wortschatz.uni-leipzig.de/en/download/Ossetian",
    "Pampanga": "https://wortschatz.uni-leipzig.de/en/download/Pampanga",
    "Pangasinan": "https://wortschatz.uni-leipzig.de/en/download/Pangasinan",
    "Panjabi": "https://wortschatz.uni-leipzig.de/en/download/Panjabi",
    "Papiamento": "https://wortschatz.uni-leipzig.de/en/download/Papiamento",
    "Pedi": "https://wortschatz.uni-leipzig.de/en/download/Pedi",
    "Persian": "https://wortschatz.uni-leipzig.de/en/download/Persian",
    "Pfaelzisch": "https://wortschatz.uni-leipzig.de/en/download/Pfaelzisch",
    "Piemontese": "https://wortschatz.uni-leipzig.de/en/download/Piemontese",
    "Plateau Malagasy": "https://wortschatz.uni-leipzig.de/en/download/Plateau%20Malagasy",
    "Polish": "https://wortschatz.uni-leipzig.de/en/download/Polish",
    "Pontic": "https://wortschatz.uni-leipzig.de/en/download/Pontic",
    "Portuguese": "https://wortschatz.uni-leipzig.de/en/download/Portuguese",
    "Pulaar": "https://wortschatz.uni-leipzig.de/en/download/Pulaar",
    "Pushto": "https://wortschatz.uni-leipzig.de/en/download/Pushto",
    "Quechua": "https://wortschatz.uni-leipzig.de/en/download/Quechua",
    "Romanian": "https://wortschatz.uni-leipzig.de/en/download/Romanian",
    "Romansh": "https://wortschatz.uni-leipzig.de/en/download/Romansh",
    "Romany": "https://wortschatz.uni-leipzig.de/en/download/Romany",
    "Rundi": "https://wortschatz.uni-leipzig.de/en/download/Rundi",
    "Russian": "https://wortschatz.uni-leipzig.de/en/download/Russian",
    "Rusyn": "https://wortschatz.uni-leipzig.de/en/download/Rusyn",
    "S'gaw Karen": "https://wortschatz.uni-leipzig.de/en/download/S'gaw%20Karen",
    "Sami": "https://wortschatz.uni-leipzig.de/en/download/Sami",
    "Samogitian": "https://wortschatz.uni-leipzig.de/en/download/Samogitian",
    "Sanskrit": "https://wortschatz.uni-leipzig.de/en/download/Sanskrit",
    "Saraiki": "https://wortschatz.uni-leipzig.de/en/download/Saraiki",
    "Sardinian": "https://wortschatz.uni-leipzig.de/en/download/Sardinian",
    "Scots": "https://wortschatz.uni-leipzig.de/en/download/Scots",
    "Sena": "https://wortschatz.uni-leipzig.de/en/download/Sena",
    "Serbian": "https://wortschatz.uni-leipzig.de/en/download/Serbian",
    "Serbo-Croatian": "https://wortschatz.uni-leipzig.de/en/download/Serbo-Croatian",
    "Shona": "https://wortschatz.uni-leipzig.de/en/download/Shona",
    "Sicilian": "https://wortschatz.uni-leipzig.de/en/download/Sicilian",
    "Silesian": "https://wortschatz.uni-leipzig.de/en/download/Silesian",
    "Sindhi": "https://wortschatz.uni-leipzig.de/en/download/Sindhi",
    "Sinhala": "https://wortschatz.uni-leipzig.de/en/download/Sinhala",
    "Slovak": "https://wortschatz.uni-leipzig.de/en/download/Slovak",
    "Slovenian": "https://wortschatz.uni-leipzig.de/en/download/Slovenian",
    "Somali": "https://wortschatz.uni-leipzig.de/en/download/Somali",
    "Soninke": "https://wortschatz.uni-leipzig.de/en/download/Soninke",
    "South Ndebele": "https://wortschatz.uni-leipzig.de/en/download/South%20Ndebele",
    "Southern Sotho": "https://wortschatz.uni-leipzig.de/en/download/Southern%20Sotho",
    "Spanish": "https://wortschatz.uni-leipzig.de/en/download/Spanish",
    "Standard Estonian": "https://wortschatz.uni-leipzig.de/en/download/Standard%20Estonian",
    "Standard Latvian": "https://wortschatz.uni-leipzig.de/en/download/Standard%20Latvian",
    "Standard Malay": "https://wortschatz.uni-leipzig.de/en/download/Standard%20Malay",
    "Sukuma": "https://wortschatz.uni-leipzig.de/en/download/Sukuma",
    "Sundanese": "https://wortschatz.uni-leipzig.de/en/download/Sundanese",
    "Susu": "https://wortschatz.uni-leipzig.de/en/download/Susu",
    "Swahili": "https://wortschatz.uni-leipzig.de/en/download/Swahili",
    "Swahili (macrolanguage)": "https://wortschatz.uni-leipzig.de/en/download/Swahili%20(macrolanguage)",
    "Swati": "https://wortschatz.uni-leipzig.de/en/download/Swati",
    "Swedish": "https://wortschatz.uni-leipzig.de/en/download/Swedish",
    "Swiss German": "https://wortschatz.uni-leipzig.de/en/download/Swiss%20German",
    "Tagalog": "https://wortschatz.uni-leipzig.de/en/download/Tagalog",
    "Tajik": "https://wortschatz.uni-leipzig.de/en/download/Tajik",
    "Tamil": "https://wortschatz.uni-leipzig.de/en/download/Tamil",
    "Tatar": "https://wortschatz.uni-leipzig.de/en/download/Tatar",
    "Telugu": "https://wortschatz.uni-leipzig.de/en/download/Telugu",
    "Thai": "https://wortschatz.uni-leipzig.de/en/download/Thai",
    "Tibetan": "https://wortschatz.uni-leipzig.de/en/download/Tibetan",
    "Tigrinya": "https://wortschatz.uni-leipzig.de/en/download/Tigrinya",
    "Timne": "https://wortschatz.uni-leipzig.de/en/download/Timne",
    "Tiv": "https://wortschatz.uni-leipzig.de/en/download/Tiv",
    "Tosk Albanian": "https://wortschatz.uni-leipzig.de/en/download/Tosk%20Albanian",
    "Tsonga": "https://wortschatz.uni-leipzig.de/en/download/Tsonga",
    "Tswana": "https://wortschatz.uni-leipzig.de/en/download/Tswana",
    "Tulu": "https://wortschatz.uni-leipzig.de/en/download/Tulu",
    "Tumbuka": "https://wortschatz.uni-leipzig.de/en/download/Tumbuka",
    "Turkish": "https://wortschatz.uni-leipzig.de/en/download/Turkish",
    "Turkmen": "https://wortschatz.uni-leipzig.de/en/download/Turkmen",
    "Tuvinian": "https://wortschatz.uni-leipzig.de/en/download/Tuvinian",
    "Udmurt": "https://wortschatz.uni-leipzig.de/en/download/Udmurt",
    "Uighur": "https://wortschatz.uni-leipzig.de/en/download/Uighur",
    "Ukrainian": "https://wortschatz.uni-leipzig.de/en/download/Ukrainian",
    "Upper Sorbian": "https://wortschatz.uni-leipzig.de/en/download/Upper%20Sorbian",
    "Urdu": "https://wortschatz.uni-leipzig.de/en/download/Urdu",
    "Uzbek": "https://wortschatz.uni-leipzig.de/en/download/Uzbek",
    "Venda": "https://wortschatz.uni-leipzig.de/en/download/Venda",
    "Venetian": "https://wortschatz.uni-leipzig.de/en/download/Venetian",
    "Vietnamese": "https://wortschatz.uni-leipzig.de/en/download/Vietnamese",
    "Vlaams": "https://wortschatz.uni-leipzig.de/en/download/Vlaams",
    "Volapük": "https://wortschatz.uni-leipzig.de/en/download/Volap%C3%BCk",
    "Võro": "https://wortschatz.uni-leipzig.de/en/download/V%C3%B5ro",
    "Walloon": "https://wortschatz.uni-leipzig.de/en/download/Walloon",
    "Waray (Philippines)": "https://wortschatz.uni-leipzig.de/en/download/Waray%20(Philippines)",
    "Welsh": "https://wortschatz.uni-leipzig.de/en/download/Welsh",
    "Western Frisian": "https://wortschatz.uni-leipzig.de/en/download/Western%20Frisian",
    "Western Mari": "https://wortschatz.uni-leipzig.de/en/download/Western%20Mari",
    "Western Panjabi": "https://wortschatz.uni-leipzig.de/en/download/Western%20Panjabi",
    "Wolof": "https://wortschatz.uni-leipzig.de/en/download/Wolof",
    "Wu Chinese": "https://wortschatz.uni-leipzig.de/en/download/Wu%20Chinese",
    "Xhosa": "https://wortschatz.uni-leipzig.de/en/download/Xhosa",
    "Yakut": "https://wortschatz.uni-leipzig.de/en/download/Yakut",
    "Yiddish": "https://wortschatz.uni-leipzig.de/en/download/Yiddish",
    "Yoruba": "https://wortschatz.uni-leipzig.de/en/download/Yoruba",
    "Zeeuws": "https://wortschatz.uni-leipzig.de/en/download/Zeeuws",
    "Zhuang": "https://wortschatz.uni-leipzig.de/en/download/Zhuang",
    "Zulu": "https://wortschatz.uni-leipzig.de/en/download/Zulu"
}
def fetch_download_links(page_url):
    """
    Fetches the Leipzig download page and extracts file names from elements
    with a 'data-corpora-file' attribute ending in ".tar.gz".
    """
    print(f"Fetching download page: {page_url}")
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {page_url}")
        sys.exit(1)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for a in soup.find_all("a", class_="link_corpora_download"):
        file_name = a.get("data-corpora-file")
        if file_name and file_name.endswith(".tar.gz"):
            links.append(file_name)
    return links

def download_file(url, output_path):
    """
    Downloads the file from the given URL and saves it to output_path.
    """
    print(f"Downloading from: {url}")
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print("Failed to download file.")
        sys.exit(1)
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Downloaded file saved as: {output_path}")

def extract_tar_gz(archive_path, extract_to):
    """
    Extracts the tar.gz archive at 'archive_path' into directory 'extract_to'.
    """
    print(f"Extracting {archive_path} to {extract_to} ...")
    with tarfile.open(archive_path, "r:gz") as tar:
        tar.extractall(path=extract_to)
    print("Extraction complete.")

def process_folder(folder_path):
    """
    Recursively reads all .txt files in folder_path and returns their combined text.
    Also removes any file that ends with "sources.txt".
    """
    combined_text = ""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith("sources.txt"):
                try:
                    os.remove(os.path.join(root, file))
                except OSError:
                    pass #la propreté avant tout
                    
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        combined_text += f.read() + " "
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    if not combined_text:
        print("No .txt files found in the extracted directory.")
        sys.exit(1)
    return combined_text

def tokenize(text):
    tokens = re.findall(r'\w+', text.lower())
    return tokens

def calculate_frequencies(tokens):
    return Counter(tokens)

def export_csv(counter, top_n=1500, output_filename='output.csv'):
    """
    Exports the top words (excluding tokens consisting solely of digits) to a CSV file with columns:
    Rank, Word, Translation.
    Also prints a summary (rank, word, frequency) as each row is written.
    """
    filtered_items = [(word, freq) for word, freq in counter.most_common() if not re.fullmatch(r'\d+', word)]
    
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Rank", "Word", "Translation"])
        for rank, (word, freq) in enumerate(filtered_items[:top_n], start=1):
            try:
                translation = GoogleTranslator(source='auto', target='en').translate(word)
            except Exception as e:
                translation = ""
                print(f"Translation error for word '{word}': {e}")
            writer.writerow([rank, word, translation])
            print(f"{rank}. {word}: {freq}")
            time.sleep(0.2)
    print(f"CSV file saved as {output_filename}")

def main():
    print("Available languages:")
    for idx, lang in enumerate(available_languages.keys(), start=1):
        print(f"{idx}: {lang}")
    choice = input("Select a language by number: ").strip()
    try:
        choice = int(choice)
    except ValueError:
        print("Invalid selection. Exiting.")
        sys.exit(1)
    if choice < 1 or choice > len(available_languages):
        print("Choice out of range. Exiting.")
        sys.exit(1)
    lang = list(available_languages.keys())[choice - 1]
    download_page_url = available_languages[lang]
    print(f"Selected language: {lang}")
    print(f"Download page URL: {download_page_url}")
    
    file_names = fetch_download_links(download_page_url)
    if not file_names:
        print("No .tar.gz files found on the page.")
        sys.exit(1)
    
    print("Available .tar.gz files:")
    for idx, name in enumerate(file_names, start=1):
        print(f"{idx}: {name}")
    
    file_choices = input("Enter the number(s) of the file(s) you want to download (comma-separated): ").strip()
    try:
        selected_indices = [int(i.strip()) for i in file_choices.split(",")]
    except ValueError:
        print("Invalid selection. Exiting.")
        sys.exit(1)
    
    selected_files = []
    for i in selected_indices:
        if i < 1 or i > len(file_names):
            print(f"Choice {i} out of range. Exiting.")
            sys.exit(1)
        selected_files.append(file_names[i - 1])
    
    download_dir = os.path.join(os.getcwd(), f"{lang}_corpus")
    os.makedirs(download_dir, exist_ok=True)
    
    extract_dir = os.path.join(download_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)
    
    for selected_file in selected_files:
        archive_path = os.path.join(download_dir, selected_file)
        download_url = DOWNLOAD_BASE + selected_file
        print(f"\nProcessing file: {selected_file}")
        print(f"Download URL: {download_url}")
        
        if os.path.exists(archive_path):
            print(f"Archive {archive_path} already exists. Skipping download.")
        else:
            download_file(download_url, archive_path)
        
        extract_tar_gz(archive_path, extract_dir)
    
    combined_text = process_folder(extract_dir)
    tokens = tokenize(combined_text)
    freq_counter = calculate_frequencies(tokens)
    output_csv = os.path.join(download_dir, "output.csv")
    export_csv(freq_counter, top_n=2000, output_filename=output_csv)

if __name__ == "__main__":
    main()

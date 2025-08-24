#!/usr/bin/env python3
"""
🌍 SISTEMA DE TRADUCCIONES - Adventure Game v3.0
Sistema multilingüe para interface y narrativa
"""

from enum import Enum
from typing import Dict, Any
from ai_engine import AILanguage

class TranslationSystem:
    """Sistema de traducciones multilingüe"""
    
    def __init__(self):
        self.translations = {
            # INTERFACE GENERAL
            "game_title": {
                AILanguage.SPANISH: "Juego de Aventuras AI v3.0",
                AILanguage.ENGLISH: "AI Adventure Game v3.0",
                AILanguage.FRENCH: "Jeu d'Aventure IA v3.0",
                AILanguage.PORTUGUESE: "Jogo de Aventura IA v3.0",
                AILanguage.ITALIAN: "Gioco di Avventura IA v3.0",
                AILanguage.GERMAN: "KI-Abenteuerspiel v3.0"
            },
            
            # PERSONALIDADES DEL NARRADOR
            "personality_mysterious": {
                AILanguage.SPANISH: "Misterioso",
                AILanguage.ENGLISH: "Mysterious",
                AILanguage.FRENCH: "Mystérieux",
                AILanguage.PORTUGUESE: "Misterioso",
                AILanguage.ITALIAN: "Misterioso",
                AILanguage.GERMAN: "Geheimnisvoll"
            },
            
            "personality_friendly": {
                AILanguage.SPANISH: "Amigable",
                AILanguage.ENGLISH: "Friendly",
                AILanguage.FRENCH: "Amical",
                AILanguage.PORTUGUESE: "Amigável",
                AILanguage.ITALIAN: "Amichevole",
                AILanguage.GERMAN: "Freundlich"
            },
            
            "personality_dramatic": {
                AILanguage.SPANISH: "Dramático",
                AILanguage.ENGLISH: "Dramatic",
                AILanguage.FRENCH: "Dramatique",
                AILanguage.PORTUGUESE: "Dramático",
                AILanguage.ITALIAN: "Drammatico",
                AILanguage.GERMAN: "Dramatisch"
            },
            
            "personality_humorous": {
                AILanguage.SPANISH: "Humorístico",
                AILanguage.ENGLISH: "Humorous",
                AILanguage.FRENCH: "Humoristique",
                AILanguage.PORTUGUESE: "Humorístico",
                AILanguage.ITALIAN: "Umoristico",
                AILanguage.GERMAN: "Humorvoll"
            },
            
            "personality_scholarly": {
                AILanguage.SPANISH: "Erudito",
                AILanguage.ENGLISH: "Scholarly",
                AILanguage.FRENCH: "Érudit",
                AILanguage.PORTUGUESE: "Erudito",
                AILanguage.ITALIAN: "Erudito",
                AILanguage.GERMAN: "Gelehrt"
            },
            
            "personality_adventurous": {
                AILanguage.SPANISH: "Aventurero",
                AILanguage.ENGLISH: "Adventurous",
                AILanguage.FRENCH: "Aventureux",
                AILanguage.PORTUGUESE: "Aventureiro",
                AILanguage.ITALIAN: "Avventuroso",
                AILanguage.GERMAN: "Abenteuerlustig"
            },
            
            # COMANDOS BÁSICOS
            "command_help": {
                AILanguage.SPANISH: "ayuda",
                AILanguage.ENGLISH: "help",
                AILanguage.FRENCH: "aide",
                AILanguage.PORTUGUESE: "ajuda",
                AILanguage.ITALIAN: "aiuto",
                AILanguage.GERMAN: "hilfe"
            },
            
            "command_look": {
                AILanguage.SPANISH: "mirar",
                AILanguage.ENGLISH: "look",
                AILanguage.FRENCH: "regarder",
                AILanguage.PORTUGUESE: "olhar",
                AILanguage.ITALIAN: "guardare",
                AILanguage.GERMAN: "schauen"
            },
            
            "command_go": {
                AILanguage.SPANISH: "ir",
                AILanguage.ENGLISH: "go",
                AILanguage.FRENCH: "aller",
                AILanguage.PORTUGUESE: "ir",
                AILanguage.ITALIAN: "andare",
                AILanguage.GERMAN: "gehen"
            },
            
            "command_take": {
                AILanguage.SPANISH: "tomar",
                AILanguage.ENGLISH: "take",
                AILanguage.FRENCH: "prendre",
                AILanguage.PORTUGUESE: "pegar",
                AILanguage.ITALIAN: "prendere",
                AILanguage.GERMAN: "nehmen"
            },
            
            "command_inventory": {
                AILanguage.SPANISH: "inventario",
                AILanguage.ENGLISH: "inventory",
                AILanguage.FRENCH: "inventaire",
                AILanguage.PORTUGUESE: "inventário",
                AILanguage.ITALIAN: "inventario",
                AILanguage.GERMAN: "inventar"
            },
            
            # MENSAJES DE SISTEMA
            "welcome_message": {
                AILanguage.SPANISH: "¡Bienvenido al Juego de Aventuras AI v3.0! Un mundo de posibilidades infinitas te espera.",
                AILanguage.ENGLISH: "Welcome to AI Adventure Game v3.0! A world of infinite possibilities awaits you.",
                AILanguage.FRENCH: "Bienvenue au Jeu d'Aventure IA v3.0! Un monde de possibilités infinies vous attend.",
                AILanguage.PORTUGUESE: "Bem-vindo ao Jogo de Aventura IA v3.0! Um mundo de possibilidades infinitas te espera.",
                AILanguage.ITALIAN: "Benvenuto al Gioco di Avventura IA v3.0! Un mondo di possibilità infinite ti aspetta.",
                AILanguage.GERMAN: "Willkommen beim KI-Abenteuerspiel v3.0! Eine Welt unendlicher Möglichkeiten erwartet Sie."
            },
            
            "select_personality": {
                AILanguage.SPANISH: "Selecciona la personalidad del narrador:",
                AILanguage.ENGLISH: "Select the narrator's personality:",
                AILanguage.FRENCH: "Sélectionnez la personnalité du narrateur:",
                AILanguage.PORTUGUESE: "Selecione a personalidade do narrador:",
                AILanguage.ITALIAN: "Seleziona la personalità del narratore:",
                AILanguage.GERMAN: "Wählen Sie die Persönlichkeit des Erzählers:"
            },
            
            "select_language": {
                AILanguage.SPANISH: "Selecciona tu idioma:",
                AILanguage.ENGLISH: "Select your language:",
                AILanguage.FRENCH: "Sélectionnez votre langue:",
                AILanguage.PORTUGUESE: "Selecione seu idioma:",
                AILanguage.ITALIAN: "Seleziona la tua lingua:",
                AILanguage.GERMAN: "Wählen Sie Ihre Sprache:"
            },
            
            # NOMBRES DE IDIOMAS
            "language_spanish": {
                AILanguage.SPANISH: "Español",
                AILanguage.ENGLISH: "Spanish",
                AILanguage.FRENCH: "Espagnol",
                AILanguage.PORTUGUESE: "Espanhol",
                AILanguage.ITALIAN: "Spagnolo",
                AILanguage.GERMAN: "Spanisch"
            },
            
            "language_english": {
                AILanguage.SPANISH: "Inglés",
                AILanguage.ENGLISH: "English",
                AILanguage.FRENCH: "Anglais",
                AILanguage.PORTUGUESE: "Inglês",
                AILanguage.ITALIAN: "Inglese",
                AILanguage.GERMAN: "Englisch"
            },
            
            "language_french": {
                AILanguage.SPANISH: "Francés",
                AILanguage.ENGLISH: "French",
                AILanguage.FRENCH: "Français",
                AILanguage.PORTUGUESE: "Francês",
                AILanguage.ITALIAN: "Francese",
                AILanguage.GERMAN: "Französisch"
            },
            
            "language_portuguese": {
                AILanguage.SPANISH: "Portugués",
                AILanguage.ENGLISH: "Portuguese",
                AILanguage.FRENCH: "Portugais",
                AILanguage.PORTUGUESE: "Português",
                AILanguage.ITALIAN: "Portoghese",
                AILanguage.GERMAN: "Portugiesisch"
            },
            
            "language_italian": {
                AILanguage.SPANISH: "Italiano",
                AILanguage.ENGLISH: "Italian",
                AILanguage.FRENCH: "Italien",
                AILanguage.PORTUGUESE: "Italiano",
                AILanguage.ITALIAN: "Italiano",
                AILanguage.GERMAN: "Italienisch"
            },
            
            "language_german": {
                AILanguage.SPANISH: "Alemán",
                AILanguage.ENGLISH: "German",
                AILanguage.FRENCH: "Allemand",
                AILanguage.PORTUGUESE: "Alemão",
                AILanguage.ITALIAN: "Tedesco",
                AILanguage.GERMAN: "Deutsch"
            }
        }
    
    def get_text(self, key: str, language: AILanguage) -> str:
        """Obtener texto traducido"""
        if key in self.translations:
            if language in self.translations[key]:
                return self.translations[key][language]
            else:
                # Fallback a español si no existe la traducción
                return self.translations[key].get(AILanguage.SPANISH, f"[{key}]")
        return f"[{key}]"
    
    def get_personality_traits(self, language: AILanguage) -> Dict[str, str]:
        """Obtener traits de personalidad para prompts de IA"""
        traits = {
            "mysterious": {
                AILanguage.SPANISH: "misterioso, enigmático, habla con acertijos",
                AILanguage.ENGLISH: "mysterious, enigmatic, speaks in riddles",
                AILanguage.FRENCH: "mystérieux, énigmatique, parle par énigmes",
                AILanguage.PORTUGUESE: "misterioso, enigmático, fala por enigmas",
                AILanguage.ITALIAN: "misterioso, enigmatico, parla per enigmi",
                AILanguage.GERMAN: "geheimnisvoll, rätselhaft, spricht in Rätseln"
            },
            "friendly": {
                AILanguage.SPANISH: "cálido, útil, alentador",
                AILanguage.ENGLISH: "warm, helpful, encouraging",
                AILanguage.FRENCH: "chaleureux, utile, encourageant",
                AILanguage.PORTUGUESE: "caloroso, útil, encorajador",
                AILanguage.ITALIAN: "caloroso, utile, incoraggiante",
                AILanguage.GERMAN: "warm, hilfsbereit, ermutigend"
            },
            "dramatic": {
                AILanguage.SPANISH: "teatral, apasionado, emocionalmente intenso",
                AILanguage.ENGLISH: "theatrical, passionate, emotionally intense",
                AILanguage.FRENCH: "théâtral, passionné, émotionnellement intense",
                AILanguage.PORTUGUESE: "teatral, apaixonado, emocionalmente intenso",
                AILanguage.ITALIAN: "teatrale, appassionato, emotivamente intenso",
                AILanguage.GERMAN: "theatralisch, leidenschaftlich, emotional intensiv"
            },
            "humorous": {
                AILanguage.SPANISH: "ingenioso, juguetón, encuentra humor en las situaciones",
                AILanguage.ENGLISH: "witty, playful, finds humor in situations",
                AILanguage.FRENCH: "spirituel, enjoué, trouve l'humour dans les situations",
                AILanguage.PORTUGUESE: "espirituoso, brincalhão, encontra humor nas situações",
                AILanguage.ITALIAN: "spiritoso, giocoso, trova umorismo nelle situazioni",
                AILanguage.GERMAN: "witzig, verspielt, findet Humor in Situationen"
            },
            "scholarly": {
                AILanguage.SPANISH: "conocedor, preciso, educativo",
                AILanguage.ENGLISH: "knowledgeable, precise, educational",
                AILanguage.FRENCH: "savant, précis, éducatif",
                AILanguage.PORTUGUESE: "conhecedor, preciso, educativo",
                AILanguage.ITALIAN: "esperto, preciso, educativo",
                AILanguage.GERMAN: "kenntnisreich, präzise, lehrreich"
            },
            "adventurous": {
                AILanguage.SPANISH: "audaz, emocionante, orientado a la acción",
                AILanguage.ENGLISH: "bold, exciting, action-oriented",
                AILanguage.FRENCH: "audacieux, excitant, orienté action",
                AILanguage.PORTUGUESE: "corajoso, emocionante, orientado à ação",
                AILanguage.ITALIAN: "audace, emozionante, orientato all'azione",
                AILanguage.GERMAN: "kühn, aufregend, aktionsorientiert"
            }
        }
        
        return {k: v.get(language, v[AILanguage.SPANISH]) for k, v in traits.items()}
    
    def get_language_instructions(self, language: AILanguage) -> str:
        """Obtener instrucciones específicas de idioma para la IA"""
        instructions = {
            AILanguage.SPANISH: "Responde SIEMPRE en español. Usa un lenguaje rico y descriptivo apropiado para una aventura en español.",
            AILanguage.ENGLISH: "ALWAYS respond in English. Use rich, descriptive language appropriate for an English adventure.",
            AILanguage.FRENCH: "Réponds TOUJOURS en français. Utilise un langage riche et descriptif approprié pour une aventure en français.",
            AILanguage.PORTUGUESE: "Responda SEMPRE em português. Use linguagem rica e descritiva apropriada para uma aventura em português.",
            AILanguage.ITALIAN: "Rispondi SEMPRE in italiano. Usa un linguaggio ricco e descrittivo appropriato per un'avventura in italiano.",
            AILanguage.GERMAN: "Antworte IMMER auf Deutsch. Verwende eine reiche, beschreibende Sprache, die für ein deutsches Abenteuer geeignet ist."
        }
        
        return instructions.get(language, instructions[AILanguage.SPANISH])

# Instancia global del sistema de traducciones
translation_system = TranslationSystem()

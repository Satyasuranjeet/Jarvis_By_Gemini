import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import os
from datetime import datetime
import time

class VoiceEngine:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        
    def speak(self, text):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def listen(self):
        """Listen for audio input and convert to text"""
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                return text.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            print("Could not request results from speech recognition service")
            return ""

class GeminiAI:
    def __init__(self, api_key):
        # Initialize Gemini AI
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def process_command(self, command):
        """Process command using Gemini AI"""
        try:
            response = await self.model.generate_content_async(command)
            return response.text
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

class JarvisAssistant:
    def __init__(self, gemini_api_key):
        self.voice_engine = VoiceEngine()
        self.speech_recognizer = SpeechRecognizer()
        self.ai = GeminiAI(gemini_api_key)
        self.is_active = False
        self.is_running = True
    
    def activate(self):
        """Activate Jarvis after wake word detection"""
        self.is_active = True
        self.voice_engine.speak("Yes boss, I'm listening")
    
    def deactivate(self):
        """Deactivate Jarvis"""
        self.is_active = False
    
    async def process_user_input(self, user_input):
        """Process user input and generate response"""
        if "exit" in user_input or "bye" in user_input:
            self.voice_engine.speak("Goodbye")
            self.is_running = False
            return
        
        if self.is_active:
            response = await self.ai.process_command(user_input)
            self.voice_engine.speak(response)
            self.deactivate()
    
    async def run(self):
        """Main loop for running Jarvis"""
        print("Jarvis is starting up...")
        self.voice_engine.speak("Jarvis is ready")
        
        while self.is_running:
            text = self.speech_recognizer.listen()
            
            if text:
                print(f"Heard: {text}")
                
                if not self.is_active and "jarvis" in text:
                    self.activate()
                else:
                    await self.process_user_input(text)
            
            time.sleep(0.1)  # Small delay to prevent CPU overuse

def main():
    # Get Gemini API key from environment variable
    api_key = "AIzaSyB3yIN6bRebDCHi7zreWgS0S_nu3dQV-xU"
    if not api_key:
        raise ValueError("Please set the GEMINI_API_KEY environment variable")
    
    # Create and run Jarvis
    jarvis = JarvisAssistant(api_key)
    asyncio.run(jarvis.run())

if __name__ == "__main__":
    import asyncio
    main()
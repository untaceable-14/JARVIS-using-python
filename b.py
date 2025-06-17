import asyncio
import edge_tts
import pygame

async def speak(text):
    voice = "en-US-GuyNeural"  # You can change to any confirmed male voice
    tts = edge_tts.Communicate(text=text, voice=voice)
    await tts.save("output.mp3")

    # Initialize pygame mixer and play the sound
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    
    # Wait until the speech is done
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Run the async speak function
asyncio.run(speak("Hello, I am Guy. Your male assistant is now working!"))


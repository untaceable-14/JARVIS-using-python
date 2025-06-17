import asyncio
import edge_tts

async def speak(text):
    tts = edge_tts.Communicate(text=text, voice="en-US-GeorgeNeural")
    await tts.save("output.mp3")

    # Play the audio using default audio player
    import os
    os.system("start output.mp3")

# Run it
asyncio.run(speak("Hello, I am George. Nice to meet you!"))

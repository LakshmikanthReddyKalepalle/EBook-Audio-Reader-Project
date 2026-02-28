# 3 Ebook Audio Reader Projects 
from PyPDF2 import PdfReader
from gtts import gTTS
import os

def pdf_to_audio(pdf_path, audio_path="output.mp3"):
    try:
        # Check if PDF exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError("PDF file does not exist.")

        # Read PDF
        reader = PdfReader(pdf_path)
        text = ""

        # Extract text safely from each page
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                print(f"⚠️ Warning: No text found on page {page_num}")

        # Check if text was extracted
        if not text.strip():
            print("❌ No readable text found in the PDF.")
            return

        # gTTS has a character limit → split large text
        max_chars = 4000
        chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

        print("🔊 Converting text to speech...")

        with open(audio_path, "wb") as audio_file:
            for i, chunk in enumerate(chunks):
                tts = gTTS(text=chunk, lang='en')
                temp_file = f"temp_{i}.mp3"
                tts.save(temp_file)

                with open(temp_file, "rb") as f:
                    audio_file.write(f.read())

                os.remove(temp_file)

        print(f"✅ Audio file saved successfully as '{audio_path}'")

        # Auto-play on Windows
        if os.name == "nt":
            os.system(f'start {audio_path}')

    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")

# Run the program
if __name__ == "__main__":
    pdf_path = input("Enter the full path to your PDF file: ").strip()
    pdf_to_audio(pdf_path)
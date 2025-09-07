import io
import logging
import wave
from gtts import gTTS
import miniaudio

def synthesize_speech(text: str) -> io.BytesIO:
    """
    Generates Arabic speech using gTTS and converts it to WAV format.
    Returns WAV audio in a BytesIO stream.
    """
    try:
        # Generate MP3 bytes
        mp3_buf = io.BytesIO()
        tts = gTTS(text=text, lang='ar', slow=False)
        tts.write_to_fp(mp3_buf)
        mp3_data = mp3_buf.getvalue()

        # Decode MP3 to PCM using miniaudio
        decoded = miniaudio.decode(mp3_data)

        # Create WAV buffer with proper sample format handling
        wav_buf = io.BytesIO()
        with wave.open(wav_buf, 'wb') as wav_file:
            # Map miniaudio sample format to bytes per sample
            format_map = {
                miniaudio.SampleFormat.UNSIGNED8: 1,
                miniaudio.SampleFormat.SIGNED16: 2,
                miniaudio.SampleFormat.SIGNED24: 3,
                miniaudio.SampleFormat.SIGNED32: 4,
                miniaudio.SampleFormat.FLOAT32: 4,
            }
            
            wav_file.setnchannels(decoded.nchannels)
            wav_file.setsampwidth(format_map[decoded.sample_format])
            wav_file.setframerate(decoded.sample_rate)
            wav_file.writeframes(decoded.samples)

        wav_buf.seek(0)
        return wav_buf

    except Exception as e:
        logging.error("Error synthesizing speech or converting to WAV", exc_info=True)
        raise RuntimeError("Failed to synthesize speech or convert to WAV.") from e
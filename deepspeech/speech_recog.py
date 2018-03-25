import sys
import deepspeech.model as model
import scipy.io.wavfile as wav

# Gool 'ol copy paste from the config parameters in the source code. Only one we really need to change
# is the WAV_FILE to a buffer/in-memory file for a server-side use case
EXTENDED_MODEL = True
WAV_FILE = "audio/test.wav"
MODEL = "models/output_graph.pb"
N_FEATURES = 26 # Number of MFCC features to use
N_CONTEXT = 9 # Size of the context window used for producing timesteps in the input vector
ALPHABET = "models/alphabet.txt"
BEAM_WIDTH = 500 # Beam width used in the CTC decoder when building candidate transcriptions
LM = "models/lm.binary"
LM_WEIGHT = 1.75 # The alpha hyperparameter of the CTC decoder. Language Model weight
TRIE = "models/trie"
WORD_COUNT_WEIGHT = 1.00 # The beta hyperparameter of the CTC decoder. Word insertion weight (penalty)
VALID_WORD_COUNT_WEIGHT = 1.00 # Used to lessen the word insertion penalty when the word is part of vocab

ds = model.Model(MODEL, N_FEATURES, N_CONTEXT, ALPHABET, BEAM_WIDTH)
if EXTENDED_MODEL:
    ds.enableDecoderWithLM(ALPHABET, LM, TRIE, LM_WEIGHT, WORD_COUNT_WEIGHT, VALID_WORD_COUNT_WEIGHT)

def test_model():
    fs, audio = wav.read(WAV_FILE)
    processed_data = ds.stt(audio, fs)
    print processed_data

def mimic_buff_file():
    with open(WAV_FILE, mode='rb') as file:
        fs, audio = wav.read(WAV_FILE)
        processed_data = ds.stt(audio, fs)
        print processed_data

if __name__ == "__main__":
    mimic_buff_file()

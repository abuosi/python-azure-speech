import os
from audio_recognize import audio_recognize
from resume_transcription import resume_transcription

def process_audio_files(audios_folder, transcripts_folder):
    # Get the list of filenames in the audios folder
    filenames = [os.path.join(audios_folder, filename) for filename in os.listdir(audios_folder)]

    if not filenames:
        print("No audio files found in the audios folder.")
        return

    # Process each audio file
    for filename in filenames:
        print('\nProcessing the file -> ' + filename)

        # Transcribe the audio file
        transcription = audio_recognize(filename)

        # Resume the transcription
        resume = resume_transcription(transcription)

        result = f"Transcription:\n\n{transcription}\n\n\nResume:\n{resume}"

        # Write the transcript file
        output_filename = os.path.join(transcripts_folder, os.path.splitext(os.path.basename(filename))[0] + '.out')
        with open(output_filename, 'w+') as f:
            f.write(result)

        print('\n\tTranscript file created -> ' + output_filename)

try:
    # Path to the audios folder
    audios_folder = './audios'
    transcripts_folder = './transcripts_new'

    process_audio_files(audios_folder, transcripts_folder)

except Exception as err:
    print("\n\nEncountered exception: {}".format(err))

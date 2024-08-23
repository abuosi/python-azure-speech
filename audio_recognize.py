import os
import time

import azure.cognitiveservices.speech as speechsdk

def audio_recognize(audio_filename):
    # Configure speech service
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceConnection_LanguageIdMode, value='Continuous')

    # Configure language detection
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
        languages=["en-US", "pt-BR", "es-ES"])

    # Configure audio input
    audio_config = speechsdk.audio.AudioConfig(filename=audio_filename)

    # Create conversation transcriber
    conversation_transcriber = speechsdk.transcription.ConversationTranscriber(
        speech_config=speech_config, 
        auto_detect_source_language_config=auto_detect_source_language_config,
        audio_config=audio_config)

    # Initialize transcription and stop flag
    transcription = ""
    transcribing_stop = False

    # Callback function for when transcribing is stopped
    def stop_cb(evt: speechsdk.SessionEventArgs):
        nonlocal transcribing_stop
        transcribing_stop = True

    # Callback function for transcribing events
    def conversation_transcriber_transcribed_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        nonlocal transcription
        transcription_content = 'Speaker ID: {}\n'.format(evt.result.speaker_id)
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            transcription_content += '\t{}\n\n'.format(evt.result.text)
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            transcription_content += 'NOMATCH: Speech could not be transcribed: {}\n'.format(evt.result.no_match_details)
        transcription += transcription_content

    # Connect callbacks to transcriber events
    conversation_transcriber.transcribed.connect(conversation_transcriber_transcribed_cb)
    conversation_transcriber.session_stopped.connect(stop_cb)
    conversation_transcriber.canceled.connect(stop_cb)

    # Start transcribing
    conversation_transcriber.start_transcribing_async()

    # Wait for completion
    while not transcribing_stop:
        time.sleep(.5)

    # Stop transcribing
    conversation_transcriber.stop_transcribing_async()

    return transcription
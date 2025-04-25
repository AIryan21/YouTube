from elevenlabs import Voice, VoiceSettings, play,save
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="sk_019d0574ebbc9d04c812969c3c81f2d599236ba555f3a398", # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

                                               ##Alice##
audio1 = client.generate(
    text="ज़िंदगी का असली सौंदर्य उस पल में छिपा है.., जब हम दर्द को सहकर, मुस्कुराना सीख जाते हैं। क्योंकि अंधेरे के बाद ही उजाले की अहमियत समझ आती है।",
    voice=Voice(
        voice_id='Xb7hH8MSUJpSbSDYk0k2',
        settings=VoiceSettings(stability=0.65, similarity_boost=0.8, style=0.0, use_speaker_boost=True)
    ),
    model="eleven_multilingual_v2"
)

                                                ##Antony##                          
audio2 = client.generate(
    text="ज़िंदगी का असली सौंदर्य उस पल में छिपा है.., जब हम दर्द को सहकर, मुस्कुराना सीख जाते हैं। क्योंकि अंधेरे के बाद ही उजाले की अहमियत समझ आती है।",
    voice=Voice(
        voice_id='ErXwobaYiN019PkySvjV',
        settings=VoiceSettings(stability=0.45, similarity_boost=0.78, style=0.0, use_speaker_boost=True)
    ),
    model="eleven_multilingual_v2"
)

save(audio1,'vocal/female.mp3')
print('Female voice generated..!')
#save(audio2,'vocal/male.mp3')
#print('Male voice generated..!')

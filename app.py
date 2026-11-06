import gradio as gr
import edge_tts
import asyncio

# Dictionnaire étendu avec accents ethniques et régionaux
VOICES = {
    # --- FRANCOPHONES ---
    "🇫🇷 France - Homme (Henri)": "fr-FR-HenriNeural",
    "🇫🇷 France - Femme (Denise)": "fr-FR-DeniseNeural",
    "🇧🇪 Belgique - Homme (Gerard)": "fr-BE-GerardNeural",
    "🇧🇪 Belgique - Femme (Charline)": "fr-BE-CharlineNeural",
    "🇨🇦 Québec - Homme (Antoine)": "fr-CA-AntoineNeural",
    "🇨🇦 Québec - Femme (Sylvie)": "fr-CA-SylvieNeural",
    "🇨🇭 Suisse - Homme (Fabrice)": "fr-CH-FabriceNeural",
    
    # --- ETHNIES & DIVERSITÉ (Voix étrangères lisant du français) ---
    "🌍 Accent Africain (Swahili) - Homme": "sw-KE-RafikiNeural",
    "🌍 Accent Africain (Swahili) - Femme": "sw-KE-ZuriNeural",
    "🏜️ Accent Arabe (Égypte) - Homme": "ar-EG-ShakirNeural",
    "🏜️ Accent Arabe (Égypte) - Femme": "ar-EG-SalmaNeural",
    "🌶️ Accent Indien (Hindi) - Homme": "hi-IN-MadhurNeural",
    "🌶️ Accent Indien (Hindi) - Femme": "hi-IN-SwaraNeural",
    "🌸 Accent Asiatique (Japonais) - Homme": "ja-JP-KeitaNeural",
    "🌸 Accent Asiatique (Japonais) - Femme": "ja-JP-NanamiNeural",
    "🇺🇸 Accent Américain - Homme": "en-US-ChristopherNeural",
    "🇬🇧 Accent Britannique - Femme": "en-GB-SoniaNeural",
    "🇪🇸 Accent Espagnol - Homme": "es-ES-AlvaroNeural",
    "🇩🇪 Accent Allemand - Femme": "de-DE-AmalaNeural"
}

async def generate_accent(text, voice_choice, age_choice):
    voice_id = VOICES.get(voice_choice, "fr-FR-HenriNeural")
    
    # Ajustement de la fréquence (Pitch) pour simuler l'âge
    pitch_map = {
        "🧑 Adulte (Normal)": "+0Hz",
        "👶 Enfant (Voix aiguë)": "+50Hz",
        "👹 Voix très grave / Sombre": "-25Hz"
    }
    pitch_value = pitch_map.get(age_choice, "+0Hz")
    
    output_file = "audio_final.mp3"
    
    try:
        # On passe le paramètre pitch à la fonction Edge TTS
        communicate = edge_tts.Communicate(text, voice_id, pitch=pitch_value)
        await communicate.save(output_file)
        return output_file, f"Génération réussie : {voice_choice} en mode {age_choice}"
    except Exception as e:
        return None, f"Erreur : {str(e)}"

with gr.Blocks(title="Machine à Voix & Accents", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🌍 La Machine à Accents & Âges")
    gr.Markdown("Transforme n'importe quel accent en voix d'enfant ou de géant grâce au modificateur de hauteur !")
    
    text_input = gr.Textbox(label="Texte à prononcer", placeholder="Ex: Bonjour buana, c'est quand le poker ?")
    
    with gr.Row():
        voice_dropdown = gr.Dropdown(
            choices=list(VOICES.keys()), 
            label="1. Choix de l'accent / Ethnie", 
            value="🌍 Accent Africain (Swahili) - Homme"
        )
        
        age_dropdown = gr.Dropdown(
            choices=["🧑 Adulte (Normal)", "👶 Enfant (Voix aiguë)", "👹 Voix très grave / Sombre"],
            label="2. Âge du personnage",
            value="🧑 Adulte (Normal)"
        )
    
    btn = gr.Button("Générer l'audio", variant="primary")
    audio_out = gr.Audio(label="Résultat Audio", type="filepath")
    status = gr.Textbox(label="Statut", interactive=False)
    
    btn.click(generate_accent, [text_input, voice_dropdown, age_dropdown], [audio_out, status])

if __name__ == "__main__":
    app.launch(inbrowser=True)

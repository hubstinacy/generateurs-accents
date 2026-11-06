import gradio as gr
import edge_tts
import asyncio

# Liste étendue des voix
VOICES = {
    "🇫🇷 France - Homme (Henri)": "fr-FR-HenriNeural",
    "🇫🇷 France - Femme (Denise)": "fr-FR-DeniseNeural",
    "🇧🇪 Belgique - Homme (Gerard)": "fr-BE-GerardNeural",
    "🇨🇦 Québec - Homme (Antoine)": "fr-CA-AntoineNeural",
    "🇨🇭 Suisse - Homme (Fabrice)": "fr-CH-FabriceNeural",
    "🌍 Africain (Swahili) - Homme": "sw-KE-RafikiNeural",
    "🌍 Africain (Swahili) - Femme": "sw-KE-ZuriNeural",
    "🏜️ Arabe (Égypte) - Homme": "ar-EG-ShakirNeural",
    "🌶️ Indien (Hindi) - Homme": "hi-IN-MadhurNeural",
    "🌸 Asiatique (Japonais) - Femme": "ja-JP-NanamiNeural",
    "🇺🇸 Américain - Homme": "en-US-ChristopherNeural",
    "🇬🇧 Britannique - Femme": "en-GB-SoniaNeural",
    "🇪🇸 Espagnol - Homme": "es-ES-AlvaroNeural",
    "🇩🇪 Allemand - Femme": "de-DE-AmalaNeural"
}

async def generate_pro(text, voice_choice, preset, speed, pitch_custom):
    voice_id = VOICES.get(voice_choice, "fr-FR-HenriNeural")
    
    if preset == "👶 Enfant":
        pitch_str = "+50Hz"
    elif preset == "👹 Monstre / Grave":
        pitch_str = "-30Hz"
    elif preset == "🤖 Personnalisé (Utiliser les curseurs)":
        pitch_str = f"{pitch_custom:+}Hz"
    else:
        pitch_str = "+0Hz"
        
    speed_str = f"{speed:+}%"
    
    output_file = "audio_app.mp3"
    
    try:
        communicate = edge_tts.Communicate(text, voice_id, rate=speed_str, pitch=pitch_str)
        await communicate.save(output_file)
        return output_file, "✅ Audio généré avec succès !"
    except Exception as e:
        return None, f"❌ Erreur : {str(e)}"

with gr.Blocks(title="Studio Vocal", theme=gr.themes.Glass(primary_hue="indigo")) as app:
    gr.Markdown("<h1 style='text-align: center;'>🎙️ Studio Vocal Pro</h1>")
    
    with gr.Tabs():
        with gr.TabItem("📝 Création"):
            text_input = gr.Textbox(label="Ton texte", lines=3, placeholder="Tape ton texte ici...")
            voice_dropdown = gr.Dropdown(choices=list(VOICES.keys()), label="🗣️ Voix et Accent", value="🇫🇷 France - Homme (Henri)")
            
            with gr.Accordion("⚙️ Réglages Avancés (Âge, Vitesse, Effets)", open=False):
                preset_dropdown = gr.Dropdown(
                    choices=["🧑 Normal", "👶 Enfant", "👹 Monstre / Grave", "🤖 Personnalisé (Utiliser les curseurs)"],
                    label="Mode rapide", value="🧑 Normal"
                )
                speed_slider = gr.Slider(minimum=-50, maximum=100, step=5, value=0, label="Vitesse (%)")
                pitch_slider = gr.Slider(minimum=-100, maximum=100, step=5, value=0, label="Hauteur de voix personnalisée (Hz)")
            
            btn = gr.Button("Générer l'audio", variant="primary", size="lg")
            audio_out = gr.Audio(label="Résultat", type="filepath")
            status = gr.Textbox(show_label=False, interactive=False)
            
            btn.click(generate_pro, [text_input, voice_dropdown, preset_dropdown, speed_slider, pitch_slider], [audio_out, status])
            
        with gr.TabItem("ℹ️ Aide"):
            gr.Markdown("### Comment utiliser le mode personnalisé ?\nSélectionne **🤖 Personnalisé** dans le Mode rapide. Utilise ensuite le curseur de Vitesse pour faire parler le personnage plus ou moins vite, et le curseur de Hauteur (Pitch) pour rendre la voix très aiguë (positif) ou très grave (négatif).")

if __name__ == "__main__":
    app.launch()

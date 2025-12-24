# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime, timezone
import os
import base64
import requests
import pytz
import math

# -----------------------------------------------------------------------------
# 1. AYARLAR & OTURUM KONTROLÜ
# -----------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="NASA Exoplanet Analytics", initial_sidebar_state="collapsed")

if 'mission_start' not in st.session_state:
    st.session_state['mission_start'] = False

# -----------------------------------------------------------------------------
# 2. GİRİŞ EKRANI (SPLASH SCREEN)
# -----------------------------------------------------------------------------
if not st.session_state['mission_start']:
    st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .block-container { padding-top: 5rem; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color: white; font-size: 3em;'>NASA EXOPLANET ANALYTICS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; margin-bottom: 50px;'>Habitable Worlds Catalog // Deep Space Network</p>", unsafe_allow_html=True)

    if st.button("SİSTEMİ BAŞLAT 🚀", use_container_width=True):
        st.session_state['mission_start'] = True
        st.rerun()
    
    st.stop()

# =============================================================================
# SİSTEM BAŞLATILDIKTAN SONRAKİ KODLAR
# =============================================================================

# -----------------------------------------------------------------------------
# MÜZİK AYARLARI (LİNKİ BURAYA YAPIŞTIRIN)
# -----------------------------------------------------------------------------
# Buraya istediğiniz YouTube linkini tam olarak yapıştırın:
MÜZIK_LINKI = "https://www.youtube.com/watch?v=JuSsvM8B4Jc" 

# Linkten Video ID'sini otomatik ayıklayan fonksiyon
def get_video_id(url):
    if "youtu.be" in url:
        return url.split("/")[-1]
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    return "JuSsvM8B4Jc" # Hata olursa varsayılan (Interstellar)

video_id = get_video_id(MÜZIK_LINKI)

# --- AKILLI MÜZİK OYNATICI (VOLUME KONTROLLÜ) ---
# Dinamik Video ID entegrasyonu yapıldı.
components.html(
    f"""
    <!DOCTYPE html>
    <html>
      <body>
        <div id="player"></div>

        <script>
          var tag = document.createElement('script');
          tag.src = "https://www.youtube.com/iframe_api";
          var firstScriptTag = document.getElementsByTagName('script')[0];
          firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

          var player;
          function onYouTubeIframeAPIReady() {{
            player = new YT.Player('player', {{
              height: '0',
              width: '0',
              videoId: '{video_id}', 
              playerVars: {{
                'autoplay': 1,
                'controls': 0,
                'loop': 1,
                'playlist': '{video_id}'
              }},
              events: {{
                'onReady': onPlayerReady
              }}
            }});
          }}

          function onPlayerReady(event) {{
            event.target.setVolume(20); // Ses Seviyesi %20
            event.target.playVideo();
          }}
        </script>
      </body>
    </html>
    """,
    height=0,
)

# --- YARDIMCI FONKSİYONLAR ---
def get_base64_image(file_name):
    try:
        if os.path.exists(file_name):
            with open(file_name, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except: return None
    return None

bg_b64 = get_base64_image("stars.jpg")
bg_css = ""

if bg_b64:
    bg_css = f"""
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_b64}");
        background-size: cover; background-position: center;
        background-repeat: no-repeat; background-attachment: fixed;
    }}
    """
else:
    bg_css = ".stApp { background-color: #050505; }"

# --- CSS STİLLERİ ---
st.markdown(f"""
<style>
    {bg_css}
    .block-container {{
        padding-top: 1rem !important; 
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important; 
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }}
    div[data-testid="column"] {{ gap: 0.5rem; }}
    header, footer {{ display: none !important; }}

    /* INFO KUTUSU */
    .info-box {{
        background: rgba(0, 0, 0, 0.75); border-left: 4px solid #00d2ff;
        padding: 15px; border-radius: 6px; font-family: 'Courier New', monospace;
        color: white; margin-bottom: 15px; font-size: 1.0em; line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.8);
    }}
    
    .visitor-box {{
        background: rgba(0, 210, 255, 0.1); border-left: 4px solid #ffc107;
        padding: 12px; border-radius: 6px; font-family: 'Courier New', monospace;
        color: white; margin-top: 15px; font-size: 1.0em; line-height: 1.5;
    }}

    .planet-card {{
        background-color: rgba(15, 20, 26, 0.92);
        border: 1px solid #444; border-radius: 6px; overflow: hidden;
        margin-bottom: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.6); transition: transform 0.2s;
    }}
    .planet-card:hover {{ border-color: #00d2ff; transform: scale(1.01); }}
    
    .card-img-bg {{
        width: 100%; height: 95px; background-position: center; background-size: cover;
        position: relative; border-bottom: 1px solid #333;
    }}
    
    .type-badge {{
        position: absolute; top: 3px; right: 3px; 
        background: rgba(0,0,0,0.85); color: #ffc107; border: 1px solid #ffc107;
        padding: 2px 5px; font-size: 0.75em; font-weight: bold; border-radius: 3px;
    }}

    .card-body {{ padding: 6px 8px; }}
    .planet-name {{ color: #fff; font-size: 1.15em; font-weight: bold; margin-bottom: 0px; }}
    .planet-sub {{ color: #aaa; font-size: 0.85em; margin-bottom: 4px; text-transform: uppercase; font-weight: 600; }}
    .stat-row {{ display: flex; justify-content: space-between; font-size: 0.95em; margin-bottom: 1px; color: #ccc; border-bottom: 1px solid #222; }}
    .status-text {{ font-size: 0.9em; color: #ddd; margin-top: 4px; padding: 2px; background: rgba(255,255,255,0.05); border-radius: 3px; }}
    .progress-bg {{ width: 100%; height: 4px; background: #333; border-radius: 2px; margin-top:2px; }}
    .progress-fg {{ height: 100%; border-radius: 2px; }}
    
    /* Buton Stili */
    .stButton button {{
        background-color: #00d2ff; color: black; font-weight: bold; font-size: 1.2em;
        padding: 10px 20px; border-radius: 8px; border: none;
        transition: 0.3s;
    }}
    .stButton button:hover {{
        background-color: #ffffff; box-shadow: 0 0 15px #00d2ff;
    }}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. HESAPLAMALAR VE VERİLER
# -----------------------------------------------------------------------------

def get_earth_sun_data():
    now = datetime.now(timezone.utc)
    day_of_year = now.timetuple().tm_yday
    
    theta = 2 * math.pi * (day_of_year - 3) / 365.25
    distance_au = 1 - 0.0167 * math.cos(theta)
    distance_km = distance_au * 149597870.7
    
    light_seconds = distance_km / 299792.458
    light_time_min = int(light_seconds // 60)
    light_time_sec = int(light_seconds % 60)
    
    return {
        "dist_km": f"{distance_km:,.0f}".replace(",", "."),
        "dist_au": f"{distance_au:.4f}",
        "light_time": f"{light_time_min}dk {light_time_sec}sn",
        "avg_temp": "14.9°C"
    }

astro_data = get_earth_sun_data()

def get_live_user_data():
    default = {"city": "Bilinmiyor", "country": "Evren", "temp": "--", "time": "--:--"}
    try:
        loc = requests.get("http://ip-api.com/json/", timeout=2).json()
        if loc['status'] == 'success':
            weather = requests.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={loc['lat']}&longitude={loc['lon']}&current_weather=true", 
                timeout=2
            ).json()
            tz = pytz.timezone(loc['timezone'])
            local_time = datetime.now(tz).strftime("%H:%M")
            return {
                "city": loc['city'], "country": loc['country'],
                "temp": weather['current_weather']['temperature'], "time": local_time
            }
    except: return default
    return default

user_data = get_live_user_data()

data = {
    "Ad": ["Ross 128 b", "Teegarden b", "Kepler-438 b", "TRAPPIST-1 e", "Kepler-452 b", "Kepler-1649 c", "Kepler-22 b", "Proxima Cen b", "Kepler-442 b", "LHS 1140 b", "Kepler-62 f", "Kepler-186 f"],
    "Tip": ["Kayalık", "Kayalık", "Kayalık", "Kayalık", "Süper-Dünya", "Kayalık", "Okyanus/Gaz", "Kayalık", "Süper-Dünya", "Süper-Dünya", "Süper-Dünya", "Kayalık"],
    "TipKodu": ["M-TIPI", "M-TIPI", "M-TIPI", "M-TIPI", "G-TIPI", "M-TIPI", "K-TIPI", "M-TIPI", "K-TIPI", "M-TIPI", "K-TIPI", "M-TIPI"],
    "Yaricap": ["6.371 km", "6.498 km", "7.135 km", "5.861 km", "10.384 km", "6.753 km", "13.379 km", "6.371 km", "8.537 km", "11.021 km", "8.983 km", "7.454 km"],
    "Sicaklik": ["27°C", "3°C", "2°C", "-22°C", "-8°C", "-39°C", "5°C", "-55°C", "-40°C", "-47°C", "-65°C", "-85°C"],
    "DurumMetni": ["Yüksek Radyasyon", "Atmosfer Bilinmiyor", "Atmosfer Bilinmiyor", "Atmosfer Bilinmiyor", "Yüksek Basınç", "Atmosfer Bilinmiyor", "Yüksek Basınç", "Dondurucu Soğuk", "Atmosfer Bilinmiyor", "Yüksek Basınç", "Dondurucu Soğuk", "Dondurucu Soğuk"],
    "DurumIcon": ["\u2622", "\u2601", "\u2601", "\u2601", "\U0001F388", "\u2601", "\U0001F388", "\u2744", "\u2601", "\U0001F388", "\u2744", "\u2744"],
    "ESI": [95, 94, 92, 83, 78, 77, 74, 72, 71, 60, 59, 56],
    "Resim": ["ross128b.jpg", "teegarden.webp", "kepler438b.png", "TRAPPIST-1.png", "Kepler-452b_art.jpg", "Kepler-1649c.jpg", "Kepler22b.png", "Proxima-b-.jpg", "Kepler_442b.webp", "lhs1140b.jpg", "Kepler-62f.jpg", "Kepler-186f_Model.webp"]
}
df = pd.DataFrame(data)

# -----------------------------------------------------------------------------
# 4. YERLEŞİM VE GÖRSELLEŞTİRME
# -----------------------------------------------------------------------------
col_left, col_right = st.columns([3.2, 6.8])

with col_left:
    st.markdown("<h1 style='color:white; margin:0; font-size:1.8em; letter-spacing:1px;'>NASA EXOPLANET ARCHIVE</h1>", unsafe_allow_html=True)
    st.markdown("<div style='color:#aaa; font-size:0.95em; margin-bottom:10px; font-weight:bold;'>VISUALIZATION PROJECT // OPEN SOURCE</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div style="color:#00d2ff; font-weight:bold; font-size:1.1em; margin-bottom:5px;">CANLI TELEMETRİ: DÜNYA</div>
        <div>🛰️ <b>Güneş'e Mesafe:</b> {astro_data['dist_km']} km</div>
        <div>☀️ <b>Işık Ulaşma Süresi:</b> {astro_data['light_time']}</div>
        <div>🌍 <b>Küresel Ort. Sıcaklık:</b> {astro_data['avg_temp']}</div>
        <div>📡 <b>Yörünge Konumu:</b> {astro_data['dist_au']} AU</div>
        <div style="font-size:0.8em; color:#aaa; margin-top:5px;"><i>*Veriler anlık yörünge mekaniğine göre hesaplanmıştır.</i></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="visitor-box">
        <div style="color:#ffc107; font-weight:bold; font-size:1.0em; margin-bottom:5px;">YEREL İSTASYON (ZİYARETÇİ)</div>
        <div>📍 {user_data['city']}, {user_data['country']}</div>
        <div>🌡️ {user_data['temp']}°C | 🕒 {user_data['time']} (Yerel)</div>
    </div>
    """, unsafe_allow_html=True)

    components.html("""
    <div id="earth" style="height:620px; width:100%;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://unpkg.com/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>
        const container = document.getElementById('earth');
        const scene = new THREE.Scene();
        
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth/container.clientHeight, 0.1, 1000);
        camera.position.z = 2.9; 
        
        const renderer = new THREE.WebGLRenderer({antialias:true, alpha:true});
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        container.appendChild(renderer.domElement);
        
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableZoom = false; controls.enableRotate = true; controls.enablePan = false;
        controls.autoRotate = false; 
        
        const loader = new THREE.TextureLoader();
        const group = new THREE.Group(); 
        group.rotation.z = 23.4 * Math.PI / 180; 
        scene.add(group);

        const earthGeometry = new THREE.SphereGeometry(1, 64, 64);
        const earthMaterial = new THREE.MeshPhongMaterial({
            map: loader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_atmos_2048.jpg'),
            specularMap: loader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_specular_2048.jpg'),
            specular: new THREE.Color(0x333333),
            shininess: 5,
            bumpMap: loader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_normal_2048.jpg'),
            bumpScale: 0.005
        });
        const earth = new THREE.Mesh(earthGeometry, earthMaterial);
        group.add(earth);
        
        const atmosphereMaterial = new THREE.MeshPhongMaterial({
            color: 0x00aaff, transparent: true, opacity: 0.15,
            side: THREE.BackSide, blending: THREE.AdditiveBlending, shininess: 0
        });
        const atmosphere = new THREE.Mesh(new THREE.SphereGeometry(1.025, 64, 64), atmosphereMaterial);
        group.add(atmosphere);

        const cloudGeometry = new THREE.SphereGeometry(1.015, 64, 64);
        const cloudMaterial = new THREE.MeshPhongMaterial({
            map: loader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_clouds_1024.png'),
            transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, side: THREE.DoubleSide
        });
        const clouds = new THREE.Mesh(cloudGeometry, cloudMaterial);
        group.add(clouds);
        
        const now = new Date();
        const start = new Date(now.getFullYear(), 0, 0);
        const diff = now - start;
        const oneDay = 1000 * 60 * 60 * 24;
        const dayOfYear = Math.floor(diff / oneDay);

        const declinationAngleRad = (Math.PI / 180) * 23.45 * Math.sin((Math.PI / 180) * (360 / 365) * (dayOfYear - 81));
        const sunY = Math.tan(declinationAngleRad) * 50;

        const sunLight = new THREE.DirectionalLight(0xffffff, 1.8);
        sunLight.position.set(50, sunY, 20);
        scene.add(sunLight);
        
        const ambientLight = new THREE.AmbientLight(0x404040);
        scene.add(ambientLight);

        function animate() {
            requestAnimationFrame(animate);
            earth.rotation.y += 0.0002;
            clouds.rotation.y += 0.0003;
            controls.update();
            renderer.render(scene, camera);
        }
        animate();
    </script>
    """, height=620)

with col_right:
    grid_cols = st.columns(3)
    for i, row in df.iterrows():
        img_b64 = get_base64_image(row['Resim'])
        bg = f"url('data:image/jpeg;base64,{img_b64}')" if img_b64 else "#111"
        esi = row['ESI']
        if esi >= 90: color = "#00ff00"
        elif esi >= 75: color = "#ffc107"
        else: color = "#ff4500"
        
        html_card = f"""<div class="planet-card"><div class="card-img-bg" style="background-image:{bg};"><div class="type-badge" style="border-color:{color}; color:{color};">{row['TipKodu']}</div></div><div class="card-body"><div class="planet-name">{row['Ad']}</div><div class="planet-sub">{row['Tip']}</div><div class="stat-row"><span>Yarıçap</span><span class="stat-val">{row['Yaricap']}</span></div><div class="stat-row"><span>Sıcaklık</span><span class="stat-val">{row['Sicaklik']}</span></div><div class="status-text">{row['DurumIcon']} {row['DurumMetni']}</div><div class="progress-container"><div style="display:flex; justify-content:space-between; font-size:0.9em; color:#ccc;"><span>Benzerlik (ESI)</span><span style="color:{color}; font-weight:bold;">%{esi}</span></div><div class="progress-bg"><div class="progress-fg" style="width:{esi}%; background:{color}; box-shadow: 0 0 5px {color};"></div></div></div></div></div>"""
        with grid_cols[i % 3]:
            st.markdown(html_card, unsafe_allow_html=True)
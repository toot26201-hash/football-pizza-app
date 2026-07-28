import streamlit as st
from urllib.request import urlopen
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
from mplsoccer import Radar, Pitch
import io

# إعداد صفحة ستريملايت لتكون بعرض واسع
st.set_page_config(page_title="Football Player Analysis Dashboard", layout="wide")

st.title("⚽ Football Player Performance & Heatmap Dashboard")
st.write("Customize player stats, update the player name, upload a new image from the sidebar, and analyze the charts below!")

# ==========================================
# 1. Sidebar (Player Info, Image Upload & Stats)
# ==========================================
st.sidebar.header("👤 Player Details")
player_name = st.sidebar.text_input("Player Name", "Frenkie de Jong")

st.sidebar.header("🖼️ Change Player Image")
uploaded_file = st.sidebar.file_uploader("Choose player image (PNG or JPG)", type=["png", "jpg", "jpeg"])

st.sidebar.header("🔧 Edit Radar Statistics")
params = [
    "Goals", "npxG", "xA", "Decision Making", 
    "Crosses", "Corner Quality", "Prog Passes", 
    "Prog Carries", "Tackles", "Recoveries"
]

low = [0] * len(params)
high = [99] * len(params)

player_values = []
for param in params:
    val = st.sidebar.slider(f"{param}", 0, 99, 50)
    player_values.append(val)

# ==========================================
# 2. Image Management
# ==========================================
if uploaded_file is not None:
    player_image = Image.open(uploaded_file)
else:
    @st.cache_resource
    def load_default_image():
        URL = "https://raw.githubusercontent.com/andrewRowlinson/mplsoccer-assets/main/fdj_cropped.png"
        return Image.open(urlopen(URL))
    player_image = load_default_image()

# ==========================================
# 3. Radar Chart Setup & Rendering
# ==========================================
radar = Radar(
    params, 
    low, 
    high,
    round_int=[False] * len(params),
    num_rings=4, 
    ring_width=1
)

fig_radar, ax_radar = radar.setup_axis(figsize=(7, 7))
fig_radar.set_facecolor("#121212")
ax_radar.set_facecolor("#121212")

radar.draw_circles(ax=ax_radar, facecolor='#1e1e1e', edgecolor='#ffd700', lw=0.5)
radar.draw_radar(
    player_values, 
    ax=ax_radar, 
    kwargs_radar={'facecolor': '#1f77b4', 'alpha': 0.6, 'edgecolor': '#ff4d4d', 'lw': 2.5},
    kwargs_rings={'facecolor': '#222222'}
)
radar.draw_range_labels(ax=ax_radar, fontsize=9, color='#ffd700')
radar.draw_param_labels(ax=ax_radar, fontsize=11, color='#ffd700', fontweight='bold')
plt.title(f"Player Performance: {player_name}", fontsize=14, weight='bold', color='#ffd700', pad=15)

# ==========================================
# 4. Match Heatmap Setup & Rendering
# ==========================================
np.random.seed(42)
x_coords = np.random.uniform(0, 120, 300)
y_coords = np.random.uniform(0, 80, 300)

pitch = Pitch(pitch_type='statsbomb', pitch_color='#aabb97', line_color='white', line_zorder=2)
fig_heat, ax_heat = pitch.draw(figsize=(7, 5))
fig_heat.set_facecolor("#121212")

bin_statistic = pitch.bin_statistic(x_coords, y_coords, statistic='count', bins=(25, 25))
bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], sigma=1)

cmap_heat = LinearSegmentedColormap.from_list("CustomHeatmap", ["#aabb97", "#ffff00", "#ffaa00", "#ff0000"], N=256)
pcm = pitch.heatmap(bin_statistic, ax=ax_heat, cmap=cmap_heat, edgecolors=None, shading='gouraud', alpha=0.8)

ax_heat.set_title(f"Match Heatmap - {player_name}", fontsize=14, weight='bold', color='#ffd700', pad=10)

# ==========================================
# 5. UI Layout & Download Buttons
# ==========================================
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Performance Radar")
    st.pyplot(fig_radar)
    
    radar_buf = io.BytesIO()
    fig_radar.savefig(radar_buf, format="png", dpi=300, facecolor=fig_radar.get_facecolor(), edgecolor='none')
    radar_buf.seek(0)
    st.download_button(
        label="📥 Download Radar Chart", 
        data=radar_buf, 
        file_name=f"{player_name}_radar.png", 
        mime="image/png"
    )

with col2:
    st.subheader("🔥 Match Heatmap")
    st.pyplot(fig_heat)
    
    heat_buf = io.BytesIO()
    fig_heat.savefig(heat_buf, format="png", dpi=300, facecolor=fig_heat.get_facecolor(), edgecolor='none')
    heat_buf.seek(0)
    st.download_button(
        label="📥 Download Heatmap", 
        data=heat_buf, 
        file_name=f"{player_name}_heatmap.png", 
        mime="image/png"
    )

# Sidebar Image Preview & Download
st.markdown("---")
st.sidebar.subheader("Player Image Preview")
st.sidebar.image(player_image, use_container_width=True)

img_buf = io.BytesIO()
player_image.save(img_buf, format="PNG")
img_buf.seek(0)
st.sidebar.download_button(
    label="📥 Download Player Image",
    data=img_buf,
    file_name=f"{player_name}_image.png",
    mime="image/png"
)

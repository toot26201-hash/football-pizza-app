import streamlit as st
from urllib.request import urlopen
from PIL import Image
import matplotlib.pyplot as plt
from mplsoccer import Radar
import io
import os

# إعداد صفحة ستريملايت لتكون بعرض واسع
st.set_page_config(page_title="TootScouting Dashboard", layout="wide")

st.title("⚽ TootScouting - Player Performance & Metrics Dashboard")
st.write("Manage player data, radar charts, match heatmaps, and standalone individual metrics from the tabs below!")

# ==========================================
# 1. القائمة الجانبية الموحدة (البيانات والصور)
# ==========================================
st.sidebar.header("👤 Player Details")
player_name = st.sidebar.text_input("Player Name", "Frenkie de Jong")

st.sidebar.header("🖼️ Player Image")
uploaded_player_img = st.sidebar.file_uploader("Choose player image (PNG/JPG)", type=["png", "jpg", "jpeg"], key="player")

st.sidebar.header("🔥 Match Heatmap Image")
uploaded_heatmap_img = st.sidebar.file_uploader("Choose heatmap image (PNG/JPG)", type=["png", "jpg", "jpeg"], key="heatmap")

# ==========================================
# 2. إدارة الصور (اللاعب + اللوجو)
# ==========================================
if uploaded_player_img is not None:
    player_image = Image.open(uploaded_player_img)
else:
    @st.cache_resource
    def load_default_player():
        URL = "https://raw.githubusercontent.com/andrewRowlinson/mplsoccer-assets/main/fdj_cropped.png"
        return Image.open(urlopen(URL))
    player_image = load_default_player()

# تحميل اللوجو الخاص بالهوية (تأكد أن اسم الملف logo.png في نفس المجلد)
@st.cache_resource
def load_logo():
    if os.path.exists("logo.png"):
        return Image.open("logo.png")
    return None

logo_image = load_logo()

# ==========================================
# 3. تقسيم الواجهة إلى تبويبات (Tabs)
# ==========================================
tab1, tab2 = st.tabs(["📊 Radar & Heatmap", "🎯 Standalone Individual Metrics"])

# --- التبويب الأول: الرادار والخريطة الحرارية ---
with tab1:
    st.header(f"Performance Analysis for {player_name}")
    
    radar_params = [
        "Goals", "npxG", "xA", "Decision Making", 
        "Crosses", "Corner Quality", "Prog Passes", 
        "Prog Carries", "Tackles", "Recoveries"
    ]
    
    st.subheader("Configure Radar Statistics (Sidebar Sliders)")
    player_values = []
    
    cols = st.columns(2)
    for i, param in enumerate(radar_params):
        with cols[i % 2]:
            val = st.slider(f"Radar: {param}", 0, 99, 50, key=f"radar_{param}")
            player_values.append(val)

    # رسم الرادار
    radar = Radar(
        radar_params, 
        [0] * len(radar_params), 
        [99] * len(radar_params),
        round_int=[False] * len(radar_params),
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

    # إضافة اللوجو بشكل صغير أسفل الرادار إذا كان موجوداً
    if logo_image is not None:
        ax_logo = fig_radar.add_axes([0.40, 0.02, 0.20, 0.08]) # [left, bottom, width, height]
        ax_logo.imshow(logo_image)
        ax_logo.axis('off')

    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("📊 Performance Radar")
        st.pyplot(fig_radar)
        
        radar_buf = io.BytesIO()
        fig_radar.savefig(radar_buf, format="png", dpi=300, facecolor=fig_radar.get_facecolor(), edgecolor='none')
        radar_buf.seek(0)
        st.download_button("📥 Download Radar Chart", data=radar_buf, file_name=f"{player_name}_radar.png", mime="image/png")

    with c2:
        st.subheader("🔥 Match Heatmap")
        if uploaded_heatmap_img is not None:
            heatmap_image = Image.open(uploaded_heatmap_img)
            st.image(heatmap_image, use_container_width=True)
            
            heat_buf = io.BytesIO()
            heatmap_image.save(heat_buf, format="PNG")
            heat_buf.seek(0)
            st.download_button("📥 Download Heatmap Image", data=heat_buf, file_name=f"{player_name}_heatmap.png", mime="image/png")
        else:
            st.info("💡 Please upload your match heatmap image from the sidebar to display it here.")

# --- التبويب الثاني: مقياس الفرديات المنفصل تماماً ---
with tab2:
    st.header(f"🎯 Standalone Individual Metrics Assessment: {player_name}")
    st.write("This section evaluates standalone player metrics (Technical, Physical, and Tactical) independent of the charts.")

    ind_metrics = {
        "Key Passes": 75,
        "Successful Dribbles %": 65,
        "Touches in Penalty Area": 40,
        "Counter-Pressing Recoveries": 80,
        "Aerial Duels Won %": 55,
        "Duels Success Rate %": 70,
        "High-Intensity Sprints": 85,
        "Ball Retention %": 90
    }

    ind_values = {}
    col_a, col_b = st.columns(2)
    
    i = 0
    for metric, default_val in ind_metrics.items():
        target_col = col_a if i % 2 == 0 else col_b
        with target_col:
            ind_values[metric] = st.slider(f"Metric: {metric}", 0, 100, default_val, key=f"ind_{metric}")
        i += 1

    st.markdown("---")
    st.subheader("📋 Individual Metrics Summary Report")
    
    import pandas as pd
    df_metrics = pd.DataFrame(list(ind_values.items()), columns=["Individual Metric", "Score / Rating"])
    st.dataframe(df_metrics, use_container_width=True)

    csv_data = df_metrics.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Individual Metrics Report (CSV)",
        data=csv_data,
        file_name=f"{player_name}_individual_metrics.csv",
        mime="text/csv"
    )

# معاينة صورة اللاعب واللوجو في القائمة الجانبية
st.markdown("---")
st.sidebar.subheader("Player Image Preview")
st.sidebar.image(player_image, use_container_width=True)

if logo_image is not None:
    st.sidebar.subheader("Brand Logo")
    st.sidebar.image(logo_image, width=100)

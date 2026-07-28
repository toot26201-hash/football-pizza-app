import streamlit as st
from urllib.request import urlopen
from PIL import Image
import matplotlib.pyplot as plt
from mplsoccer import Radar
import io

# إعداد صفحة ستريملايت لتكون بعرض واسع
st.set_page_config(page_title="Football Player Radar Chart", layout="wide")

st.title("⚽ تطبيق تحليل أداء اللاعبين")
st.write("قم بتعديل إحصائيات اللاعب أو ارفع صورة جديدة من القائمة الجانبية، ثم حمل النتائج بسهولة!")

# ==========================================
# 1. القائمة الجانبية (رفع الصورة + القيم)
# ==========================================
st.sidebar.header("🖼️ تغيير صورة اللاعب")
uploaded_file = st.sidebar.file_uploader("اختر صورة اللاعب (PNG أو JPG)", type=["png", "jpg", "jpeg"])

st.sidebar.header("🔧 تعديل إحصائيات اللاعب")
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
# 2. إدارة الصورة
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
# 3. إعداد ورسم الـ Radar
# ==========================================
radar = Radar(
    params, 
    low, 
    high,
    round_int=[False] * len(params),
    num_rings=4, 
    ring_width=1
)

fig, ax = radar.setup_axis(figsize=(8, 8))

# تنسيق الخلفية
fig.set_facecolor("#121212")
ax.set_facecolor("#121212")

# رسم دوائر الخلفية
radar.draw_circles(ax=ax, facecolor='#1e1e1e', edgecolor='#ffd700', lw=0.5)

# رسم إحصائيات اللاعب (أزرق من الداخل وحافة حمراء)
radar.draw_radar(
    player_values, 
    ax=ax, 
    kwargs_radar={'facecolor': '#1f77b4', 'alpha': 0.6, 'edgecolor': '#ff4d4d', 'lw': 2.5},
    kwargs_rings={'facecolor': '#222222'}
)

# رسم التسميات والحدود
radar.draw_range_labels(ax=ax, fontsize=9, color='#ffd700')
radar.draw_param_labels(ax=ax, fontsize=11, color='#ffd700', fontweight='bold')

plt.title("Player Performance Chart", fontsize=16, weight='bold', color='#ffd700', pad=20)

# ==========================================
# 4. عرض المحتوى وأزرار التحميل المنفصلة والواضحة
# ==========================================
col1, col2 = st.columns([3, 1])

with col1:
    st.pyplot(fig)

with col2:
    st.subheader("صورة اللاعب")
    st.image(player_image, use_container_width=True)
    
    # زر تحميل صورة اللاعب منفصلة
    img_buf = io.BytesIO()
    player_image.save(img_buf, format="PNG")
    img_buf.seek(0)
    st.download_button(
        label="📥 تحميل صورة اللاعب فقط",
        data=img_buf,
        file_name="player_image.png",
        mime="image/png"
    )
    
    st.markdown("---")
    
    # زر تحميل الرسم البياني منفصلاً بجودة عالية
    chart_buf = io.BytesIO()
    fig.savefig(chart_buf, format="png", dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    chart_buf.seek(0)
    
    st.download_button(
        label="📥 تحميل الرسم البياني (Radar)",
        data=chart_buf,
        file_name="radar_chart.png",
        mime="image/png"
    )
    
    st.info("💡 تم توفير زر لتحميل الرسم البياني وزر لتحميل الصورة لضمان حصولك على أعلى جودة لكل عنصر بدون أي تداخل أو قص.")

import streamlit as st
from urllib.request import urlopen
from PIL import Image
import matplotlib.pyplot as plt
from mplsoccer import Radar

# إعداد صفحة ستريملايت لتكون بعرض واسع
st.set_page_config(page_title="Football Player Radar Chart", layout="wide")

st.title("⚽ تطبيق تحليل أداء اللاعبين")
st.write("قم بتعديل إحصائيات اللاعب أو ارفع صورة جديدة من القائمة الجانبية!")

# ==========================================
# 1. القائمة الجانبية (رفع الصورة + القيم)
# ==========================================
st.sidebar.header("🖼️ تغيير صورة اللاعب")
uploaded_file = st.sidebar.file_uploader("اختر صورة اللاعب (PNG أو JPG)", type=["png", "jpg", "jpeg"])

st.sidebar.header("🔧 تعديل إحصائيات اللاعب")
params = [
    "Goals", "npxG", "xA", "SCA",
    "PA Entries", "Prog Passes", "Prog Carries", 
    "Tackles", "Interceptions", "Recoveries"
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
# 3. إعداد ورسم الـ Radar (حافة حمراء للخط المتغير)
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

# رسم دوائر الخلفية
radar.draw_circles(ax=ax, facecolor='#1e1e1e', edgecolor='#ffd700', lw=0.5)

# رسم إحصائيات اللاعب: لون داخلي أزرق مع حافة باللون الأحمر ('#ff4d4d')
radar.draw_radar(
    player_values, 
    ax=ax, 
    kwargs_radar={'facecolor': '#1f77b4', 'alpha': 0.6, 'edgecolor': '#ff4d4d', 'lw': 2.5},
    kwargs_rings={'facecolor': '#222222'}
)

# رسم التسميات والحدود بدون زحمة
radar.draw_range_labels(ax=ax, fontsize=9, color='#ffd700')
radar.draw_param_labels(ax=ax, fontsize=11, color='#ffd700', fontweight='bold')

# تنسيق الخلفية والعنوان
fig.set_facecolor("#121212")
ax.set_facecolor("#121212")
plt.title("Player Performance Chart", fontsize=16, weight='bold', color='#ffd700', pad=20)

# ==========================================
# 4. عرض المحتوى في الواجهة
# ==========================================
col1, col2 = st.columns([3, 1])

with col1:
    st.pyplot(fig)

with col2:
    st.subheader("صورة اللاعب")
    st.image(player_image, use_container_width=True)
    st.info("💡 يمكنك رفع أي صورة جديدة وستظهر مباشرة هنا وفي التطبيق.")

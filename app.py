import streamlit as st
from urllib.request import urlopen
from PIL import Image
import matplotlib.pyplot as plt
from mplsoccer import Radar

# إعداد صفحة ستريملايت لتكون بعرض واسع
st.set_page_config(page_title="Football Player Radar Chart", layout="wide")

st.title("⚽ تطبيق تحليل أداء اللاعبين (Radar Chart)")
st.write("قم بتعديل قيم اللاعب وإحصائياته أو ارفع صورة جديدة من القائمة الجانبية!")

# ==========================================
# 1. القائمة الجانبية (رفع الصورة + تعديل القيم)
# ==========================================
st.sidebar.header("🖼️ تغيير صورة اللاعب")
uploaded_file = st.sidebar.file_uploader("اختر صورة (PNG أو JPG)", type=["png", "jpg", "jpeg"])

st.sidebar.header("🔧 تعديل بيانات اللاعب")
params = [
    "Goals", "npxG", "xA", "SCA",
    "PA Entries", "Touches/Turnover", "Prog Passes",
    "Prog Carries", "Final 1/3 Passes", "Final 1/3 Carries", "Pressure Regains",
    "Tackles", "Interceptions", "Recoveries", "Aerial Win %"
]

low = [0] * len(params)
high = [99] * len(params)

player_values = []
for param in params:
    val = st.sidebar.slider(f"{param}", 0, 99, 50)
    player_values.append(val)

# ==========================================
# 2. إدارة الصورة (المفروضة أو المرفوعة)
# ==========================================
if uploaded_file is not None:
    # استخدام الصورة التي قام المستخدم برفعها
    player_image = Image.open(uploaded_file)
    image_caption = "الصورة المرفوعة"
else:
    # الصورة الافتراضية في حال لم يتم رفع شيء
    @st.cache_resource
    def load_default_image():
        URL = "https://raw.githubusercontent.com/andrewRowlinson/mplsoccer-assets/main/fdj_cropped.png"
        return Image.open(urlopen(URL))
    player_image = load_default_image()
    image_caption = "Frenkie de Jong (افتراضية)"

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

# رسم دوائر الخلفية
radar.draw_circles(ax=ax, facecolor='#222222', edgecolor='#333333')

# رسم إحصائيات اللاعب
radar.draw_radar(
    player_values, 
    ax=ax, 
    kwargs_radar={'facecolor': '#1a4f7c', 'alpha': 0.6},
    kwargs_rings={'facecolor': '#333333'}
)

# رسم التسميات
radar.draw_range_labels(ax=ax, fontsize=10, color='#ffffff')
radar.draw_param_labels(ax=ax, fontsize=12, color='#ffffff', fontweight='bold')

# تنسيق الخلفية والعنوان
fig.set_facecolor("#121212")
ax.set_facecolor("#121212")
plt.title("Player Performance Radar Chart", fontsize=16, weight='bold', color='white', pad=20)

# ==========================================
# 4. العرض في واجهة التطبيق
# ==========================================
col1, col2 = st.columns([3, 1])

with col1:
    st.pyplot(fig)

with col2:
    st.subheader("صورة اللاعب")
    st.image(player_image, caption=image_caption, use_container_width=True)
    st.info("💡 يمكنك الآن رفع أي صورة من جهازك عبر القائمة الجانبية لتظهر بجانب الرسم فوراً.")

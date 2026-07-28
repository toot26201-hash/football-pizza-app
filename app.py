import streamlit as st
from urllib.request import urlopen
from PIL import Image
import matplotlib.pyplot as plt
from mplsoccer import Radar

# إعداد صفحة ستريملايت لتكون بعرض واسع
st.set_page_config(page_title="Football Player Radar Chart", layout="wide")

st.title("⚽ تطبيق تحليل أداء اللاعبين (Radar Chart)")
st.write("قم بتعديل قيم اللاعب من القائمة الجانبية وشاهد التغيير فوراً في الرسم البياني!")

# ==========================================
# 1. إعداد البيانات والمعلمات (Params & Values)
# ==========================================
params = [
    "Goals", "npxG", "xA", "SCA",
    "PA Entries", "Touches/Turnover", "Prog Passes",
    "Prog Carries", "Final 1/3 Passes", "Final 1/3 Carries", "Pressure Regains",
    "Tackles", "Interceptions", "Recoveries", "Aerial Win %"
]

# إعداد الحدود الدنيا والعليا لكل مؤشر
low = [0] * len(params)
high = [99] * len(params)

# القوائم الجانبية لتعديل القيم بحرية
st.sidebar.header("🔧 تعديل بيانات اللاعب")
player_values = []
for param in params:
    val = st.sidebar.slider(f"{param}", 0, 99, 50)
    player_values.append(val)

# ==========================================
# 2. تحميل صورة اللاعب
# ==========================================
@st.cache_resource
def load_image():
    URL = "https://raw.githubusercontent.com/andrewRowlinson/mplsoccer-assets/main/fdj_cropped.png"
    return Image.open(urlopen(URL))

fdj_cropped = load_image()

# ==========================================
# 3. إعداد ورسم الـ Radar بالشكل الصحيح 100%
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

# رسم الإحصائيات بالطريقة الصحيحة عبر kwargs_radar
radar.draw_radar(
    player_values, 
    ax=ax, 
    kwargs_radar={'facecolor': '#1a4f7c', 'alpha': 0.6},
    kwargs_rings={'facecolor': '#333333'}
)

# رسم التسميات والحدود لتوضيح البيانات
radar.draw_range_labels(ax=ax, fontsize=10, color='#ffffff')
radar.draw_param_labels(ax=ax, fontsize=12, color='#ffffff', fontweight='bold')

# إعداد خلفية الرسم والعنوان
fig.set_facecolor("#121212")
ax.set_facecolor("#121212")
plt.title("Player Performance Radar Chart", fontsize=16, weight='bold', color='white', pad=20)

# ==========================================
# 4. عرض المحتوى في الواجهة
# ==========================================
col1, col2 = st.columns([3, 1])

with col1:
    st.pyplot(fig)

with col2:
    st.subheader("صورة اللاعب")
    st.image(fdj_cropped, caption="Frenkie de Jong", use_container_width=True)
    st.info("💡 تحكم في أرقام اللاعب من القائمة الجانبية وسيتحدث الرسم فوراً.")

import streamlit as st
from urllib.request import urlopen
from PIL import Image
import matplotlib.pyplot as plt
from mplsoccer import PyPizza

# إعداد صفحة ستريملايت لتكون بعرض واسع
st.set_page_config(page_title="Football Player Pizza Chart", layout="wide")

st.title("⚽ تطبيق تحليل أداء اللاعبين (PyPizza Model)")
st.write("قم بتعديل إحصائيات اللاعب أو ارفع صورة جديدة من القائمة الجانبية!")

# ==========================================
# 1. القائمة الجانبية (رفع الصورة + القيم)
# ==========================================
st.sidebar.header("🖼️ تغيير صورة اللاعب")
uploaded_file = st.sidebar.file_uploader("اختر صورة اللاعب (PNG أو JPG)", type=["png", "jpg", "jpeg"])

st.sidebar.header("🔧 تعديل إحصائيات اللاعب")
params = [
    "Goals", "npxG", "xA", "SCA",
    "PA Entries", "Touches/Turnover", "Prog Passes",
    "Prog Carries", "Final 1/3 Passes", "Final 1/3 Carries", "Pressure Regains",
    "Tackles", "Interceptions", "Recoveries", "Aerial Win %"
]

player_values = []
for param in params:
    val = st.sidebar.slider(f"{param}", 0, 99, 50)
    player_values.append(val)

# ==========================================
# 2. إدارة الصورة (المرفوعة أو الافتراضية)
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
# 3. إعداد ورسم الـ PyPizza Chart (النموذج القياسي الآمن)
# ==========================================
baker = PyPizza(
    params=params,
    straight_line_color="#222222",
    straight_line_lw=1,
    last_circle_lw=1,
    other_circle_lw=0,
    inner_circle_size=20
)

# الرسم بالطريقة القياسية الخالية من أي وسائط معقدة
fig, ax = baker.make_pizza(
    player_values,
    figsize_square=8,
    facecolor="#313332",
    bg_color="#121212",
    slice_colors=["#1a4f7c"] * len(params),
    value_colors=["#ffffff"] * len(params),
    kwargs_slices=dict(edgecolor="#121212", linewidth=2, zorder=2),
    kwargs_params=dict(color="#ffffff", fontsize=11, fontweight="bold", va="center")
)

# إضافة عنوان للرسم
fig.text(
    0.51, 0.97, "Player Performance - Pizza Chart", 
    size=18, fontweight="bold", ha="center", color="#ffffff"
)

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

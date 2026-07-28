import streamlit as st
from urllib.request import urlopen
import matplotlib.pyplot as plt
from PIL import Image
from mplsoccer import PyPizza, FontManager

# إعداد صفحة ستريملايت لتكون بعرض واسع
st.set_page_config(page_title="Football Player Pizza Chart", layout="wide")

st.title("⚽ تطبيق تحليل أداء اللاعبين (Streamlit + mplsoccer)")
st.write("قم بتعديل قيم اللاعب من القائمة الجانبية وشاهد التغيير فوراً في الرسم البياني!")

# ==========================================
# 1. إعداد البيانات والمعلمات (Params & Values)
# ==========================================
params = [
    "Non-Penalty Goals", "npxG", "xA", "Open Play SCA",
    "Penalty Area Entries", "Touches per Turnover", "Progressive Passes",
    "Progressive Carries", "Final 1/3 Passes", "Final 1/3 Carries", "Pressure Regains",
    "Tackles Made", "Interceptions", "Recoveries", "Aerial Win %"
]

# القوائم الجانبية لتعديل القيم بحرية
st.sidebar.header("🔧 تعديل بيانات اللاعب")
player_values = []
for param in params:
    val = st.sidebar.slider(f"{param}", 0, 99, 50)
    player_values.append(val)

# ==========================================
# 2. تحميل صورة اللاعب والصقها
# ==========================================
@st.cache_resource
def load_image():
    URL = "https://raw.githubusercontent.com/andrewRowlinson/mplsoccer-assets/main/fdj_cropped.png"
    return Image.open(urlopen(URL))

fdj_cropped = load_image()

# ==========================================
# 3. إعداد ورسم الـ Pizza Chart
# ==========================================
# تخصيص الألوان (شرائح مظلمة ومضيئة)
slice_colors = ["#1a4f7c"] * len(params)
text_colors = ["#000000"] * len(params)

baker = PyPizza(
    params=params,
    min_range=0,
    max_range=99,
    straight_line_color="#222222",
    straight_line_lw=1,
    last_circle_lw=1,
    other_circle_lw=0,
    inner_circle_size=20
)

# إنشاء الرسم
fig, ax = baker.make_pizza(
    player_values,
    figsize_square=8,
    facecolor="#313332",
    bg_color="#121212",
    slice_colors=slice_colors,
    value_colors=text_colors,
    value_bg_colors=slice_colors,
    kwargs_slices=dict(edgecolor="#121212", linewidth=2, zorder=2),
    kwargs_params=dict(color="#ffffff", fontsize=11, fontweight="bold", va="center"),
    kwargs_values=dict(color="#ffffff", fontsize=11, zorder=3,
                       bbox=dict(edgecolor="#000000", facecolor="#1a4f7c", boxstyle="round,pad=0.2", lw=1))
)

# إضافة عنوان وشرح داخل الرسم
fig.text(
    0.51, 0.97, "Frenkie de Jong - Performance Pizza Chart", 
    size=18, fontweight="bold", ha="center", color="#ffffff"
)

# عرض الرسم داخل تطبيق ستريملايت
col1, col2 = st.columns([3, 1])

with col1:
    st.pyplot(fig)

with col2:
    st.subheader("صورة اللاعب")
    st.image(fdj_cropped, caption="Frenkie de Jong", use_column_width=True)
    st.info("💡 يمكنك التحكم في أرقام اللاعب وإحصائياته مباشرة من القائمة الجانبية (Sidebar) في أقصى اليسار/اليمين.")

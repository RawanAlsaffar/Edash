import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import warnings
import os
import json

warnings.filterwarnings('ignore')

# المسار الأساسي للمشروع
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────
# إعدادات الصفحة
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="تحليل الكهرباء - الهلال الأحمر السعودي",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS - هوية الهلال الأحمر السعودي (أحمر + رمادي + أبيض)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ===== الخلفية العامة ===== */
.stApp {
    background-color: #f8f9fa;
    color: #1a1a2e;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    direction: rtl;
}

/* ===== الشريط الجانبي ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #fdf5f5 100%);
    border-left: 1px solid #f0d0d0;
    border-right: none;
}
[data-testid="stSidebar"] * { color: #1a1a2e !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #555 !important; font-size: 14px !important;
}

/* ===== بطاقات KPI - حجم متوسط متوازن ===== */
.kpi-card {
    background: #ffffff;
    border: 1px solid #ead8d8;
    border-radius: 12px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    margin-bottom: 10px;
    box-shadow: 0 2px 6px rgba(180,0,0,0.06);
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(180,0,0,0.10);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 4px;
    height: 100%;
    border-radius: 0 12px 12px 0;
}
.kpi-card.red::before    { background: #c0392b; }
.kpi-card.green::before  { background: #27ae60; }
.kpi-card.blue::before   { background: #2980b9; }
.kpi-card.orange::before { background: #e67e22; }
.kpi-card.purple::before { background: #8e44ad; }
.kpi-card.teal::before   { background: #16a085; }
.kpi-card.crimson::before{ background: #c0392b; }

.kpi-label {
    color: #7a7a8a;
    font-size: 13px;
    margin-bottom: 6px;
    font-weight: 500;
}
.kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: #1a1a2e;
    line-height: 1.2;
}
.kpi-value.red    { color: #c0392b; }
.kpi-value.green  { color: #27ae60; }
.kpi-value.blue   { color: #2980b9; }
.kpi-value.orange { color: #e67e22; }
.kpi-value.purple { color: #8e44ad; }
.kpi-value.teal   { color: #16a085; }
.kpi-value.crimson{ color: #c0392b; }

.kpi-delta { font-size: 12px; margin-top: 5px; }
.kpi-delta.up   { color: #27ae60; }
.kpi-delta.down { color: #c0392b; }
.kpi-icon {
    position: absolute;
    top: 12px;
    left: 14px;
    font-size: 28px;
    opacity: 0.08;
}

/* ===== بطاقات KPI الثابتة (عدد الحسابات) - حجم متوسط ===== */
.static-kpi-card {
    background: #ffffff;
    border: 1px solid #ead8d8;
    border-radius: 12px;
    padding: 18px 16px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(180,0,0,0.06);
    margin-bottom: 10px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.static-kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(180,0,0,0.10);
}
.static-kpi-year {
    font-size: 14px;
    font-weight: 600;
    color: #7a7a8a;
    margin-bottom: 8px;
}
.static-kpi-value {
    font-size: 36px;
    font-weight: 800;
    line-height: 1.1;
}
.static-kpi-label {
    font-size: 13px;
    color: #7a7a8a;
    margin-top: 5px;
}

/* ===== رأس الصفحة - هوية الهلال الأحمر ===== */
.main-header {
    background: linear-gradient(135deg, #8b0000 0%, #c0392b 60%, #e74c3c 100%);
    border-radius: 14px;
    padding: 20px 26px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 16px rgba(192,57,43,0.25);
}
.main-header h1 {
    color: #ffffff !important;
    font-size: 22px !important;
    margin: 0 !important;
    font-weight: 700 !important;
}
.main-header p {
    color: #ffd5d0 !important;
    font-size: 13px !important;
    margin: 4px 0 0 !important;
}

/* ===== رأس الأقسام ===== */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 24px 0 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid #f0d8d8;
}
.section-header h3 {
    color: #8b0000 !important;
    font-size: 17px !important;
    margin: 0 !important;
    font-weight: 700;
}
.section-icon {
    background: #fdf0f0;
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 12px;
    color: #c0392b;
    font-weight: 700;
    letter-spacing: 0.5px;
    border: 1px solid #f5c6c2;
}

/* ===== شارات ===== */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}
.badge-green  { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.badge-blue   { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
.badge-red    { background: #fde8e6; color: #8b0000; border: 1px solid #f5c6c2; }
.badge-orange { background: #fff3cd; color: #856404; border: 1px solid #ffeeba; }

/* ===== بطاقات الإحصاءات الوصفية ===== */
.stat-card {
    background: #ffffff;
    border: 1px solid #ead8d8;
    border-radius: 10px;
    padding: 14px 14px;
    text-align: center;
    box-shadow: 0 2px 5px rgba(180,0,0,0.05);
    margin-bottom: 8px;
}
.stat-card .stat-label {
    color: #7a7a8a;
    font-size: 12px;
    margin-bottom: 6px;
    font-weight: 500;
}
.stat-card .stat-value {
    font-size: 22px;
    font-weight: 700;
}
.stat-card .stat-year {
    font-size: 11px;
    color: #9aa5b4;
    margin-top: 3px;
}

/* ===== بطاقات معلومات النموذج ===== */
.model-info-card {
    background: #ffffff;
    border: 1px solid #ead8d8;
    border-radius: 12px;
    padding: 18px 16px;
    margin-bottom: 10px;
    box-shadow: 0 2px 6px rgba(180,0,0,0.06);
}
.model-info-card h4 {
    color: #7a7a8a;
    font-size: 12px;
    margin: 0 0 8px;
    font-weight: 500;
}
.model-info-card .model-value {
    font-size: 24px;
    font-weight: 700;
    line-height: 1.2;
}
.model-info-card .model-sub {
    font-size: 11px;
    color: #9aa5b4;
    margin-top: 4px;
}

/* ===== بطاقات التنبيه ===== */
.alert-card {
    background: #ffffff;
    border: 1px solid #ead8d8;
    border-radius: 10px;
    padding: 12px 14px;
    margin: 5px 0;
    box-shadow: 0 1px 4px rgba(180,0,0,0.04);
}
.alert-card.warning { border-right: 4px solid #e67e22; }
.alert-card.danger  { border-right: 4px solid #c0392b; }
.alert-card.info    { border-right: 4px solid #2980b9; }
.alert-card.success { border-right: 4px solid #27ae60; }

/* ===== بطاقات الأرباع ===== */
.quarter-card {
    background: #ffffff;
    border: 1px solid #ead8d8;
    border-radius: 10px;
    padding: 16px 14px;
    text-align: center;
    margin: 4px 0;
    box-shadow: 0 2px 6px rgba(180,0,0,0.06);
}
.quarter-card h4 {
    color: #7a7a8a !important;
    font-size: 13px !important;
    margin: 0 0 8px !important;
    font-weight: 600;
}
.quarter-card .q-value {
    font-size: 22px;
    font-weight: 700;
}
.quarter-card .q-label {
    font-size: 11px;
    color: #9aa5b4;
    margin-top: 4px;
}

/* ===== بطاقة شرح RMSE/MAE ===== */
.metric-explain-card {
    background: #fdf0f0;
    border: 1px solid #f5c6c2;
    border-radius: 12px;
    padding: 16px 18px;
    margin: 10px 0;
}
.metric-explain-card h4 {
    color: #8b0000;
    font-size: 14px;
    margin: 0 0 8px;
    font-weight: 700;
}
.metric-explain-card p {
    color: #2c3e50;
    font-size: 13px;
    margin: 0;
    line-height: 1.6;
}

/* ===== بطاقة الحساب الزائد ===== */
.extra-ca-card {
    background: #ffffff;
    border: 1px solid #ead8d8;
    border-radius: 10px;
    padding: 14px 16px;
    margin: 6px 0;
    box-shadow: 0 1px 5px rgba(180,0,0,0.06);
    border-right: 4px solid #c0392b;
    transition: transform 0.15s, box-shadow 0.15s;
}
.extra-ca-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(180,0,0,0.10);
}
.extra-ca-title {
    color: #8b0000;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 4px;
}
.extra-ca-meta {
    color: #7a7a8a;
    font-size: 12px;
}

/* ===== التبويبات ===== */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #ffffff;
    border-radius: 12px;
    padding: 4px;
    gap: 3px;
    border: 1px solid #ead8d8;
    box-shadow: 0 2px 6px rgba(180,0,0,0.05);
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent;
    color: #7a7a8a;
    border-radius: 8px;
    padding: 9px 16px;
    font-size: 13px;
    font-weight: 500;
    border: none;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #c0392b !important;
    color: white !important;
    font-weight: 700 !important;
}

/* ===== عناصر Streamlit الأساسية ===== */
[data-baseweb="tag"] {
    background-color: #fde8e6 !important;
    border: 1px solid #f5c6c2 !important;
    color: #8b0000 !important;
}
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f8f9fa; }
::-webkit-scrollbar-thumb { background: #d4a0a0; border-radius: 3px; }
hr { border-color: #f0d8d8 !important; }

[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #ead8d8 !important;
    border-radius: 12px !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, #8b0000, #c0392b) !important;
}
[data-baseweb="select"] {
    background: #ffffff !important;
    border-color: #dde3ea !important;
}
[data-baseweb="select"] * {
    background: #ffffff !important;
    color: #1a1a2e !important;
}
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #ead8d8 !important;
    border-radius: 10px !important;
    padding: 14px !important;
}
[data-testid="stMetricLabel"] {
    color: #7a7a8a !important;
    font-size: 13px !important;
}
[data-testid="stMetricValue"] {
    color: #1a1a2e !important;
    font-size: 24px !important;
}

/* ===== تذييل الصفحة ===== */
.footer {
    text-align: center;
    color: #9aa5b4;
    font-size: 12px;
    padding: 20px 0 10px;
    border-top: 1px solid #f0d8d8;
    margin-top: 32px;
}

/* ===== بطاقة معلومات مميزة ===== */
.info-banner {
    background: linear-gradient(135deg, #fdf0f0 0%, #fff8f8 100%);
    border: 1px solid #f5c6c2;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 10px 0 16px;
    color: #8b0000;
    font-size: 14px;
}
.info-banner b { color: #c0392b; }

/* ===== بطاقة KPI الزائدة (عدد) ===== */
.excess-count-card {
    background: linear-gradient(135deg, #fff5f5 0%, #fde8e6 100%);
    border: 1px solid #f5c6c2;
    border-radius: 12px;
    padding: 16px 18px;
    text-align: center;
    margin-bottom: 10px;
}
.excess-count-card .ec-num {
    font-size: 40px;
    font-weight: 800;
    color: #c0392b;
    line-height: 1;
}
.excess-count-card .ec-label {
    font-size: 13px;
    color: #7a7a8a;
    margin-top: 4px;
}
.excess-count-card .ec-year {
    font-size: 12px;
    color: #c0392b;
    font-weight: 600;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# تحميل البيانات
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(BASE_DIR, 'SRCA_Electricity_Data.csv'))
    df['Year'] = df['Year'].astype(int)
    df['Month'] = df['Month'].astype(int)
    df['Collective_CA'] = df['Collective_CA'].astype(str)
    df['Contract_Account'] = df['Contract_Account'].astype(str)
    return df

@st.cache_data
def load_predictions():
    pred = pd.read_csv(os.path.join(BASE_DIR, 'SRCA_2026_Predictions.csv'))
    pred['Collective_CA'] = pred['Collective_CA'].astype(str)
    pred['Contract_Account'] = pred['Contract_Account'].astype(str)
    return pred

@st.cache_data
def load_q1_comparison():
    comp = pd.read_csv(os.path.join(BASE_DIR, 'SRCA_Q1_2026_Comparison.csv'))
    comp['Collective_CA'] = comp['Collective_CA'].astype(str)
    comp['Contract_Account'] = comp['Contract_Account'].astype(str)
    return comp

@st.cache_data
def load_model_metrics():
    metrics_path = os.path.join(BASE_DIR, 'model_metrics.json')
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            return json.load(f)
    return None

@st.cache_data
def compute_extra_cas(df_full):
    """
    حساب الحسابات التجميعية الزائدة لكل سنة
    الأصلية = 37 حساب (الموجودة في 2026)
    الزائدة = الموجودة في 2024/2025 ولا توجد في 2026
    """
    original_cas = set(df_full[df_full['Year'] == 2026]['Collective_CA'].unique())
    ca_2024 = set(df_full[df_full['Year'] == 2024]['Collective_CA'].unique())
    ca_2025 = set(df_full[df_full['Year'] == 2025]['Collective_CA'].unique())

    extra_2024 = sorted(ca_2024 - original_cas)
    extra_2025 = sorted(ca_2025 - original_cas)

    return original_cas, extra_2024, extra_2025

# تحميل البيانات
df = load_data()
pred_df = load_predictions()
comp_df = load_q1_comparison()
model_metrics = load_model_metrics()

# ─────────────────────────────────────────────
# الثوابت
# ─────────────────────────────────────────────
YEAR_COLORS = {2024: '#2980b9', 2025: '#27ae60', 2026: '#c0392b'}

REGION_COLORS = {
    'الوسطى':  '#1565C0',   # أزرق داكن قوي
    'الغربية': '#2E7D32',   # أخضر داكن
    'الشرقية': '#B71C1C',   # أحمر داكن
    'الشمالية':'#6A1B9A',   # بنفسجي داكن
    'الجنوبية':'#E65100',   # برتقالي داكن
}

MONTH_NAMES = {
    1: 'يناير', 2: 'فبراير', 3: 'مارس', 4: 'أبريل',
    5: 'مايو', 6: 'يونيو', 7: 'يوليو', 8: 'أغسطس',
    9: 'سبتمبر', 10: 'أكتوبر', 11: 'نوفمبر', 12: 'ديسمبر'
}

# القيم الثابتة لعدد الحسابات التجميعية
STATIC_CA_COUNTS = {2024: 58, 2025: 41, 2026: 37}
ORIGINAL_CA_COUNT = 37  # الحسابات الأصلية الحقيقية
# حد الاستهلاك المنخفض جداً (kWh)
NEAR_ZERO_THRESHOLD = 1.67

def classify_consumption(total_kwh):
    """تصنيف الاستهلاك: صفري / منخفض جداً / حقيقي"""
    if total_kwh == 0:
        return 'صفري', '#B71C1C', '🔴'
    elif total_kwh <= NEAR_ZERO_THRESHOLD:
        return 'منخفض جداً', '#E65100', '🟠'
    else:
        return 'حقيقي', '#2E7D32', '🟢'

# ─────────────────────────────────────────────
# دوال مساعدة للرسوم البيانية
# ─────────────────────────────────────────────
def light_layout(height=300, title='', showlegend=False, **kwargs):
    base = dict(
        height=height,
        paper_bgcolor='#ffffff',
        plot_bgcolor='#fdf8f8',
        font=dict(color='#1a1a2e', size=13, family='Arial'),
        margin=dict(l=20, r=20, t=40 if title else 20, b=20),
        showlegend=showlegend,
        legend=dict(
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#ead8d8',
            borderwidth=1,
            font=dict(size=13)
        ),
    )
    if title:
        base['title'] = dict(text=title, font=dict(size=15, color='#8b0000'), x=0.01)
    base.update(kwargs)
    return base

def light_xaxis(**kwargs):
    base = dict(
        gridcolor='#f5e8e8',
        linecolor='#ead8d8',
        tickfont=dict(color='#4a5568', size=12),
        zerolinecolor='#ead8d8'
    )
    base.update(kwargs)
    return base

def light_yaxis(**kwargs):
    base = dict(
        gridcolor='#f5e8e8',
        linecolor='#ead8d8',
        tickfont=dict(color='#4a5568', size=12),
        zerolinecolor='#ead8d8'
    )
    base.update(kwargs)
    return base

def fmt_num(n, unit=''):
    """تنسيق الأرقام بشكل مختصر"""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M {unit}".strip()
    elif n >= 1_000:
        return f"{n/1_000:.1f}K {unit}".strip()
    return f"{n:.0f} {unit}".strip()

def delta_pct(new_val, old_val):
    """حساب نسبة التغيير المئوية"""
    if old_val == 0:
        return 0
    return ((new_val - old_val) / old_val) * 100

def kpi_card(label, value, delta=None, color='blue', icon=''):
    """إنشاء بطاقة KPI بحجم متوسط متوازن"""
    delta_html = ''
    if delta is not None:
        arrow = '▲' if delta > 0 else '▼'
        cls = 'up' if delta > 0 else 'down'
        delta_html = f'<div class="kpi-delta {cls}">{arrow} {abs(delta):.1f}% مقارنة بالعام السابق</div>'
    icon_html = f'<div class="kpi-icon">{icon}</div>' if icon else ''
    return (
        f'<div class="kpi-card {color}">'
        f'{icon_html}'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value {color}">{value}</div>'
        f'{delta_html}'
        f'</div>'
    )

def static_ca_kpi(year, count, color, label_suffix=''):
    """بطاقة KPI ثابتة لعدد الحسابات التجميعية - حجم متوسط"""
    year_label = f"{year}" if not label_suffix else f"{year} {label_suffix}"
    return (
        f'<div class="static-kpi-card">'
        f'<div class="static-kpi-year">سنة {year_label}</div>'
        f'<div class="static-kpi-value" style="color:{color};">{count}</div>'
        f'<div class="static-kpi-label">حساب تجميعي</div>'
        f'</div>'
    )

def section_header(icon_text, title):
    """رأس قسم موحد"""
    return (
        f'<div class="section-header">'
        f'<span class="section-icon">{icon_text}</span>'
        f'<h3>{title}</h3>'
        f'</div>'
    )

def get_ca_summary(df_full, ca_id, year):
    """استخراج ملخص حساب تجميعي معين"""
    df_ca = df_full[(df_full['Collective_CA'] == ca_id) & (df_full['Year'] == year)]
    if len(df_ca) == 0:
        return None
    region_mode = df_ca['Region_Major'].dropna().mode()
    region = region_mode.iloc[0] if len(region_mode) > 0 else '-'
    city_mode = df_ca['Region_City'].dropna().mode() if 'Region_City' in df_ca.columns else pd.Series([])
    city = city_mode.iloc[0] if len(city_mode) > 0 else '-'
    n_contracts = df_ca['Contract_Account'].nunique()
    total_kwh = df_ca['Consumption_kWh'].sum()
    total_sar = df_ca['Bill_Amount'].sum()
    n_months = df_ca['Month'].nunique()
    return {
        'region': region, 'city': city,
        'n_contracts': n_contracts,
        'total_kwh': total_kwh,
        'total_sar': total_sar,
        'n_months': n_months,
        'contracts': sorted(df_ca['Contract_Account'].unique().tolist())
    }

# ─────────────────────────────────────────────
# الشريط الجانبي
# ─────────────────────────────────────────────
with st.sidebar:
    logo_path = os.path.join(BASE_DIR, 'SRCAlogo_local_cmyk.jpg')
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown(
            '<h2 style="text-align:center; color:#c0392b; font-size:18px;">🌙 الهلال الأحمر السعودي</h2>',
            unsafe_allow_html=True
        )

    st.markdown("### فلاتر البيانات")

    all_years_option = st.checkbox("الكل (جميع السنوات)", value=True, key="all_years_cb")
    if all_years_option:
        selected_years = [2024, 2025, 2026]
        st.multiselect(
            "السنة",
            options=[2024, 2025, 2026],
            default=[2024, 2025, 2026],
            key="years",
            disabled=True,
            help="قم بإلغاء تحديد 'الكل' لاختيار سنوات محددة"
        )
    else:
        selected_years = st.multiselect(
            "السنة",
            options=[2024, 2025, 2026],
            default=[2024, 2025, 2026],
            key="years"
        )
        if not selected_years:
            selected_years = [2024, 2025, 2026]

    regions = ['الكل'] + sorted(df['Region_Major'].dropna().unique().tolist())
    selected_region = st.selectbox("المنطقة الرئيسية", regions, key="region")

    ca_options = ['الكل'] + sorted(df['Collective_CA'].unique().tolist())
    selected_ca = st.selectbox("الحساب التجميعي", ca_options, key="ca")

    max_cons = int(df['Consumption_kWh'].max())
    cons_range = st.slider(
        "نطاق الاستهلاك (كيلوواط/ساعة)",
        0, max_cons, (0, max_cons),
        key="cons"
    )

    st.markdown("---")
    st.markdown(
        '<div style="text-align:center; color:#9aa5b4; font-size:11px;">أبريل 2026</div>',
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────
# تطبيق الفلاتر
# ─────────────────────────────────────────────
mask = (
    df['Year'].isin(selected_years) &
    df['Consumption_kWh'].between(cons_range[0], cons_range[1])
)
if selected_region != 'الكل':
    mask &= df['Region_Major'] == selected_region
if selected_ca != 'الكل':
    mask &= df['Collective_CA'] == selected_ca

df_f = df[mask].copy()
df_24 = df_f[df_f['Year'] == 2024]
df_25 = df_f[df_f['Year'] == 2025]
df_26 = df_f[df_f['Year'] == 2026]

# ─────────────────────────────────────────────
# الرأس الرئيسي - هوية الهلال الأحمر
# ─────────────────────────────────────────────
total_records = len(df_f)
st.markdown(f"""
<div class="main-header">
    <div>
        <h1>⚡ تحليل استهلاك الكهرباء</h1>
        <p>هيئة الهلال الأحمر السعودي | بيانات 2024 - 2026</p>
    </div>
    <div style="text-align:left;">
        <span class="badge badge-green">● مباشر</span>
        <div style="color:#ffd5d0; font-size:12px; margin-top:5px;">إجمالي السجلات: {total_records:,}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# التبويبات الرئيسية
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab_geo, tab4, tab_excess = st.tabs([
    "📊 نظرة عامة",
    "📈 التحليل الإحصائي",
    "🏢 إدارة الأصول",
    "🗺️ التحليل الجغرافي",
    "🔮 توقعات 2026",
    "🔍 الحسابات الزائدة"
])

# ══════════════════════════════════════════════
# تبويب 1: نظرة عامة
# ══════════════════════════════════════════════
with tab1:
    # ── مؤشرات الاستهلاك ──
    total_24 = df_24['Consumption_kWh'].sum()
    total_25 = df_25['Consumption_kWh'].sum()
    total_full_26 = pred_df['Predicted_Consumption'].sum()
    delta_25_24 = delta_pct(total_25, total_24)
    delta_26_25 = delta_pct(total_full_26, total_25)
    num_sub = df_f['Contract_Account'].nunique()

    st.markdown(section_header('kWh', 'مؤشرات الاستهلاك (كيلوواط/ساعة)'), unsafe_allow_html=True)

    # صف أول: 3 بطاقات استهلاك
    kpi_row1 = st.columns(3)
    with kpi_row1[0]:
        st.markdown(kpi_card("إجمالي الاستهلاك 2024", fmt_num(total_24), None, 'blue'), unsafe_allow_html=True)
    with kpi_row1[1]:
        st.markdown(kpi_card("إجمالي الاستهلاك 2025", fmt_num(total_25), delta_25_24, 'green'), unsafe_allow_html=True)
    with kpi_row1[2]:
        st.markdown(kpi_card("توقعات الاستهلاك 2026", fmt_num(total_full_26), delta_26_25, 'orange'), unsafe_allow_html=True)

    # صف ثانٍ: 2 بطاقات
    kpi_row2 = st.columns(2)
    with kpi_row2[0]:
        st.markdown(kpi_card("إجمالي الحسابات الفرعية", str(num_sub), None, 'purple'), unsafe_allow_html=True)
    with kpi_row2[1]:
        bill_24 = df_24['Bill_Amount'].sum()
        bill_25 = df_25['Bill_Amount'].sum()
        delta_bill = delta_pct(bill_25, bill_24)
        st.markdown(kpi_card("إجمالي الفواتير 2025", fmt_num(bill_25, 'SAR'), delta_bill, 'red'), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── عدد الحسابات التجميعية (ثابت) ──
    st.markdown(section_header('حسابات', 'عدد الحسابات التجميعية (قيم ثابتة)'), unsafe_allow_html=True)
    ca_cols = st.columns(3)
    with ca_cols[0]:
        st.markdown(static_ca_kpi(2024, STATIC_CA_COUNTS[2024], '#2980b9'), unsafe_allow_html=True)
    with ca_cols[1]:
        st.markdown(static_ca_kpi(2025, STATIC_CA_COUNTS[2025], '#27ae60'), unsafe_allow_html=True)
    with ca_cols[2]:
        st.markdown(static_ca_kpi(2026, STATIC_CA_COUNTS[2026], '#c0392b', '(الربع الأول)'), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── الإحصاءات الوصفية للاستهلاك ──
    st.markdown(section_header('إحصاء', 'الإحصاءات الوصفية للاستهلاك (كيلوواط/ساعة)'), unsafe_allow_html=True)

    stat_cols = st.columns(3)

    with stat_cols[0]:
        st.markdown(f"""
        <div style="background:#f0f8ff; border:1px solid #bee3f8; border-radius:12px; padding:16px; margin-bottom:10px;">
            <div style="color:#2980b9; font-size:14px; font-weight:700; margin-bottom:12px; border-bottom:1px solid #bee3f8; padding-bottom:8px;">
                📅 سنة 2024
            </div>
        </div>
        """, unsafe_allow_html=True)
        s24 = df_24['Consumption_kWh']
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown(f'<div class="stat-card"><div class="stat-label">المتوسط</div><div class="stat-value" style="color:#2980b9;">{fmt_num(s24.mean())}</div><div class="stat-year">كيلوواط/ساعة</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stat-card"><div class="stat-label">الانحراف المعياري</div><div class="stat-value" style="color:#8e44ad;">{fmt_num(s24.std())}</div><div class="stat-year">كيلوواط/ساعة</div></div>', unsafe_allow_html=True)
        with sc2:
            st.markdown(f'<div class="stat-card"><div class="stat-label">الوسيط</div><div class="stat-value" style="color:#16a085;">{fmt_num(s24.median())}</div><div class="stat-year">كيلوواط/ساعة</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stat-card"><div class="stat-label">عدد السجلات</div><div class="stat-value" style="color:#e67e22;">{len(s24):,}</div><div class="stat-year">2024</div></div>', unsafe_allow_html=True)

    with stat_cols[1]:
        st.markdown(f"""
        <div style="background:#f0fff4; border:1px solid #c3e6cb; border-radius:12px; padding:16px; margin-bottom:10px;">
            <div style="color:#27ae60; font-size:14px; font-weight:700; margin-bottom:12px; border-bottom:1px solid #c3e6cb; padding-bottom:8px;">
                📅 سنة 2025
            </div>
        </div>
        """, unsafe_allow_html=True)
        s25 = df_25['Consumption_kWh']
        sc3, sc4 = st.columns(2)
        with sc3:
            st.markdown(f'<div class="stat-card"><div class="stat-label">المتوسط</div><div class="stat-value" style="color:#27ae60;">{fmt_num(s25.mean())}</div><div class="stat-year">كيلوواط/ساعة</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stat-card"><div class="stat-label">الانحراف المعياري</div><div class="stat-value" style="color:#8e44ad;">{fmt_num(s25.std())}</div><div class="stat-year">كيلوواط/ساعة</div></div>', unsafe_allow_html=True)
        with sc4:
            st.markdown(f'<div class="stat-card"><div class="stat-label">الوسيط</div><div class="stat-value" style="color:#16a085;">{fmt_num(s25.median())}</div><div class="stat-year">كيلوواط/ساعة</div></div>', unsafe_allow_html=True)
            growth_rate = delta_pct(s25.mean(), df_24['Consumption_kWh'].mean())
            arrow = '▲' if growth_rate >= 0 else '▼'
            color = '#27ae60' if growth_rate >= 0 else '#c0392b'
            st.markdown(f'<div class="stat-card"><div class="stat-label">معدل التغير 24→25</div><div class="stat-value" style="color:{color};">{arrow} {abs(growth_rate):.1f}%</div><div class="stat-year">نسبة مئوية</div></div>', unsafe_allow_html=True)

    with stat_cols[2]:
        st.markdown(f"""
        <div style="background:#fff5f5; border:1px solid #f5c6c2; border-radius:12px; padding:16px; margin-bottom:10px;">
            <div style="color:#c0392b; font-size:14px; font-weight:700; margin-bottom:12px; border-bottom:1px solid #f5c6c2; padding-bottom:8px;">
                📅 سنة 2026 (Q1)
            </div>
        </div>
        """, unsafe_allow_html=True)
        s26 = df_26['Consumption_kWh']
        sc5, sc6 = st.columns(2)
        with sc5:
            st.markdown(f'<div class="stat-card"><div class="stat-label">المتوسط</div><div class="stat-value" style="color:#c0392b;">{fmt_num(s26.mean()) if len(s26) > 0 else "—"}</div><div class="stat-year">كيلوواط/ساعة</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stat-card"><div class="stat-label">الانحراف المعياري</div><div class="stat-value" style="color:#8e44ad;">{fmt_num(s26.std()) if len(s26) > 0 else "—"}</div><div class="stat-year">كيلوواط/ساعة</div></div>', unsafe_allow_html=True)
        with sc6:
            st.markdown(f'<div class="stat-card"><div class="stat-label">الوسيط</div><div class="stat-value" style="color:#16a085;">{fmt_num(s26.median()) if len(s26) > 0 else "—"}</div><div class="stat-year">كيلوواط/ساعة</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stat-card"><div class="stat-label">عدد السجلات</div><div class="stat-value" style="color:#e67e22;">{len(s26):,}</div><div class="stat-year">2026 (Q1)</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── الاتجاه الشهري ──
    st.markdown(section_header('بياني', 'الاتجاه الشهري للاستهلاك'), unsafe_allow_html=True)

    fig_trend = go.Figure()
    for yr in sorted(selected_years):
        d = df_f[df_f['Year'] == yr].groupby('Month')['Consumption_kWh'].sum().reset_index().sort_values('Month')
        fig_trend.add_trace(go.Scatter(
            x=d['Month'], y=d['Consumption_kWh'],
            name=str(yr), mode='lines+markers',
            line=dict(color=YEAR_COLORS.get(yr, '#888'), width=2.5),
            marker=dict(size=7),
            hovertemplate=f'{yr} | الشهر %{{x}}: %{{y:,.0f}} kWh<extra></extra>'
        ))
    fig_trend.update_layout(**light_layout(height=320, showlegend=True))
    fig_trend.update_xaxes(**light_xaxis(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=[MONTH_NAMES[i] for i in range(1, 13)]
    ))
    fig_trend.update_yaxes(**light_yaxis(tickformat=',.0f'))
    st.plotly_chart(fig_trend, use_container_width=True, key="trend_line")

    # ── توزيع المناطق ومقارنة 2024 vs 2025 ──
    col_reg, col_cmp = st.columns(2)

    with col_reg:
        st.markdown(section_header('مناطق', 'توزيع الاستهلاك بالمناطق'), unsafe_allow_html=True)
        region_data = df_f.groupby('Region_Major')['Consumption_kWh'].sum().sort_values()
        fig_reg = go.Figure(go.Bar(
            x=region_data.values,
            y=region_data.index,
            orientation='h',
            marker=dict(
                color=[REGION_COLORS.get(r, '#888') for r in region_data.index],
                line=dict(color='#ffffff', width=1)
            ),
            text=[fmt_num(v) for v in region_data.values],
            textposition='outside',
            textfont=dict(color='#4a5568', size=12),
            hovertemplate='<b>%{y}</b><br>%{x:,.0f} kWh<extra></extra>'
        ))
        fig_reg.update_layout(**light_layout(height=300, showlegend=False))
        fig_reg.update_xaxes(**light_xaxis(tickformat=',.0f'))
        fig_reg.update_yaxes(**light_yaxis())
        st.plotly_chart(fig_reg, use_container_width=True, key="region_bar")

    with col_cmp:
        st.markdown(section_header('مقارنة', 'مقارنة الاستهلاك الشهري 2024 مقابل 2025'), unsafe_allow_html=True)
        m24 = df_f[df_f['Year'] == 2024].groupby('Month')['Consumption_kWh'].sum().reset_index()
        m25 = df_f[df_f['Year'] == 2025].groupby('Month')['Consumption_kWh'].sum().reset_index()
        fig_cmp = go.Figure()
        fig_cmp.add_trace(go.Bar(
            x=m24['Month'], y=m24['Consumption_kWh'],
            name='2024', marker=dict(color='#2980b9', opacity=0.85)
        ))
        fig_cmp.add_trace(go.Bar(
            x=m25['Month'], y=m25['Consumption_kWh'],
            name='2025', marker=dict(color='#27ae60', opacity=0.85)
        ))
        fig_cmp.update_layout(**light_layout(height=300, showlegend=True, barmode='group'))
        fig_cmp.update_xaxes(**light_xaxis(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=[MONTH_NAMES[i] for i in range(1, 13)]
        ))
        fig_cmp.update_yaxes(**light_yaxis(tickformat=',.0f'))
        st.plotly_chart(fig_cmp, use_container_width=True, key="compare_bar")

    # ── التوزيع الموسمي ──
    season_map = {
        'الربيع': [3, 4, 5], 'الصيف': [6, 7, 8],
        'الخريف': [9, 10, 11], 'الشتاء': [12, 1, 2]
    }
    season_colors = {
        'الصيف': '#c0392b', 'الخريف': '#e67e22',
        'الشتاء': '#2980b9', 'الربيع': '#27ae60'
    }
    season_totals = {
        s: df_f[df_f['Month'].isin(months)]['Consumption_kWh'].sum()
        for s, months in season_map.items()
    }
    fig_season = go.Figure(go.Pie(
        labels=list(season_totals.keys()),
        values=list(season_totals.values()),
        marker=dict(
            colors=[season_colors[s] for s in season_totals.keys()],
            line=dict(color='#ffffff', width=2)
        ),
        textinfo='label+percent',
        textfont=dict(color='#1a1a2e', size=13)
    ))
    fig_season.update_layout(**light_layout(height=280, title='توزيع الاستهلاك الموسمي', showlegend=False))
    st.plotly_chart(fig_season, use_container_width=True, key="season_pie")

# ══════════════════════════════════════════════
# تبويب 2: التحليل الإحصائي
# ══════════════════════════════════════════════
with tab2:
    st.markdown(section_header('تحليل', 'التحليل الإحصائي المتقدم'), unsafe_allow_html=True)

    dyn_yr = max(selected_years)
    region_ca = (
        df_f[df_f['Year'] == dyn_yr]
        .groupby('Region_Major')['Collective_CA']
        .nunique()
        .reset_index()
    )
    fig_rca = go.Figure(go.Bar(
        x=region_ca['Region_Major'],
        y=region_ca['Collective_CA'],
        marker=dict(
            color=[REGION_COLORS.get(r, '#6b7a8d') for r in region_ca['Region_Major']],
            line=dict(color='#ffffff', width=1)
        ),
        text=region_ca['Collective_CA'],
        textposition='outside',
        textfont=dict(color='#4a5568', size=13)
    ))
    fig_rca.update_layout(**light_layout(
        height=280,
        title=f'عدد الحسابات التجميعية بالمنطقة ({dyn_yr})',
        showlegend=False
    ))
    fig_rca.update_xaxes(**light_xaxis())
    fig_rca.update_yaxes(**light_yaxis())
    st.plotly_chart(fig_rca, use_container_width=True, key="rca_bar")

    # ── معدل النمو الشهري ──
    st.markdown(section_header('نمو', 'معدل النمو الشهري بين 2024 و2025'), unsafe_allow_html=True)

    growth_24 = df_f[df_f['Year'] == 2024].groupby('Month')['Consumption_kWh'].sum()
    growth_25 = df_f[df_f['Year'] == 2025].groupby('Month')['Consumption_kWh'].sum()
    common_months = sorted(set(growth_24.index) & set(growth_25.index))

    if common_months:
        growth_data = [
            {
                'month': m,
                'name': MONTH_NAMES[m],
                'pct': delta_pct(growth_25.get(m, 0), growth_24.get(m, 0))
            }
            for m in common_months
        ]
        for row_start in range(0, len(growth_data), 4):
            row_items = growth_data[row_start:row_start + 4]
            g_cols = st.columns(len(row_items))
            for i, item in enumerate(row_items):
                pct = item['pct']
                color = '#27ae60' if pct >= 0 else '#c0392b'
                arrow = '▲' if pct >= 0 else '▼'
                bg = '#f0fff4' if pct >= 0 else '#fff5f5'
                border = '#c3e6cb' if pct >= 0 else '#f5c6c2'
                with g_cols[i]:
                    st.markdown(f"""
                    <div style="background:{bg}; border:1px solid {border}; border-radius:10px;
                                padding:14px 10px; text-align:center; margin-bottom:8px;">
                        <div style="color:#6b7a8d; font-size:12px; font-weight:600; margin-bottom:6px;">
                            {item['name']}
                        </div>
                        <div style="color:{color}; font-size:22px; font-weight:800;">
                            {arrow} {abs(pct):.1f}%
                        </div>
                        <div style="color:#9aa5b4; font-size:11px; margin-top:3px;">معدل النمو</div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("لا توجد بيانات مشتركة بين 2024 و2025 في الفلاتر الحالية.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── أعلى وأدنى حسابات ──
    col_up, col_down = st.columns(2)

    with col_up:
        st.markdown(section_header('أعلى', f'أعلى 5 حسابات تجميعية استهلاكاً ({dyn_yr})'), unsafe_allow_html=True)
        top_ca = (
            df_f[df_f['Year'] == dyn_yr]
            .groupby('Collective_CA')
            .agg(Consumption=('Consumption_kWh', 'sum'), Bill=('Bill_Amount', 'sum'))
            .nlargest(5, 'Consumption')
            .reset_index()
        )
        fig_up = go.Figure(go.Bar(
            x=top_ca['Consumption'],
            y=top_ca['Collective_CA'],
            orientation='h',
            marker=dict(color='#c0392b', opacity=0.85),
            text=[f"{fmt_num(v)} | {fmt_num(b, 'SAR')}" for v, b in zip(top_ca['Consumption'], top_ca['Bill'])],
            textposition='outside',
            textfont=dict(color='#4a5568', size=11),
            hovertemplate='<b>حساب: %{y}</b><br>الاستهلاك: %{x:,.0f} kWh<extra></extra>'
        ))
        fig_up.update_layout(**light_layout(height=360, showlegend=False))
        fig_up.update_xaxes(**light_xaxis(tickformat=',.0f'))
        fig_up.update_yaxes(**light_yaxis(tickfont=dict(color='#1a1a2e', size=12), type='category', dtick=1))
        fig_up.update_layout(margin=dict(l=200))
        st.plotly_chart(fig_up, use_container_width=True, key="top_ca")

    with col_down:
        st.markdown(section_header('أدنى', f'أدنى 5 حسابات تجميعية استهلاكاً ({dyn_yr})'), unsafe_allow_html=True)
        bot_ca = (
            df_f[(df_f['Year'] == dyn_yr) & (df_f['Consumption_kWh'] > 0)]
            .groupby('Collective_CA')
            .agg(Consumption=('Consumption_kWh', 'sum'), Bill=('Bill_Amount', 'sum'))
            .nsmallest(5, 'Consumption')
            .reset_index()
        )
        fig_down = go.Figure(go.Bar(
            x=bot_ca['Consumption'],
            y=bot_ca['Collective_CA'],
            orientation='h',
            marker=dict(color='#27ae60', opacity=0.85),
            text=[f"{fmt_num(v)} | {fmt_num(b, 'SAR')}" for v, b in zip(bot_ca['Consumption'], bot_ca['Bill'])],
            textposition='outside',
            textfont=dict(color='#4a5568', size=11),
            hovertemplate='<b>حساب: %{y}</b><br>الاستهلاك: %{x:,.0f} kWh<extra></extra>'
        ))
        fig_down.update_layout(**light_layout(height=360, showlegend=False))
        fig_down.update_xaxes(**light_xaxis(tickformat=',.0f'))
        fig_down.update_yaxes(**light_yaxis(tickfont=dict(color='#1a1a2e', size=12), type='category', dtick=1))
        fig_down.update_layout(margin=dict(l=200))
        st.plotly_chart(fig_down, use_container_width=True, key="bot_ca")

# ══════════════════════════════════════════════
# تبويب 3: إدارة الأصول
# ══════════════════════════════════════════════
with tab3:
    st.markdown(section_header('أصول', 'إدارة الأصول والحسابات التجميعية'), unsafe_allow_html=True)

    asset_year = st.selectbox(
        "اختر السنة لعرض الحسابات التجميعية:",
        options=[2024, 2025, 2026],
        index=0,
        key="asset_year_select"
    )

    ca_for_year = sorted(df[df['Year'] == asset_year]['Collective_CA'].unique().tolist())

    st.markdown(
        f'<div class="info-banner">'
        f'عدد الحسابات التجميعية لسنة <b>{asset_year}</b>: '
        f'<b>{len(ca_for_year)}</b> حساب تجميعي'
        f'</div>',
        unsafe_allow_html=True
    )

    search_ca = st.selectbox(
        "اختر حسابًا تجميعيًا لعرض تفاصيله:",
        options=["اختر حسابًا..."] + ca_for_year,
        key="search_ca_select"
    )

    if search_ca != "اختر حسابًا...":
        ca_detail_all = df[df['Collective_CA'] == search_ca]
        ca_detail_yr  = ca_detail_all[ca_detail_all['Year'] == asset_year]

        ca_total_kwh     = ca_detail_all['Consumption_kWh'].sum()
        ca_total_sar     = ca_detail_all['Bill_Amount'].sum()
        ca_num_contracts = ca_detail_all['Contract_Account'].nunique()
        ca_avg_kwh       = ca_detail_all['Consumption_kWh'].mean()
        ca_region = ca_detail_all['Region_Major'].mode()[0] if len(ca_detail_all) > 0 else '-'
        ca_city = (
            ca_detail_all['Region_City'].mode()[0]
            if 'Region_City' in ca_detail_all.columns and len(ca_detail_all) > 0
            else '-'
        )

        d_col1, d_col2, d_col3, d_col4 = st.columns(4)
        with d_col1:
            st.markdown(kpi_card("إجمالي الاستهلاك", fmt_num(ca_total_kwh, 'kWh'), None, 'blue'), unsafe_allow_html=True)
        with d_col2:
            st.markdown(kpi_card("إجمالي المبلغ", fmt_num(ca_total_sar, 'SAR'), None, 'orange'), unsafe_allow_html=True)
        with d_col3:
            st.markdown(kpi_card("عدد العدادات", str(ca_num_contracts), None, 'purple'), unsafe_allow_html=True)
        with d_col4:
            st.markdown(kpi_card("متوسط الاستهلاك", fmt_num(ca_avg_kwh, 'kWh'), None, 'green'), unsafe_allow_html=True)

        st.markdown(f"""
        <div class="alert-card info" style="margin:10px 0 16px;">
            <div style="color:#2980b9; font-weight:700; font-size:14px;">الحساب: {search_ca}</div>
            <div style="color:#6b7a8d; font-size:12px; margin-top:4px;">
                المنطقة: {ca_region} | المدينة: {ca_city} | إجمالي العدادات: {ca_num_contracts}
            </div>
        </div>
        """, unsafe_allow_html=True)

        ca_monthly = ca_detail_all.groupby(['Year', 'Month']).agg(
            Consumption=('Consumption_kWh', 'sum'),
            Bill=('Bill_Amount', 'sum')
        ).reset_index()

        fig_ca_detail = go.Figure()
        for yr in sorted(ca_monthly['Year'].unique()):
            d = ca_monthly[ca_monthly['Year'] == yr].sort_values('Month')
            fig_ca_detail.add_trace(go.Scatter(
                x=d['Month'], y=d['Consumption'],
                name=str(yr), mode='lines+markers',
                line=dict(color=YEAR_COLORS.get(yr, '#888'), width=2.5),
                marker=dict(size=7),
                hovertemplate=f'{yr} | الشهر %{{x}}: %{{y:,.0f}} kWh<extra></extra>'
            ))
        fig_ca_detail.update_layout(**light_layout(
            height=300,
            title=f'الاستهلاك الشهري - حساب {search_ca}',
            showlegend=True
        ))
        fig_ca_detail.update_xaxes(**light_xaxis(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=[MONTH_NAMES[i] for i in range(1, 13)]
        ))
        fig_ca_detail.update_yaxes(**light_yaxis(tickformat=',.0f'))
        st.plotly_chart(fig_ca_detail, use_container_width=True, key="ca_detail_chart")

        # جدول العدادات التابعة
        st.markdown(section_header('عدادات', f'العدادات التابعة للحساب {search_ca} - سنة {asset_year}'), unsafe_allow_html=True)
        contracts_yr = (
            ca_detail_yr.groupby('Contract_Account')
            .agg(
                الاستهلاك_kWh=('Consumption_kWh', 'sum'),
                المبلغ_SAR=('Bill_Amount', 'sum'),
                عدد_الأشهر=('Month', 'nunique')
            )
            .sort_values('الاستهلاك_kWh', ascending=False)
            .reset_index()
        )
        contracts_yr.columns = ['رقم العداد', 'الاستهلاك (kWh)', 'المبلغ (SAR)', 'عدد الأشهر']
        st.dataframe(
            contracts_yr.style.format({
                'الاستهلاك (kWh)': '{:,.0f}',
                'المبلغ (SAR)': '{:,.2f}'
            }).background_gradient(subset=['الاستهلاك (kWh)'], cmap='Reds'),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.markdown(
            '<div class="info-banner">اختر حسابًا تجميعيًا من القائمة أعلاه لعرض تفاصيله وجميع عداداته.</div>',
            unsafe_allow_html=True
        )

    # ── مقارنة الحسابات التجميعية 2024 مقابل 2025 ──
    st.markdown(section_header('مقارنة', 'مقارنة الحسابات التجميعية: 2024 مقابل 2025'), unsafe_allow_html=True)

    ca_24_sum = df[df['Year'] == 2024].groupby(['Collective_CA', 'Region_Major'])['Consumption_kWh'].sum().reset_index()
    ca_25_sum = df[df['Year'] == 2025].groupby('Collective_CA')['Consumption_kWh'].sum().reset_index()
    ca_compare = ca_24_sum.merge(ca_25_sum, on='Collective_CA', suffixes=('_2024', '_2025'), how='outer').fillna(0)
    ca_compare['التغيير_%'] = ca_compare.apply(
        lambda r: delta_pct(r['Consumption_kWh_2025'], r['Consumption_kWh_2024']), axis=1
    ).round(1)
    ca_compare.columns = ['Collective_CA', 'المنطقة', 'استهلاك_2024', 'استهلاك_2025', 'التغيير_%']

    cmp_col1, cmp_col2 = st.columns([2, 1])
    with cmp_col1:
        st.dataframe(
            ca_compare.style.format({
                'استهلاك_2024': '{:,.0f}',
                'استهلاك_2025': '{:,.0f}',
                'التغيير_%': '{:+.1f}%'
            }).background_gradient(subset=['التغيير_%'], cmap='RdYlGn'),
            use_container_width=True,
            hide_index=True
        )
    with cmp_col2:
        region_share = df_f.groupby('Region_Major')['Consumption_kWh'].sum()
        region_pct = (region_share / region_share.sum() * 100).round(1)
        fig_share = go.Figure(go.Bar(
            x=region_pct.values,
            y=region_pct.index,
            orientation='h',
            marker=dict(
                color=[REGION_COLORS.get(r, '#888') for r in region_pct.index],
                line=dict(color='#ffffff', width=1)
            ),
            text=[f'{v:.1f}%' for v in region_pct.values],
            textposition='outside',
            textfont=dict(color='#4a5568', size=12)
        ))
        fig_share.update_layout(**light_layout(height=280, title='الحصة النسبية للمناطق', showlegend=False))
        fig_share.update_xaxes(**light_xaxis(ticksuffix='%'))
        fig_share.update_yaxes(**light_yaxis())
        st.plotly_chart(fig_share, use_container_width=True, key="region_share")

    # ── الحسابات المرشحة للمراجعة ──
    st.markdown(section_header('تنبيه', 'الحسابات المرشحة للمراجعة'), unsafe_allow_html=True)

    high_growth = ca_compare[ca_compare['التغيير_%'] > 50].sort_values('التغيير_%', ascending=False)
    high_drop   = ca_compare[ca_compare['التغيير_%'] < -30].sort_values('التغيير_%')

    alert_col1, alert_col2 = st.columns(2)
    with alert_col1:
        st.markdown('<div style="color:#e67e22; font-weight:700; font-size:14px; margin-bottom:8px;">⬆️ ارتفاع كبير (أكثر من 50%)</div>', unsafe_allow_html=True)
        for _, row in high_growth.iterrows():
            st.markdown(f"""
            <div class="alert-card warning">
                <div style="font-weight:700; font-size:13px;">حساب {row['Collective_CA']}</div>
                <div style="color:#7a7a8a; font-size:12px;">{row['المنطقة']} | {row['التغيير_%']:+.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

    with alert_col2:
        st.markdown('<div style="color:#c0392b; font-weight:700; font-size:14px; margin-bottom:8px;">⬇️ انخفاض كبير (أكثر من 30%)</div>', unsafe_allow_html=True)
        for _, row in high_drop.iterrows():
            st.markdown(f"""
            <div class="alert-card danger">
                <div style="font-weight:700; font-size:13px;">حساب {row['Collective_CA']}</div>
                <div style="color:#7a7a8a; font-size:12px;">{row['المنطقة']} | {row['التغيير_%']:+.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

    # ── حسابات استهلاك صفري مع فاتورة ──
    zero_cons_bill = df_f[
        (df_f['Consumption_kWh'] == 0) & (df_f['Bill_Amount'] > 0)
    ].groupby('Contract_Account').agg(
        فاتورة=('Bill_Amount', 'sum'),
        أشهر=('Month', 'nunique')
    ).reset_index()

    if len(zero_cons_bill) > 0:
        st.markdown('<div style="color:#8e44ad; font-weight:700; font-size:14px; margin:12px 0 8px;">⚠️ استهلاك صفري مع فاتورة</div>', unsafe_allow_html=True)
        for _, row in zero_cons_bill.iterrows():
            st.markdown(f"""
            <div class="alert-card" style="border-right:4px solid #8e44ad;">
                <div style="font-weight:700; font-size:13px;">حساب {row['Contract_Account']}</div>
                <div style="color:#7a7a8a; font-size:12px;">فاتورة: {row['فاتورة']:.2f} ريال | {row['أشهر']} أشهر</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# تبويب الجغرافي
# ══════════════════════════════════════════════
with tab_geo:
    st.markdown(section_header('جغرافي', 'التحليل الجغرافي حسب المنطقة'), unsafe_allow_html=True)

    region_geo = df_f.groupby('Region_Major').agg(
        Consumption=('Consumption_kWh', 'sum'),
        Bill=('Bill_Amount', 'sum'),
        Contracts=('Contract_Account', 'nunique'),
        CollectiveCAs=('Collective_CA', 'nunique')
    ).reset_index().sort_values('Consumption', ascending=False)

    geo_col1, geo_col2 = st.columns(2)
    with geo_col1:
        fig_geo_bar = go.Figure(go.Bar(
            x=region_geo['Region_Major'],
            y=region_geo['Consumption'],
            marker=dict(
                color=[REGION_COLORS.get(r, '#888') for r in region_geo['Region_Major']],
                line=dict(color='#ffffff', width=1)
            ),
            text=[fmt_num(v) for v in region_geo['Consumption']],
            textposition='outside',
            textfont=dict(color='#4a5568', size=12),
            hovertemplate='<b>%{x}</b><br>%{y:,.0f} kWh<extra></extra>'
        ))
        fig_geo_bar.update_layout(**light_layout(height=320, title='إجمالي الاستهلاك بالمنطقة', showlegend=False))
        fig_geo_bar.update_xaxes(**light_xaxis())
        fig_geo_bar.update_yaxes(**light_yaxis(tickformat=',.0f'))
        st.plotly_chart(fig_geo_bar, use_container_width=True, key="geo_bar")

    with geo_col2:
        fig_geo_pie = go.Figure(go.Pie(
            labels=region_geo['Region_Major'],
            values=region_geo['Consumption'],
            marker=dict(
                colors=[REGION_COLORS.get(r, '#888') for r in region_geo['Region_Major']],
                line=dict(color='#ffffff', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(color='#1a1a2e', size=13)
        ))
        fig_geo_pie.update_layout(**light_layout(height=320, title='نسبة الاستهلاك بالمنطقة', showlegend=False))
        st.plotly_chart(fig_geo_pie, use_container_width=True, key="geo_pie")

    # رسم الاستهلاك الشهري بالمنطقة
    st.markdown(section_header('شهري', 'الاستهلاك الشهري حسب المنطقة'), unsafe_allow_html=True)
    region_monthly = df_f.groupby(['Month', 'Region_Major'])['Consumption_kWh'].sum().reset_index()
    fig_reg_monthly = go.Figure()
    # ألوان وأشكال مميزة لكل منطقة
    REGION_DASH = {
        'الوسطى':   'solid',
        'الغربية':  'solid',
        'الشرقية':  'dash',
        'الشمالية': 'dot',
        'الجنوبية': 'dashdot',
    }
    REGION_SYMBOL = {
        'الوسطى':   'circle',
        'الغربية':  'square',
        'الشرقية':  'diamond',
        'الشمالية': 'triangle-up',
        'الجنوبية': 'cross',
    }
    for region in region_geo['Region_Major']:
        d = region_monthly[region_monthly['Region_Major'] == region].sort_values('Month')
        fig_reg_monthly.add_trace(go.Scatter(
            x=d['Month'], y=d['Consumption_kWh'],
            name=region, mode='lines+markers',
            line=dict(
                color=REGION_COLORS.get(region, '#888'),
                width=3.5,
                dash=REGION_DASH.get(region, 'solid')
            ),
            marker=dict(
                size=9,
                symbol=REGION_SYMBOL.get(region, 'circle'),
                color=REGION_COLORS.get(region, '#888'),
                line=dict(color='white', width=1.5)
            ),
            hovertemplate=f'<b>{region}</b><br>الشهر %{{x}}: %{{y:,.0f}} kWh<extra></extra>'
        ))
    _monthly_layout = light_layout(height=420, showlegend=True)
    _monthly_layout['legend'] = dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        bgcolor='rgba(255,255,255,0.95)',
        bordercolor='#ead8d8',
        borderwidth=1,
        font=dict(size=14, color='#1a1a2e')
    )
    fig_reg_monthly.update_layout(**_monthly_layout)
    fig_reg_monthly.update_xaxes(**light_xaxis(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=[MONTH_NAMES[i] for i in range(1, 13)],
        tickfont=dict(color='#1a1a2e', size=13)
    ))
    fig_reg_monthly.update_yaxes(**light_yaxis(
        tickformat=',.0f',
        tickfont=dict(color='#1a1a2e', size=13)
    ))
    st.plotly_chart(fig_reg_monthly, use_container_width=True, key="reg_monthly")

    # جدول ملخص المناطق
    st.markdown(section_header('ملخص', 'جدول ملخص المناطق'), unsafe_allow_html=True)
    region_tbl = region_geo.copy()
    region_tbl.columns = ['المنطقة', 'الاستهلاك (kWh)', 'المبلغ (SAR)', 'عدد الحسابات التعاقدية', 'عدد الحسابات التجميعية']
    region_tbl['نسبة الاستهلاك %'] = (
        region_tbl['الاستهلاك (kWh)'] / region_tbl['الاستهلاك (kWh)'].sum() * 100
    ).round(1)
    st.dataframe(
        region_tbl.style.format({
            'الاستهلاك (kWh)': '{:,.0f}',
            'المبلغ (SAR)': '{:,.2f}',
            'نسبة الاستهلاك %': '{:.1f}%'
        }).background_gradient(subset=['الاستهلاك (kWh)'], cmap='Reds'),
        use_container_width=True
    )

# ══════════════════════════════════════════════
# تبويب 4: توقعات 2026
# ══════════════════════════════════════════════
with tab4:
    st.markdown(section_header('توقعات', 'نموذج التنبؤ بالاستهلاك 2026'), unsafe_allow_html=True)

    pred_monthly = pred_df.groupby(['Month', 'Type'])['Predicted_Consumption'].sum().reset_index()
    actual_q1       = pred_monthly[pred_monthly['Type'] == 'فعلي']['Predicted_Consumption'].sum()
    predicted_q2_q4 = pred_monthly[pred_monthly['Type'] == 'متوقع']['Predicted_Consumption'].sum()
    total_2026      = actual_q1 + predicted_q2_q4

    q1_comp_agg = comp_df.groupby('Month').agg(
        فعلي=('Consumption_kWh', 'sum'),
        متوقع=('Predicted_Consumption', 'sum')
    ).reset_index()
    q1_accuracy = (
        100 - abs(q1_comp_agg['فعلي'].sum() - q1_comp_agg['متوقع'].sum())
        / q1_comp_agg['فعلي'].sum() * 100
        if q1_comp_agg['فعلي'].sum() > 0 else 0
    )

    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(kpi_card("Q1 2026 الفعلي", fmt_num(actual_q1), None, 'green'), unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(kpi_card("Q2-Q4 المتوقع", fmt_num(predicted_q2_q4), None, 'orange'), unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(kpi_card("إجمالي 2026 المتوقع", fmt_num(total_2026), None, 'blue'), unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(kpi_card("دقة النموذج Q1", f"{q1_accuracy:.1f}%", None, 'purple'), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── معلومات تدريب النموذج ──
    st.markdown(section_header('نموذج', 'معلومات تدريب النموذج'), unsafe_allow_html=True)

    if model_metrics:
        best_model_name = model_metrics.get('best_model', 'XGBoost')
        xgb_metrics = model_metrics.get('models', {}).get(best_model_name, {})
        r2_score = xgb_metrics.get('r2', 0.9475)
        rmse_val = xgb_metrics.get('rmse', 1733.8)
        mae_val  = xgb_metrics.get('mae', 590.7)
    else:
        best_model_name = 'XGBoost'
        r2_score = 0.9475
        rmse_val = 1733.8
        mae_val  = 590.7

    total_records_model = len(df)
    train_records = int(total_records_model * 0.80)
    test_records  = total_records_model - train_records

    avg_actual_kwh = df[df['Year'].isin([2024, 2025])]['Consumption_kWh'].mean()
    rmse_pct = (rmse_val / avg_actual_kwh * 100) if avg_actual_kwh > 0 else 0
    mae_pct  = (mae_val  / avg_actual_kwh * 100) if avg_actual_kwh > 0 else 0

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(f"""
        <div class="model-info-card">
            <h4>النموذج المستخدم</h4>
            <div class="model-value" style="color:#2980b9;">{best_model_name}</div>
            <div class="model-sub">أفضل نموذج من 3 خوارزميات</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
        <div class="model-info-card">
            <h4>دقة النموذج (R² Score)</h4>
            <div class="model-value" style="color:#27ae60;">{r2_score*100:.1f}%</div>
            <div class="model-sub">معامل التحديد — كلما اقترب من 100% كان النموذج أدق</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"""
        <div class="model-info-card">
            <h4>دقة التنبؤ Q1 2026</h4>
            <div class="model-value" style="color:#27ae60;">{q1_accuracy:.1f}%</div>
            <div class="model-sub">مقارنة بالاستهلاك الفعلي للربع الأول</div>
        </div>
        """, unsafe_allow_html=True)

    m_col4, m_col5, m_col6 = st.columns(3)
    with m_col4:
        st.markdown(f"""
        <div class="model-info-card">
            <h4>بيانات التدريب (80%)</h4>
            <div class="model-value" style="color:#e67e22;">{train_records:,}</div>
            <div class="model-sub">سجل استُخدم لتدريب النموذج</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col5:
        st.markdown(f"""
        <div class="model-info-card">
            <h4>بيانات الاختبار (20%)</h4>
            <div class="model-value" style="color:#c0392b;">{test_records:,}</div>
            <div class="model-sub">سجل استُخدم لاختبار دقة النموذج</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col6:
        st.markdown(f"""
        <div class="model-info-card">
            <h4>نسبة الخطأ المئوية (MAE%)</h4>
            <div class="model-value" style="color:#8e44ad;">{mae_pct:.1f}%</div>
            <div class="model-sub">متوسط الخطأ المطلق كنسبة من المتوسط الفعلي</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-explain-card">
        <h4>📘 شرح مقاييس الخطأ</h4>
        <p>
        <b>MAE (متوسط الخطأ المطلق)</b> = {mae_val:,.0f} كيلوواط/ساعة ({mae_pct:.1f}%)
        — يعني أن النموذج يُخطئ في المتوسط بمقدار {mae_val:,.0f} كيلوواط/ساعة لكل تنبؤ.
        <br><br>
        <b>RMSE (جذر متوسط مربع الخطأ)</b> = {rmse_val:,.0f} كيلوواط/ساعة ({rmse_pct:.1f}%)
        — يُعطي وزناً أكبر للأخطاء الكبيرة؛ كلما انخفض كان النموذج أكثر دقة واستقراراً.
        <br><br>
        <b>نسبة الخطأ المئوية</b> محسوبة بالنسبة لمتوسط الاستهلاك الفعلي ({avg_actual_kwh:,.0f} كيلوواط/ساعة).
        </p>
    </div>
    """.format(
        mae_val=mae_val, mae_pct=mae_pct,
        rmse_val=rmse_val, rmse_pct=rmse_pct,
        avg_actual_kwh=avg_actual_kwh
    ), unsafe_allow_html=True)

    if model_metrics and 'models' in model_metrics:
        with st.expander("📊 مقارنة أداء النماذج الثلاثة"):
            models_data = []
            for model_name, metrics in model_metrics['models'].items():
                models_data.append({
                    'النموذج': model_name,
                    'R² Score': f"{metrics.get('r2', 0)*100:.2f}%",
                    'RMSE': f"{metrics.get('rmse', 0):,.1f}",
                    'MAE': f"{metrics.get('mae', 0):,.1f}",
                    'الحالة': '✅ الأفضل' if model_name == best_model_name else '-'
                })
            st.dataframe(pd.DataFrame(models_data), use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── الاستهلاك الفعلي والمتوقع 2026 ──
    st.markdown(section_header('بياني', 'الاستهلاك الفعلي والمتوقع 2026'), unsafe_allow_html=True)

    forecast_monthly = pred_df.groupby(['Month', 'Type'])['Predicted_Consumption'].sum().reset_index()
    actual_part = forecast_monthly[forecast_monthly['Type'] == 'فعلي'].sort_values('Month')
    pred_part   = forecast_monthly[forecast_monthly['Type'] == 'متوقع'].sort_values('Month')

    hist_2024 = df[df['Year'] == 2024].groupby('Month')['Consumption_kWh'].sum().reset_index()
    hist_2025 = df[df['Year'] == 2025].groupby('Month')['Consumption_kWh'].sum().reset_index()

    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(
        x=hist_2024['Month'], y=hist_2024['Consumption_kWh'],
        name='2024 فعلي', mode='lines',
        line=dict(color='#2980b9', width=2, dash='dot'), opacity=0.7,
        hovertemplate='2024 | الشهر %{x}: %{y:,.0f}<extra></extra>'
    ))
    fig_forecast.add_trace(go.Scatter(
        x=hist_2025['Month'], y=hist_2025['Consumption_kWh'],
        name='2025 فعلي', mode='lines',
        line=dict(color='#27ae60', width=2, dash='dot'), opacity=0.7,
        hovertemplate='2025 | الشهر %{x}: %{y:,.0f}<extra></extra>'
    ))
    fig_forecast.add_trace(go.Scatter(
        x=actual_part['Month'], y=actual_part['Predicted_Consumption'],
        name='2026 فعلي (Q1)', mode='lines+markers',
        line=dict(color='#c0392b', width=3),
        marker=dict(size=9, symbol='circle'),
        hovertemplate='2026 فعلي | الشهر %{x}: %{y:,.0f}<extra></extra>'
    ))
    fig_forecast.add_trace(go.Scatter(
        x=pred_part['Month'], y=pred_part['Predicted_Consumption'],
        name='2026 متوقع', mode='lines+markers',
        line=dict(color='#c0392b', width=3, dash='dash'),
        marker=dict(size=9, symbol='diamond'),
        hovertemplate='2026 متوقع | الشهر %{x}: %{y:,.0f}<extra></extra>'
    ))
    fig_forecast.update_layout(**light_layout(height=380, showlegend=True))
    fig_forecast.update_xaxes(**light_xaxis(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=[MONTH_NAMES[i] for i in range(1, 13)]
    ))
    fig_forecast.update_yaxes(**light_yaxis(tickformat=',.0f'))
    st.plotly_chart(fig_forecast, use_container_width=True, key="forecast_main")

    # ── مقارنة Q1 ──
    if len(q1_comp_agg) > 0:
        st.markdown(section_header('Q1', 'مقارنة الربع الأول 2026: الفعلي مقابل المتوقع'), unsafe_allow_html=True)
        q1_col1, q1_col2 = st.columns(2)
        with q1_col1:
            fig_q1 = go.Figure()
            q1_comp_agg['Month_Name'] = q1_comp_agg['Month'].map(MONTH_NAMES)
            fig_q1.add_trace(go.Bar(
                x=q1_comp_agg['Month_Name'], y=q1_comp_agg['فعلي'],
                name='فعلي', marker=dict(color='#27ae60', opacity=0.85)
            ))
            fig_q1.add_trace(go.Bar(
                x=q1_comp_agg['Month_Name'], y=q1_comp_agg['متوقع'],
                name='متوقع', marker=dict(color='#2980b9', opacity=0.85)
            ))
            fig_q1.update_layout(**light_layout(height=300, showlegend=True, title='الفعلي مقابل المتوقع - Q1 2026'))
            fig_q1.update_layout(barmode='group')
            fig_q1.update_xaxes(**light_xaxis())
            fig_q1.update_yaxes(**light_yaxis(tickformat=',.0f'))
            st.plotly_chart(fig_q1, use_container_width=True, key="q1_comp")

        with q1_col2:
            q1_comp_agg['خطأ_%'] = (
                (q1_comp_agg['فعلي'] - q1_comp_agg['متوقع']) /
                q1_comp_agg['فعلي'].replace(0, np.nan) * 100
            ).round(1)
            err_colors = ['#27ae60' if e >= 0 else '#c0392b' for e in q1_comp_agg['خطأ_%'].fillna(0)]
            fig_err = go.Figure(go.Bar(
                x=q1_comp_agg['Month_Name'],
                y=q1_comp_agg['خطأ_%'],
                marker=dict(color=err_colors, line=dict(color='#ffffff', width=1)),
                text=[f'{e:+.1f}%' for e in q1_comp_agg['خطأ_%'].fillna(0)],
                textposition='outside',
                textfont=dict(color='#4a5568', size=12)
            ))
            fig_err.add_hline(y=0, line_color='#9aa5b4', line_width=1)
            fig_err.update_layout(**light_layout(height=300, title='نسبة الخطأ في التنبؤ (%)', showlegend=False))
            fig_err.update_xaxes(**light_xaxis())
            fig_err.update_yaxes(**light_yaxis(ticksuffix='%'))
            st.plotly_chart(fig_err, use_container_width=True, key="q1_err")

    # ── توقعات الأرباع ──
    st.markdown(section_header('أرباع', 'توقعات الأرباع 2026'), unsafe_allow_html=True)

    quarter_map = {
        1: 'Q1', 2: 'Q1', 3: 'Q1',
        4: 'Q2', 5: 'Q2', 6: 'Q2',
        7: 'Q3', 8: 'Q3', 9: 'Q3',
        10: 'Q4', 11: 'Q4', 12: 'Q4'
    }
    quarter_colors = {'Q1': '#27ae60', 'Q2': '#2980b9', 'Q3': '#c0392b', 'Q4': '#e67e22'}

    pred_df_copy = pred_df.copy()
    pred_df_copy['Quarter'] = pred_df_copy['Month'].map(quarter_map)
    q_summary = pred_df_copy.groupby(['Quarter', 'Type'])['Predicted_Consumption'].sum().reset_index()

    q_cols = st.columns(4)
    for i, q in enumerate(['Q1', 'Q2', 'Q3', 'Q4']):
        q_data  = q_summary[q_summary['Quarter'] == q]
        q_total = q_data['Predicted_Consumption'].sum()
        q_type  = q_data['Type'].iloc[0] if len(q_data) > 0 else 'متوقع'
        q_label = {'Q1': 'الربع الأول', 'Q2': 'الربع الثاني', 'Q3': 'الربع الثالث', 'Q4': 'الربع الرابع'}[q]
        q_color = quarter_colors[q]
        with q_cols[i]:
            st.markdown(f"""
            <div class="quarter-card">
                <h4>{q_label}</h4>
                <div class="q-value" style="color:{q_color};">{fmt_num(q_total)}</div>
                <div class="q-label">كيلوواط/ساعة</div>
                <div style="margin-top:8px;">
                    <span class="badge" style="background:{q_color}22; color:{q_color}; border:1px solid {q_color}44;">
                        {'فعلي' if q_type == 'فعلي' else 'متوقع'}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    q_chart_cols = st.columns(2)
    for idx, (q, q_color) in enumerate([('Q2', '#2980b9'), ('Q3', '#c0392b')]):
        q_months  = [m for m, qtr in quarter_map.items() if qtr == q]
        q_monthly = (
            pred_df_copy[pred_df_copy['Month'].isin(q_months)]
            .groupby('Month')['Predicted_Consumption']
            .sum()
            .reset_index()
        )
        q_monthly['Month_Name'] = q_monthly['Month'].map(MONTH_NAMES)
        r_c = int(q_color[1:3], 16)
        g_c = int(q_color[3:5], 16)
        b_c = int(q_color[5:7], 16)
        fig_q = go.Figure(go.Scatter(
            x=q_monthly['Month_Name'], y=q_monthly['Predicted_Consumption'],
            name='2026 متوقع', mode='lines+markers',
            line=dict(color=q_color, width=3),
            marker=dict(size=10, symbol='diamond'),
            fill='tozeroy',
            fillcolor=f'rgba({r_c},{g_c},{b_c},0.10)'
        ))
        q_label = {'Q2': 'الربع الثاني', 'Q3': 'الربع الثالث'}[q]
        fig_q.update_layout(**light_layout(height=280, title=f'توقعات {q_label} 2026', showlegend=False))
        fig_q.update_xaxes(**light_xaxis())
        fig_q.update_yaxes(**light_yaxis(tickformat=',.0f'))
        with q_chart_cols[idx]:
            st.plotly_chart(fig_q, use_container_width=True, key=f"q{idx+2}_chart")

    # ── ملخص التوقعات السنوية ──
    st.markdown(section_header('ملخص', 'ملخص التوقعات السنوية'), unsafe_allow_html=True)

    summary_data = {
        'السنة': ['2024 (فعلي)', '2025 (فعلي)', '2026 (متوقع)'],
        'الاستهلاك الكلي (كيلوواط)': [
            df[df['Year'] == 2024]['Consumption_kWh'].sum(),
            df[df['Year'] == 2025]['Consumption_kWh'].sum(),
            total_2026
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df['التغيير %'] = summary_df['الاستهلاك الكلي (كيلوواط)'].pct_change() * 100

    fig_summary = go.Figure(go.Bar(
        x=summary_df['السنة'],
        y=summary_df['الاستهلاك الكلي (كيلوواط)'],
        marker=dict(
            color=['#2980b9', '#27ae60', '#c0392b'],
            line=dict(color='#ffffff', width=2)
        ),
        text=[fmt_num(v) for v in summary_df['الاستهلاك الكلي (كيلوواط)']],
        textposition='outside',
        textfont=dict(color='#1a1a2e', size=14, family='Arial'),
        hovertemplate='%{x}<br>%{y:,.0f} كيلوواط<extra></extra>'
    ))
    fig_summary.update_layout(**light_layout(height=320, showlegend=False))
    fig_summary.update_xaxes(**light_xaxis())
    fig_summary.update_yaxes(**light_yaxis(tickformat=',.0f'))
    st.plotly_chart(fig_summary, use_container_width=True, key="summary_bar")

# ══════════════════════════════════════════════
# تبويب 5: الحسابات التجميعية الزائدة (جديد)
# ══════════════════════════════════════════════
with tab_excess:
    # ── حساب الحسابات الزائدة ──
    original_cas, extra_2024, extra_2025 = compute_extra_cas(df)

    # ── رأس القسم ──
    st.markdown(section_header('🔍 زائدة', 'تحليل الحسابات التجميعية الزائدة'), unsafe_allow_html=True)

    # ── شرح المنهجية ──
    st.markdown(f"""
    <div class="info-banner">
        <b>المنهجية:</b> الحسابات التجميعية الأصلية (الحقيقية) = <b>{ORIGINAL_CA_COUNT}</b> حساباً
        (الموجودة في بيانات 2026 Q1).
        الحسابات الزائدة هي الحسابات الموجودة في 2024 أو 2025 ولا تظهر في 2026،
        مما يشير إلى أنها قد تكون حسابات مكررة أو منتهية أو بحاجة للمراجعة.
    </div>
    """, unsafe_allow_html=True)

    # ── بطاقات KPI للحسابات الزائدة ──
    exc_col1, exc_col2, exc_col3 = st.columns(3)
    with exc_col1:
        st.markdown(f"""
        <div class="excess-count-card">
            <div class="ec-year">الحسابات الأصلية</div>
            <div class="ec-num" style="color:#27ae60;">{ORIGINAL_CA_COUNT}</div>
            <div class="ec-label">حساب تجميعي حقيقي</div>
        </div>
        """, unsafe_allow_html=True)
    with exc_col2:
        st.markdown(f"""
        <div class="excess-count-card">
            <div class="ec-year">زائدة في 2024</div>
            <div class="ec-num">{len(extra_2024)}</div>
            <div class="ec-label">من أصل {STATIC_CA_COUNTS[2024]} حساب</div>
        </div>
        """, unsafe_allow_html=True)
    with exc_col3:
        st.markdown(f"""
        <div class="excess-count-card">
            <div class="ec-year">زائدة في 2025</div>
            <div class="ec-num" style="color:#e67e22;">{len(extra_2025)}</div>
            <div class="ec-label">من أصل {STATIC_CA_COUNTS[2025]} حساب</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── فلتر السنة ──
    excess_year_filter = st.radio(
        "عرض الحسابات الزائدة لـ:",
        options=["الكل (2024 + 2025)", "2024 فقط", "2025 فقط"],
        horizontal=True,
        key="excess_year_filter"
    )

    # تحديد القائمة المعروضة
    if excess_year_filter == "2024 فقط":
        display_extras = [(ca, 2024) for ca in extra_2024]
    elif excess_year_filter == "2025 فقط":
        display_extras = [(ca, 2025) for ca in extra_2025]
    else:
        display_extras = [(ca, 2024) for ca in extra_2024] + [(ca, 2025) for ca in extra_2025]

    total_excess = len(display_extras)

    # ── جدول ملخص الحسابات الزائدة ──
    st.markdown(section_header('قائمة', f'قائمة الحسابات الزائدة ({total_excess} حساب)'), unsafe_allow_html=True)
    # ── فلتر الاستهلاك الصفري/المنخفض ──
    show_zero_filter = st.checkbox(
        "🔍 عرض الحسابات ذات الاستهلاك الصفري أو المنخفض فقط",
        value=False, key="zero_filter_cb"
    )
    if show_zero_filter:
        near_zero_threshold_input = st.number_input(
            "حد الاستهلاك المنخفض (kWh)",
            min_value=0.0, max_value=1000.0,
            value=float(NEAR_ZERO_THRESHOLD), step=0.1, key="near_zero_input"
        )
    else:
        near_zero_threshold_input = NEAR_ZERO_THRESHOLD

    # حساب إحصاءات التصنيف
    all_rows_for_stats = []
    for ca_id, yr in display_extras:
        info = get_ca_summary(df, ca_id, yr)
        if info:
            cls_label, _, _ = classify_consumption(info['total_kwh'])
            all_rows_for_stats.append(cls_label)
    zero_cnt = all_rows_for_stats.count('صفري')
    low_cnt  = all_rows_for_stats.count('منخفض جداً')
    real_cnt = all_rows_for_stats.count('حقيقي')

    # بطاقات تصنيف الاستهلاك
    cls_c1, cls_c2, cls_c3, cls_c4 = st.columns(4)
    with cls_c1:
        st.markdown(
            f'<div style="background:#ffebee;border:1px solid #ef9a9a;border-radius:8px;padding:10px;text-align:center;margin-bottom:12px;">'  
            f'<div style="font-size:22px;font-weight:800;color:#B71C1C;">{zero_cnt}</div>'
            f'<div style="font-size:12px;color:#7a7a8a;">🔴 استهلاك صفري</div>'
            f'<div style="font-size:11px;color:#B71C1C;margin-top:4px;">مرشح للحذف الفوري</div></div>',
            unsafe_allow_html=True)
    with cls_c2:
        st.markdown(
            f'<div style="background:#fff3e0;border:1px solid #ffcc80;border-radius:8px;padding:10px;text-align:center;margin-bottom:12px;">'
            f'<div style="font-size:22px;font-weight:800;color:#E65100;">{low_cnt}</div>'
            f'<div style="font-size:12px;color:#7a7a8a;">🟠 منخفض جداً (≤{NEAR_ZERO_THRESHOLD} kWh)</div>'
            f'<div style="font-size:11px;color:#E65100;margin-top:4px;">يحتاج مراجعة</div></div>',
            unsafe_allow_html=True)
    with cls_c3:
        st.markdown(
            f'<div style="background:#e8f5e9;border:1px solid #a5d6a7;border-radius:8px;padding:10px;text-align:center;margin-bottom:12px;">'
            f'<div style="font-size:22px;font-weight:800;color:#2E7D32;">{real_cnt}</div>'
            f'<div style="font-size:12px;color:#7a7a8a;">🟢 استهلاك حقيقي</div>'
            f'<div style="font-size:11px;color:#2E7D32;margin-top:4px;">يحتاج تحقق من السبب</div></div>',
            unsafe_allow_html=True)
    with cls_c4:
        st.markdown(
            f'<div style="background:#f3e5f5;border:1px solid #ce93d8;border-radius:8px;padding:10px;text-align:center;margin-bottom:12px;">'
            f'<div style="font-size:22px;font-weight:800;color:#6A1B9A;">{zero_cnt + low_cnt}</div>'
            f'<div style="font-size:12px;color:#7a7a8a;">⚡ مرشح للإلغاء</div>'
            f'<div style="font-size:11px;color:#6A1B9A;margin-top:4px;">صفري + منخفض جداً</div></div>',
            unsafe_allow_html=True)

    # بناء جدول ملخص مع التصنيف
    summary_rows = []
    for ca_id, yr in display_extras:
        info = get_ca_summary(df, ca_id, yr)
        if info:
            cls_label, cls_color, cls_icon = classify_consumption(info['total_kwh'])
            if show_zero_filter and info['total_kwh'] > near_zero_threshold_input:
                continue
            summary_rows.append({
                'الحساب التجميعي': ca_id,
                'السنة': yr,
                'المنطقة': info['region'],
                'المدينة': info['city'],
                'عدد العدادات': info['n_contracts'],
                'الاستهلاك (kWh)': info['total_kwh'],
                'المبلغ (SAR)': info['total_sar'],
                'عدد الأشهر': info['n_months'],
                'تصنيف الاستهلاك': f"{cls_icon} {cls_label}"
            })
    if summary_rows:
        summary_excess_df = pd.DataFrame(summary_rows)
        st.dataframe(
            summary_excess_df.style.format({
                'الاستهلاك (kWh)': '{:,.1f}',
                'المبلغ (SAR)': '{:,.2f}'
            }).background_gradient(subset=['الاستهلاك (kWh)'], cmap='RdYlGn'),
            use_container_width=True,
            hide_index=True
        )
        # ── رسم توزيع الحسابات الزائدة بالمنطقة ──
        region_excess = summary_excess_df.groupby('المنطقة').agg(
            عدد=('الحساب التجميعي', 'count'),
            استهلاك=('الاستهلاك (kWh)', 'sum')
        ).reset_index()

        exc_chart_col1, exc_chart_col2 = st.columns(2)
        with exc_chart_col1:
            fig_exc_reg = go.Figure(go.Bar(
                x=region_excess['المنطقة'],
                y=region_excess['عدد'],
                marker=dict(
                    color=[REGION_COLORS.get(r, '#c0392b') for r in region_excess['المنطقة']],
                    line=dict(color='#ffffff', width=1)
                ),
                text=region_excess['عدد'],
                textposition='outside',
                textfont=dict(color='#4a5568', size=13)
            ))
            fig_exc_reg.update_layout(**light_layout(height=280, title='توزيع الحسابات الزائدة بالمنطقة', showlegend=False))
            fig_exc_reg.update_xaxes(**light_xaxis())
            fig_exc_reg.update_yaxes(**light_yaxis())
            st.plotly_chart(fig_exc_reg, use_container_width=True, key="exc_region_bar")

        with exc_chart_col2:
            fig_exc_kwh = go.Figure(go.Bar(
                x=region_excess['المنطقة'],
                y=region_excess['استهلاك'],
                marker=dict(
                    color=[REGION_COLORS.get(r, '#c0392b') for r in region_excess['المنطقة']],
                    opacity=0.8,
                    line=dict(color='#ffffff', width=1)
                ),
                text=[fmt_num(v) for v in region_excess['استهلاك']],
                textposition='outside',
                textfont=dict(color='#4a5568', size=12)
            ))
            fig_exc_kwh.update_layout(**light_layout(height=280, title='استهلاك الحسابات الزائدة بالمنطقة (kWh)', showlegend=False))
            fig_exc_kwh.update_xaxes(**light_xaxis())
            fig_exc_kwh.update_yaxes(**light_yaxis(tickformat=',.0f'))
            st.plotly_chart(fig_exc_kwh, use_container_width=True, key="exc_kwh_bar")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── تفاصيل حساب زائد محدد ──
    st.markdown(section_header('تفاصيل', 'تفاصيل حساب تجميعي زائد'), unsafe_allow_html=True)

    # فلتر السنة للتفاصيل
    detail_year_sel = st.selectbox(
        "اختر السنة:",
        options=[2024, 2025],
        key="excess_detail_year"
    )
    excess_list_for_year = extra_2024 if detail_year_sel == 2024 else extra_2025

    selected_excess_ca = st.selectbox(
        f"اختر حساباً زائداً من سنة {detail_year_sel}:",
        options=["اختر حساباً..."] + excess_list_for_year,
        key="excess_ca_select"
    )

    if selected_excess_ca != "اختر حساباً...":
        info = get_ca_summary(df, selected_excess_ca, detail_year_sel)

        if info:
            # بطاقات KPI للحساب الزائد
            exc_d1, exc_d2, exc_d3, exc_d4 = st.columns(4)
            with exc_d1:
                st.markdown(kpi_card("إجمالي الاستهلاك", fmt_num(info['total_kwh'], 'kWh'), None, 'red'), unsafe_allow_html=True)
            with exc_d2:
                st.markdown(kpi_card("إجمالي المبلغ", fmt_num(info['total_sar'], 'SAR'), None, 'orange'), unsafe_allow_html=True)
            with exc_d3:
                st.markdown(kpi_card("عدد العدادات", str(info['n_contracts']), None, 'purple'), unsafe_allow_html=True)
            with exc_d4:
                st.markdown(kpi_card("عدد الأشهر", str(info['n_months']), None, 'blue'), unsafe_allow_html=True)

            # معلومات الحساب
            st.markdown(f"""
            <div class="extra-ca-card">
                <div class="extra-ca-title">🔴 حساب تجميعي زائد: {selected_excess_ca}</div>
                <div class="extra-ca-meta">
                    المنطقة: {info['region']} &nbsp;|&nbsp;
                    المدينة: {info['city']} &nbsp;|&nbsp;
                    السنة: {detail_year_sel} &nbsp;|&nbsp;
                    الحالة: <b style="color:#c0392b;">غير موجود في 2026</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # رسم الاستهلاك الشهري
            ca_monthly_exc = (
                df[(df['Collective_CA'] == selected_excess_ca) & (df['Year'] == detail_year_sel)]
                .groupby('Month')['Consumption_kWh']
                .sum()
                .reset_index()
                .sort_values('Month')
            )
            if len(ca_monthly_exc) > 0:
                ca_monthly_exc['Month_Name'] = ca_monthly_exc['Month'].map(MONTH_NAMES)
                fig_exc_detail = go.Figure(go.Bar(
                    x=ca_monthly_exc['Month_Name'],
                    y=ca_monthly_exc['Consumption_kWh'],
                    marker=dict(color='#c0392b', opacity=0.80, line=dict(color='#ffffff', width=1)),
                    text=[fmt_num(v) for v in ca_monthly_exc['Consumption_kWh']],
                    textposition='outside',
                    textfont=dict(color='#4a5568', size=12),
                    hovertemplate='%{x}: %{y:,.0f} kWh<extra></extra>'
                ))
                fig_exc_detail.update_layout(**light_layout(
                    height=280,
                    title=f'الاستهلاك الشهري - حساب {selected_excess_ca} ({detail_year_sel})',
                    showlegend=False
                ))
                fig_exc_detail.update_xaxes(**light_xaxis())
                fig_exc_detail.update_yaxes(**light_yaxis(tickformat=',.0f'))
                st.plotly_chart(fig_exc_detail, use_container_width=True, key="exc_detail_chart")

            # جدول العدادات التابعة
            st.markdown(
                section_header('عدادات', f'العدادات التابعة للحساب الزائد {selected_excess_ca}'),
                unsafe_allow_html=True
            )
            contracts_exc = (
                df[(df['Collective_CA'] == selected_excess_ca) & (df['Year'] == detail_year_sel)]
                .groupby('Contract_Account')
                .agg(
                    الاستهلاك_kWh=('Consumption_kWh', 'sum'),
                    المبلغ_SAR=('Bill_Amount', 'sum'),
                    عدد_الأشهر=('Month', 'nunique'),
                    المنطقة=('Region_Major', 'first'),
                    المدينة=('Region_City', 'first') if 'Region_City' in df.columns else ('Region_Major', 'first')
                )
                .sort_values('الاستهلاك_kWh', ascending=False)
                .reset_index()
            )
            contracts_exc.columns = ['رقم العداد', 'الاستهلاك (kWh)', 'المبلغ (SAR)', 'عدد الأشهر', 'المنطقة', 'المدينة']

            st.dataframe(
                contracts_exc.style.format({
                    'الاستهلاك (kWh)': '{:,.0f}',
                    'المبلغ (SAR)': '{:,.2f}'
                }).background_gradient(subset=['الاستهلاك (kWh)'], cmap='Reds'),
                use_container_width=True,
                hide_index=True
            )

            # ملخص قرار
            total_exc_kwh = info['total_kwh']
            total_exc_sar = info['total_sar']
            st.markdown(f"""
            <div class="alert-card danger" style="margin-top:16px;">
                <div style="color:#c0392b; font-weight:700; font-size:14px; margin-bottom:6px;">
                    📋 ملخص القرار المقترح
                </div>
                <div style="color:#4a5568; font-size:13px; line-height:1.8;">
                    • الحساب <b>{selected_excess_ca}</b> موجود في بيانات <b>{detail_year_sel}</b> فقط ولا يظهر في 2026.<br>
                    • يضم <b>{info['n_contracts']}</b> عداد(ات) فرعية في منطقة <b>{info['region']}</b>.<br>
                    • إجمالي الاستهلاك: <b>{fmt_num(total_exc_kwh)} kWh</b> | إجمالي الفواتير: <b>{fmt_num(total_exc_sar)} SAR</b>.<br>
                    • <b>التوصية:</b> مراجعة هذا الحساب والتحقق من صحة تصنيفه قبل اتخاذ قرار الإلغاء.
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="info-banner">اختر حساباً تجميعياً زائداً من القائمة أعلاه لعرض تفاصيله وعداداته.</div>',
            unsafe_allow_html=True
        )

    # ── عرض موحد: جميع الحسابات الزائدة ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(section_header('موحد', 'عرض موحد: جميع الحسابات الزائدة (2024 + 2025)'), unsafe_allow_html=True)

    all_excess_rows = []
    for ca_id in extra_2024:
        info = get_ca_summary(df, ca_id, 2024)
        if info:
            all_excess_rows.append({
                'الحساب التجميعي': ca_id,
                'السنة': 2024,
                'المنطقة': info['region'],
                'عدد العدادات': info['n_contracts'],
                'الاستهلاك (kWh)': info['total_kwh'],
                'المبلغ (SAR)': info['total_sar'],
                'عدد الأشهر': info['n_months'],
                'الحالة': '🔴 زائد في 2024'
            })
    for ca_id in extra_2025:
        info = get_ca_summary(df, ca_id, 2025)
        if info:
            all_excess_rows.append({
                'الحساب التجميعي': ca_id,
                'السنة': 2025,
                'المنطقة': info['region'],
                'عدد العدادات': info['n_contracts'],
                'الاستهلاك (kWh)': info['total_kwh'],
                'المبلغ (SAR)': info['total_sar'],
                'عدد الأشهر': info['n_months'],
                'الحالة': '🟠 زائد في 2025'
            })

    if all_excess_rows:
        all_excess_df = pd.DataFrame(all_excess_rows)
        st.dataframe(
            all_excess_df.style.format({
                'الاستهلاك (kWh)': '{:,.0f}',
                'المبلغ (SAR)': '{:,.2f}'
            }).background_gradient(subset=['الاستهلاك (kWh)'], cmap='Reds'),
            use_container_width=True,
            hide_index=True,
            height=400
        )

        # إجماليات
        total_exc_all_kwh = all_excess_df['الاستهلاك (kWh)'].sum()
        total_exc_all_sar = all_excess_df['المبلغ (SAR)'].sum()
        total_exc_meters  = all_excess_df['عدد العدادات'].sum()

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#fff5f5,#fde8e6); border:1px solid #f5c6c2;
                    border-radius:12px; padding:16px 20px; margin-top:12px;">
            <div style="color:#8b0000; font-weight:700; font-size:15px; margin-bottom:10px;">
                📊 إجماليات الحسابات الزائدة
            </div>
            <div style="display:flex; gap:30px; flex-wrap:wrap;">
                <div style="text-align:center;">
                    <div style="color:#c0392b; font-size:28px; font-weight:800;">{len(all_excess_rows)}</div>
                    <div style="color:#7a7a8a; font-size:12px;">حساب تجميعي زائد</div>
                </div>
                <div style="text-align:center;">
                    <div style="color:#e67e22; font-size:28px; font-weight:800;">{total_exc_meters}</div>
                    <div style="color:#7a7a8a; font-size:12px;">عداد فرعي إجمالي</div>
                </div>
                <div style="text-align:center;">
                    <div style="color:#2980b9; font-size:28px; font-weight:800;">{fmt_num(total_exc_all_kwh)}</div>
                    <div style="color:#7a7a8a; font-size:12px;">إجمالي الاستهلاك (kWh)</div>
                </div>
                <div style="text-align:center;">
                    <div style="color:#27ae60; font-size:28px; font-weight:800;">{fmt_num(total_exc_all_sar)}</div>
                    <div style="color:#7a7a8a; font-size:12px;">إجمالي الفواتير (SAR)</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# تذييل الصفحة
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ⚡ تحليل استهلاك الكهرباء | هيئة الهلال الأحمر السعودي | أبريل 2026
</div>
""", unsafe_allow_html=True)

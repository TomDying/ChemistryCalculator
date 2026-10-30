
import streamlit as st
import periodictable as pt
import streamlit.components.v1 as components
from pathlib import Path

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Chemistry Calculator Hub",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# COLOURS
# ==========================================================

BG = "#141B2D"
CARD = "#1E293B"
TEXT = "#FFFFFF"
SECONDARY = "#94A3B8"
GREEN = "#22C55E"

ELEMENT_COLOURS = {
    "alkali metal": "#EF4444",
    "alkaline earth metal": "#F97316",
    "transition metal": "#EAB308",
    "post-transition metal": "#22C55E",
    "metalloid": "#14B8A6",
    "nonmetal": "#3B82F6",
    "halogen": "#8B5CF6",
    "noble gas": "#EC4899",
    "lanthanide": "#A855F7",
    "actinide": "#D946EF",
    "unknown": "#64748B"
}

# ==========================================================
# ELEMENT DATA
# ==========================================================

ELEMENTS = {
    element.symbol: element
    for element in pt.elements
    if element.number > 0
}

ELEMENT_CATEGORIES = {

    "alkali metal": [
        "Li", "Na", "K", "Rb", "Cs", "Fr"
    ],

    "alkaline earth metal": [
        "Be", "Mg", "Ca", "Sr", "Ba", "Ra"
    ],

    "transition metal": [
        "Sc", "Ti", "V", "Cr", "Mn", "Fe",
        "Co", "Ni", "Cu", "Zn", "Y", "Zr",
        "Nb", "Mo", "Tc", "Ru", "Rh", "Pd",
        "Ag", "Cd", "Hf", "Ta", "W", "Re",
        "Os", "Ir", "Pt", "Au", "Hg", "Rf",
        "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
        "Rg", "Cn"
    ],

    "post-transition metal": [
        "Al", "Ga", "In", "Sn", "Tl", "Pb",
        "Bi", "Po", "Nh", "Fl", "Mc", "Lv"
    ],

    "metalloid": [
        "B", "Si", "Ge", "As", "Sb", "Te"
    ],

    "nonmetal": [
        "H", "C", "N", "O", "P", "S", "Se"
    ],

    "halogen": [
        "F", "Cl", "Br", "I", "At", "Ts"
    ],

    "noble gas": [
        "He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"
    ],

    "lanthanide": [
        "La", "Ce", "Pr", "Nd", "Pm", "Sm",
        "Eu", "Gd", "Tb", "Dy", "Ho", "Er",
        "Tm", "Yb", "Lu"
    ],

    "actinide": [
        "Ac", "Th", "Pa", "U", "Np", "Pu",
        "Am", "Cm", "Bk", "Cf", "Es", "Fm",
        "Md", "No", "Lr"
    ]
}


def get_category(symbol):

    for category, symbols in ELEMENT_CATEGORIES.items():

        if symbol in symbols:
            return category

    return "unknown"


# ==========================================================
# PERIODIC TABLE LAYOUT
# ==========================================================

PERIODIC_ROWS = [

    ["H"] + [""] * 16 + ["He"],

    ["Li", "Be"] + [""] * 10 +
    ["B", "C", "N", "O", "F", "Ne"],

    ["Na", "Mg"] + [""] * 10 +
    ["Al", "Si", "P", "S", "Cl", "Ar"],

    ["K", "Ca", "Sc", "Ti", "V", "Cr",
     "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
     "Ga", "Ge", "As", "Se", "Br", "Kr"],

    ["Rb", "Sr", "Y", "Zr", "Nb", "Mo",
     "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
     "In", "Sn", "Sb", "Te", "I", "Xe"],

    ["Cs", "Ba", "", "Hf", "Ta", "W",
     "Re", "Os", "Ir", "Pt", "Au", "Hg",
     "Tl", "Pb", "Bi", "Po", "At", "Rn"],

    ["Fr", "Ra", "", "Rf", "Db", "Sg",
     "Bh", "Hs", "Mt", "Ds", "Rg", "Cn",
     "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]

]

LANTHANIDES = ELEMENT_CATEGORIES["lanthanide"]
ACTINIDES = ELEMENT_CATEGORIES["actinide"]

# ==========================================================
# SESSION STATE
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_element" not in st.session_state:
    st.session_state.selected_element = None

if "compound" not in st.session_state:
    st.session_state.compound = []


def navigate(page):

    st.session_state.page = page
    st.session_state.selected_element = None
    st.rerun()


def back_button():

    st.divider()

    if st.button(
        "← Back to Home",
        use_container_width=True
    ):

        navigate("home")

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.stApp {
    background-color: #141B2D;
    color: #FFFFFF;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

h1, h2, h3 {
    color: #FFFFFF !important;
}

p, label {
    color: #FFFFFF;
}

div.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    transition: 0.2s;
}

div.stButton > button:hover {
    border-color: #22C55E;
    color: #22C55E;
}

.calculator-card {
    background-color: #1E293B;
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 15px;
    border: 1px solid #334155;
}

.result-card {
    background-color: #1E293B;
    border-left: 5px solid #22C55E;
    padding: 20px;
    border-radius: 10px;
    margin-top: 15px;
}

.element-info {
    background-color: #1E293B;
    border: 2px solid #3B82F6;
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
}

[data-testid="stMetricValue"] {
    color: #22C55E;
}

footer {
    visibility: hidden;
}

@media (max-width: 768px) {

    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    h1 {
        font-size: 1.8rem !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# INTERACTIVE PERIODIC TABLE COMPONENT
# ==========================================================

periodic_component = components.declare_component(
    "chemistry_periodic_table",
    path=str(
        Path(__file__).parent / "periodic_component"
    )
)


def display_periodic_table():

    element_data = {}

    for symbol, element in ELEMENTS.items():

        category = get_category(symbol)

        density = getattr(element, "density", None)

        try:
            density_text = (
                f"{density:.4g} g/cm³"
                if density is not None
                else "Not available"
            )
        except (TypeError, ValueError):
            density_text = "Not available"

        element_data[symbol] = {
            "symbol": symbol,
            "name": element.name.capitalize(),
            "number": element.number,
            "mass": f"{element.mass:.4f}",
            "category": category.title(),
            "density": density_text,
            "colour": ELEMENT_COLOURS[category]
        }

    data = {
        "elements": element_data,
        "rows": PERIODIC_ROWS,
        "lanthanides": LANTHANIDES,
        "actinides": ACTINIDES
    }

    selected = periodic_component(
        data=data,
        selected=st.session_state.selected_element,
        key="periodic_table_component"
    )

    if selected and selected in ELEMENTS:

        st.session_state.selected_element = selected


# ==========================================================
# ELEMENT INFORMATION
# ==========================================================

def show_element_info(symbol):

    element = ELEMENTS[symbol]

    category = get_category(symbol)

    density = getattr(element, "density", None)

    if density is not None:

        try:
            density_text = f"{density:.4g} g/cm³"

        except (TypeError, ValueError):
            density_text = "Not available"

    else:
        density_text = "Not available"

    st.markdown(
        f"""
        <div class="element-info">

        <h2 style="color:#22C55E;">
        {element.name.capitalize()} ({symbol})
        </h2>

        <p><b>Atomic Number:</b> {element.number}</p>

        <p><b>Symbol:</b> {symbol}</p>

        <p><b>Atomic Mass:</b> {element.mass:.4f} g/mol</p>

        <p><b>Category:</b> {category.title()}</p>

        <p><b>Density:</b> {density_text}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    quantity = st.number_input(
        "Number of atoms",
        min_value=1,
        max_value=100000,
        value=1,
        step=1,
        key=f"quantity_{symbol}"
    )

    if st.button(
        "+ Add to Compound",
        key=f"add_{symbol}",
        use_container_width=True
    ):

        st.session_state.compound.append({
            "symbol": symbol,
            "count": quantity
        })

        st.success(
            f"Added {quantity} × {symbol} to your compound!"
        )

        st.rerun()

# ==========================================================
# PERIODIC TABLE PAGE
# ==========================================================

def periodic_table():

    st.title("🔬 Periodic Table")

    st.caption(
        "Hover over an element to see its properties. "
        "Click an element to select it."
    )

    st.divider()

    st.subheader("All Elements")

    # Interactive periodic table
    display_periodic_table()

    st.caption(
        "Scroll horizontally on smaller screens "
        "to explore the complete periodic table."
    )

    # COLOUR LEGEND

    st.divider()

    st.subheader("Element Categories")

    legend_items = list(ELEMENT_COLOURS.items())

    for start in range(0, len(legend_items), 3):

        cols = st.columns(3)

        for index, (category, colour) in enumerate(
            legend_items[start:start + 3]
        ):

            with cols[index]:

                st.markdown(
                    f"""
                    <p style="font-size:13px;">
                    <span style="color:{colour};">●</span>
                    {category.title()}
                    </p>
                    """,
                    unsafe_allow_html=True
                )

    # ELEMENT INFORMATION

    st.divider()

    if st.session_state.selected_element:

        st.subheader("Selected Element")

        show_element_info(
            st.session_state.selected_element
        )

    else:

        st.info(
            "Click an element in the periodic table "
            "to view its information."
        )

    # COMPOUND BUILDER

    st.divider()

    st.header("Your Compound")

    if not st.session_state.compound:

        st.info("You haven't added any elements yet.")

    else:

        total_mass = 0

        for index, item in enumerate(
            st.session_state.compound
        ):

            symbol = item["symbol"]
            count = item["count"]
            element = ELEMENTS[symbol]

            contribution = element.mass * count
            total_mass += contribution

            col1, col2 = st.columns([4, 1])

            with col1:

                st.markdown(
                    f"**{symbol} – "
                    f"{element.name.capitalize()}** × {count}"
                )

                st.caption(
                    f"{count} × {element.mass:.4f} "
                    f"= {contribution:.4f} g/mol"
                )

            with col2:

                if st.button(
                    "Remove",
                    key=f"remove_{index}",
                    use_container_width=True
                ):

                    st.session_state.compound.pop(index)
                    st.rerun()

        st.markdown(
            f"""
            <div class="result-card">

            <h3>Calculated Molar Mass</h3>

            <h1 style="color:#22C55E;">
            {total_mass:.4f} g/mol
            </h1>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Clear All Elements",
            type="secondary",
            use_container_width=True
        ):

            st.session_state.compound = []
            st.rerun()


    back_button()


# ==========================================================
# HOME SCREEN
# ==========================================================

def home():

    st.title("⚗️ Chemistry Calculator Hub")

    st.markdown(
        '<p style="color:#94A3B8;">'
        'Your chemistry tools, all in one place.'
        '</p>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("## 🔬 Periodic Table")

            st.markdown(
                "Explore all 118 elements, view their properties "
                "and calculate the molar mass of compounds."
            )

            st.markdown(
                '<p style="color:#22C55E;">'
                'Including Molar Mass Calculator'
                '</p>',
                unsafe_allow_html=True
            )

            if st.button(
                "Open Periodic Table →",
                key="home_periodic",
                use_container_width=True
            ):

                navigate("periodic")

    with col2:

        with st.container(border=True):

            st.markdown("## ⚗️ Moles Calculator")

            st.markdown(
                "Calculate moles, mass and molar mass "
                "using interchangeable equations."
            )

            if st.button(
                "Open Moles Calculator →",
                key="home_moles",
                use_container_width=True
            ):

                navigate("moles")

    col3, col4 = st.columns(2)

    with col3:

        with st.container(border=True):

            st.markdown("## 🧪 Concentration Calculator")

            st.markdown(
                "Calculate concentration, moles and volume "
                "using different rearrangements of the equation."
            )

            if st.button(
                "Open Concentration Calculator →",
                key="home_concentration",
                use_container_width=True
            ):

                navigate("concentration")

    with col4:

        with st.container(border=True):

            st.markdown("## 📚 Chemistry Tools")

            st.markdown(
                "More chemistry calculators can be added here "
                "in future updates."
            )

            st.caption("Additional features coming soon.")


# ==========================================================
# MOLES CALCULATOR
# ==========================================================

def moles_calculator():

    st.title("⚗️ Moles Calculator")

    st.caption("Calculate mass, moles or molar mass.")

    st.divider()

    target = st.selectbox(
        "What would you like to calculate?",
        ["Number of moles", "Mass", "Molar mass"]
    )

    st.markdown("### Enter your known values")

    if target == "Number of moles":

        mass = st.number_input(
            "Mass (g)", min_value=0.0,
            value=0.0, step=0.1
        )

        molar_mass = st.number_input(
            "Molar mass (g/mol)", min_value=0.0,
            value=0.0, step=0.1
        )

        if st.button("Calculate", use_container_width=True):

            if molar_mass == 0:
                st.error("Molar mass cannot be zero.")
            else:
                answer = mass / molar_mass

                st.success(
                    f"Number of moles = {answer:.6g} mol"
                )

                st.latex(r"n = \frac{m}{M}")

    elif target == "Mass":

        moles = st.number_input(
            "Number of moles (mol)",
            min_value=0.0, value=0.0, step=0.1
        )

        molar_mass = st.number_input(
            "Molar mass (g/mol)",
            min_value=0.0, value=0.0, step=0.1
        )

        if st.button("Calculate", use_container_width=True):

            answer = moles * molar_mass

            st.success(f"Mass = {answer:.6g} g")

            st.latex(r"m = n \times M")

    else:

        mass = st.number_input(
            "Mass (g)", min_value=0.0,
            value=0.0, step=0.1
        )

        moles = st.number_input(
            "Number of moles (mol)",
            min_value=0.0, value=0.0, step=0.1
        )

        if st.button("Calculate", use_container_width=True):

            if moles == 0:
                st.error("Number of moles cannot be zero.")
            else:
                answer = mass / moles

                st.success(
                    f"Molar mass = {answer:.6g} g/mol"
                )

                st.latex(r"M = \frac{m}{n}")

    back_button()


# ==========================================================
# CONCENTRATION CALCULATOR
# ==========================================================

def concentration_calculator():

    st.title("🧪 Concentration Calculator")

    st.caption("Calculate concentration, moles or volume.")

    st.divider()

    target = st.selectbox(
        "What would you like to calculate?",
        ["Concentration", "Number of moles", "Volume"]
    )

    volume_unit = st.selectbox(
        "Volume unit",
        ["dm³", "cm³"]
    )

    st.markdown("### Enter your known values")

    if target == "Concentration":

        moles = st.number_input(
            "Number of moles (mol)",
            min_value=0.0, value=0.0, step=0.1
        )

        volume = st.number_input(
            f"Volume ({volume_unit})",
            min_value=0.0, value=0.0, step=0.1
        )

        if st.button("Calculate", use_container_width=True):

            if volume == 0:
                st.error("Volume cannot be zero.")
            else:

                if volume_unit == "cm³":
                    volume /= 1000

                answer = moles / volume

                st.success(
                    f"Concentration = {answer:.6g} mol/dm³"
                )

                st.latex(r"c = \frac{n}{V}")

    elif target == "Number of moles":

        concentration = st.number_input(
            "Concentration (mol/dm³)",
            min_value=0.0, value=0.0, step=0.1
        )

        volume = st.number_input(
            f"Volume ({volume_unit})",
            min_value=0.0, value=0.0, step=0.1
        )

        if st.button("Calculate", use_container_width=True):

            if volume_unit == "cm³":
                volume /= 1000

            answer = concentration * volume

            st.success(
                f"Number of moles = {answer:.6g} mol"
            )

            st.latex(r"n = c \times V")

    else:

        moles = st.number_input(
            "Number of moles (mol)",
            min_value=0.0, value=0.0, step=0.1
        )

        concentration = st.number_input(
            "Concentration (mol/dm³)",
            min_value=0.0, value=0.0, step=0.1
        )

        if st.button("Calculate", use_container_width=True):

            if concentration == 0:
                st.error("Concentration cannot be zero.")
            else:

                answer = moles / concentration

                if volume_unit == "cm³":
                    answer *= 1000

                st.success(
                    f"Volume = {answer:.6g} {volume_unit}"
                )

                st.latex(r"V = \frac{n}{c}")

    back_button()


# ==========================================================
# APPLICATION NAVIGATION
# ==========================================================

if st.session_state.page == "home":

    home()

elif st.session_state.page == "periodic":

    periodic_table()

elif st.session_state.page == "moles":

    moles_calculator()

elif st.session_state.page == "concentration":

    concentration_calculator()

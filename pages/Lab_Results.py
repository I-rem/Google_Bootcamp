import streamlit as st

st.title("🧪 Laboratuvar Sonuçları")

if "selected_case" not in st.session_state:
    st.warning("Lütfen önce bir vaka seçin.")
    st.stop()

case = st.session_state.selected_case
lab_tests = case.get("lab_results", {})

if "ordered_tests" not in st.session_state:
    st.session_state.ordered_tests = []

st.markdown("### İsteyebileceğiniz Testler:")

for test_name in lab_tests:
    if test_name not in st.session_state.ordered_tests:
        if st.button(f"🧾 {test_name} iste"):
            st.session_state.ordered_tests.append(test_name)
            st.success(f"{test_name} istendi.")

# Show ordered test results
if st.session_state.ordered_tests:
    st.markdown("### Sonuçlar:")
    for test in st.session_state.ordered_tests:
        result = lab_tests[test]
        st.markdown(f"**{test}:** {result}")
else:
    st.info("Henüz test istemediniz.")

import streamlit as st
from extract_funders_flair import extract_funders_and_ror_ids


def main():
    st.title("Extract Funders from Funding Statement")
    st.markdown("Enter a funding statement to extract funder names, award numbers, and ROR IDs.")
    funding_statement = st.text_area("Funding Statement", height=200)
    if st.button("Extract"):
        if funding_statement.strip():
            with st.spinner("Extracting funders and ROR IDs..."):
                try:
                    results = extract_funders_and_ror_ids(funding_statement)
                    if results:
                        st.subheader("Extracted Funders and ROR IDs:")
                        table_data = [["Organisation", "ROR ID"]]
                        for org_name,  ror_id in results:
                            table_data.append([org_name, ror_id])
                        st.table(table_data)
                    else:
                        st.warning("No funders found in the provided funding statement.")
                except Exception as e:
                    st.error(f"An error occurred during extraction: {str(e)}")
        else:
            st.warning("Please enter a funding statement.")


if __name__ == "__main__":
    main()

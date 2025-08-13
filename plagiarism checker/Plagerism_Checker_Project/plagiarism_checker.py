import streamlit as st
import fitz  # PyMuPDF for PDFs
from compare_reports import compute_similarity
from extract_text import extract_text_from_pdf
from textstat import flesch_reading_ease

def format_student_group(raw_text):
    """Formats student names and IDs from newline-separated text into a readable list."""
    lines = raw_text.strip().split('\n')
    formatted = []

    for i in range(0, len(lines), 2):
        name = lines[i]
        student_id = lines[i+1] if i + 1 < len(lines) else ""
        formatted.append(f"{name} ({student_id})\n")

    return '\n'.join(formatted)


# Streamlit UI
st.title("Project Report Plagiarism Checker")

title = st.text_input("Enter Project Title")
abstract = st.text_area("Enter Project Abstract", height=200)

    # Check for plagiarism
if st.button("Check Plagiarism"):
    results = compute_similarity(title, abstract)

    if results:
        # st.write("### Potential Matches Found:")
        max_title=max(r[1] for r in results)
        st.write("### Potential Matches Found:")

            # Filter and display only significant results
        for report, title_score, abstract_score,students,guide,year, in results:
            title_score = max(0, title_score)
            abstract_score = max(0, abstract_score)

            st.write(f"📄 **{report}**")
            st.write(f"📌 Title Similarity: {title_score:.2f}%")
            st.write(f"📌 Abstract Similarity: {abstract_score:.2f}%")
            st.write("\n")

            st.write(f"🎓 **Student Group:**\n {format_student_group(students)}")
            st.write(f"🧑‍🏫 **Guide:** {guide}")
            st.write(f"📅 **Academic Year: ** {year}")
            st.write("---")
    else:
        st.write("✅ No significant plagiarism detected.")
        st.write("---")

            # Additional Features
    st.subheader("Additional Analysis on Title")

            # Title uniqueness score: (1 - plagiarism_score) / 100
    title_similarity = results[0][1] if results else 0  # Get title similarity from results
    uniqueness_score = max(0, (1 - max_title / 100))

            # Readability score using Flesch Reading Ease formula
    rsc= flesch_reading_ease(abstract)
    readability_score =abs(rsc)

    col1, col2 = st.columns(2)
    with col1:
                st.metric("Uniqueness Score", 
                f"{uniqueness_score:.2f}/1.0",
                help="Higher is better (1.0 = completely unique)")

    with col2:
                st.metric("Readability (Flesch)", 
                f"{readability_score:.1f}",
                help="60+ is good (higher = easier to read)")


# to make datbase: python compare_reports.py
#
#to run the app: python -m streamlit run plagiarism_checker.py

# Plagerism_Checker_Project
A Streamlit-based web application that detects plagiarism in a project report by analyzing titles and abstracts, with additional features like title uniqueness and readability scoring.


# 🚀Features
* 🔍 Takes Ttile and Abstract as Input from user.
* 📊 Computes plagiarism scores using cosine similarity against a department library.
* 📈 Shows title uniqueness score and Flesch Reading Ease readability.
* ✅ Displays only significant matches.

  
# 🧠Technologies Used
* Python
* Streamlit – UI framework
* PyMuPDF (fitz) – PDF parsing
* Scikit-learn – TF-IDF and Cosine Similarity
* textstat – Readability scores
* Regex – Custom text extraction logic

  
# 📌Notes
* Place previous project reports (PDFs) inside the libraries_inserted/ folder.
* Run compare_reports.py once to populate the database (report_database.json).
* Then, use plagiarism_checker.py to intake and analyze new project reports.
* Extract Text python file made specific to certain Report Format.

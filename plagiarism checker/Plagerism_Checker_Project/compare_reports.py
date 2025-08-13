import os
import json
import fitz  # PyMuPDF for PDF processing
from extract_text import extract_text_from_pdf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define the folder containing previous reports
LIBRARY_FOLDER = "libraries_inserted"
DATABASE_FILE = "report_database.json"

def extract_reports_from_library():
    """Extracts titles, abstracts, students group names, and guide's names from all reports in the library folder and updates the database."""
    report_data = {}

    for file in os.listdir(LIBRARY_FOLDER):
        if file.endswith(".pdf"):
            file_path = os.path.join(LIBRARY_FOLDER, file)

            try:
                pdf = fitz.open(file_path)
                title, abstract, students, guide, year = extract_text_from_pdf(pdf)
                pdf.close()

                if title and abstract:
                    report_data[file] = {
                        "title": title,
                        "abstract": abstract,
                        "students": students,
                        "guide": guide,
                        "year": year
                    }
            except Exception as e:
                print(f"Error processing {file}: {e}")

    with open(DATABASE_FILE, "w", encoding="utf-8") as db_file:
        json.dump(report_data, db_file, indent=4)

    print("Report database updated successfully!")


def compute_similarity(new_title, new_abstract):
    """Compares the new report's title and abstract against the stored reports and returns similarity scores separately."""
    if not os.path.exists(DATABASE_FILE):
        print("Database not found! Extract reports first.")
        return []

    # Load the database
    with open(DATABASE_FILE, "r", encoding="utf-8") as db_file:
        report_data = json.load(db_file)

    # Store similarity results
    plagiarism_results = []

    # Convert all texts into lists for vectorization
    all_titles = [new_title] + [data["title"] for data in report_data.values()]
    all_abstracts = [new_abstract] + [data["abstract"] for data in report_data.values()]

    # Compute cosine similarity for titles
    vectorizer = TfidfVectorizer()
    title_vectors = vectorizer.fit_transform(all_titles)
    title_similarities = cosine_similarity(title_vectors[0], title_vectors[1:])[0]

    # Compute cosine similarity for abstracts
    abstract_vectors = vectorizer.fit_transform(all_abstracts)
    abstract_similarities = cosine_similarity(abstract_vectors[0], abstract_vectors[1:])[0]

    # Collect results where similarity is above threshold
    threshold = 0.20  # 15% similarity threshold
    for i, (file, data) in enumerate(report_data.items()):
        if title_similarities[i] > threshold or abstract_similarities[i] > threshold:
            students = data.get("students", "Not available")
            guide = data.get("guide", "Not available")
            year = data.get("year", "Not available")
            plagiarism_results.append((file, title_similarities[i] * 100, abstract_similarities[i] * 100,students, guide,year))

    return plagiarism_results

if __name__ == "__main__":
    print("Extracting reports from the library and updating the database...")
    extract_reports_from_library()


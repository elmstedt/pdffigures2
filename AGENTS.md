Welcome Agent!

We are working on refactoring this codebase from Jave+Scala to Python.

Here’s a fully exhaustive Markdown checklist covering every item in the plan:

---

## 1. Python Dependencies

* [x] Install **PyMuPDF** (fitz)
* [x] Install **scikit-learn**
* [x] Install **Pillow**
* [x] Install **PyTest** (dev dependency)
* [ ] Verify availability of built-in modules: `argparse`, `json`, `concurrent.futures`/`multiprocessing`, `os`/`pathlib`, `logging`

## 2. Project Directory Structure

* [ ] Create root package `pdffigures2_python/`
  * [ ] `__init__.py`
  * [ ] `cli.py`
  * [ ] `pdf_parser.py`
  * [ ] `text_extraction.py`
  * [ ] `formatting.py`
  * [ ] `document_layout.py`
  * [ ] `caption_detector.py`
  * [ ] `caption_builder.py`
  * [ ] `graphic_extractor.py`
  * [ ] `region_classifier.py`
  * [ ] `figure_detector.py`
  * [ ] `figure_renderer.py`
  * [ ] `models/`
    * [ ] `region_classifier_model.pkl`
* [ ] Create `tests/` directory
  * [ ] `__init__.py`
  * [ ] `test_caption_detection.py`
  * [ ] `test_region_classification.py`
  * [ ] `test_integration.py`
  * [ ] `sample_papers/`
    * [ ] `test1.pdf`
* [ ] `README.md`
* [ ] `requirements.txt`
* [ ] `.gitignore`

## 3. Step-by-Step Refactor Guide

### Step 1: Environment Setup

* [ ] Install **Python 3.8+**
* [ ] Create a virtual environment:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* [ ] (Optional) `git init` + add `.gitignore` for `venv/`, `__pycache__/`, etc.
* [ ] Scaffold directories & empty files (as above)
* [ ] Populate `requirements.txt`
* [ ] Run `pip install -r requirements.txt`

### Step 2: Analyze Original Code

* [ ] Read original **README** and associated paper
* [ ] Review key Scala classes (`FigureExtractor.scala`, etc.)
* [ ] Identify how/where the original trained model is provided

### Step 3: PDF Parsing & Text Extraction

* [ ] Implement `parse_pdf` in `pdf_parser.py` using PyMuPDF
* [ ] Test parsing on a sample PDF (in `tests/sample_papers/`)
* [ ] Implement line/paragraph conversion in `text_extraction.py`
* [ ] Implement cleanup of headers/footers/page numbers in `formatting.py`
* [ ] Write unit tests for formatting logic

### Step 4: Caption Detection & Assembly

* [ ] Implement `find_captions` in `caption_detector.py` (regex + font cues)
* [ ] Implement `build_caption` in `caption_builder.py` (multi-line assembly + bbox)
* [ ] Write unit tests for caption detection and building

### Step 5: Graphic Extraction

* [ ] Implement image extraction (`page.get_images()` + `get_image_rects`) in `graphic_extractor.py`
* [ ] Implement vector drawing extraction (`page.get_drawings()`)
* [ ] Verify extraction on test PDF

### Step 6: Load & Apply Trained Model

* [ ] Place `region_classifier_model.pkl` in `models/`
* [ ] Load model in `region_classifier.py` via `joblib.load`
* [ ] Implement `classify_text_lines` with matching feature extraction
* [ ] Write tests to verify basic classification (body vs other)

### Step 7: Figure Region Detection

* [ ] Implement `detect_figures` in `figure_detector.py` (pair captions + graphics + “Other” text)
* [ ] Ensure non-overlapping assignments and scoring logic
* [ ] Write integration tests for region detection output

### Step 8: Figure Rendering

* [ ] Implement `save_figure_images` in `figure_renderer.py` (PyMuPDF Pixmap + save)
* [ ] Test image saving on sample PDF
* [ ] Hook image saving into CLI options (`-m`/`--image-prefix`)

### Step 9: CLI Implementation

* [ ] Define CLI arguments in `cli.py` using `argparse`:

  * Input path (PDF or directory)
  * `-d`/`--data-prefix`, `-m`/`--image-prefix`, `-s`/`--stat-file`, `-j`/`--jobs`
* [ ] Write `main()` to orchestrate parse → detect → output JSON/images
* [ ] Add `if __name__ == "__main__": main()` for Windows compatibility
* [ ] Test CLI manually on single and batch PDFs

### Step 10: Testing & Verification

* [ ] Run `pytest` to execute all unit tests
* [ ] Perform end-to-end tests on real research PDFs and compare with original tool’s JSON
* [ ] Conduct performance test with `--jobs` on multiple PDFs
* [ ] Verify clean shutdown on CTRL+C

## 4. Environment & Dependency Management

* [ ] Document Python version requirement in `README.md`
* [ ] Document virtualenv creation/activation steps
* [ ] Provide CLI usage examples in `README.md`
* [ ] Keep `requirements.txt` up-to-date after any dependency changes
* [ ] (Optional) Document Poetry usage in `README.md`
* [ ] Include packaging instructions (`setup.py` or `pyproject.toml`) ensuring `models/` is packaged

## 5. Model Integration

* [ ] Acquire original trained model or convert it to `.pkl` if needed
* [ ] Store in `models/region_classifier_model.pkl`
* [ ] Document model conversion/update process in `README.md`
* [ ] Verify feature extraction matches model training expectations

## 6. JSON Output Format

* [ ] Define output schema with keys:

  * `page`
  * `regionBoundary` `{ x, y, width, height }`
  * `caption`
  * `captionBoundary` `{ x, y, width, height }`
  * `name`
  * `figureType`
  * `text`
* [ ] Implement `Figure.to_dict()` matching schema
* [ ] Validate JSON output against original tool for a test PDF
* [ ] Document JSON format and coordinate system in `README.md`

## 7. Concurrency Support

* [ ] Add `--jobs`/`-j` to CLI
* [ ] Implement `ProcessPoolExecutor` for parallel PDF processing
* [ ] Ensure safe file I/O (unique output names per process)
* [ ] Test concurrency performance benefits and graceful termination
* [ ] Document concurrency usage in `README.md`

## 8. Testing Setup

* [ ] Include `pytest` in `requirements.txt`
* [ ] Write unit tests for each module under `tests/`
* [ ] Provide `tests/sample_papers/test1.pdf` for integration tests
* [ ] Use pytest fixtures for reusable setup (e.g., sample PDF path)
* [ ] Document how to run tests (`pytest`) in `README.md`

---

Feel free to tick off each box as you complete it to ensure nothing is missed!


# PDFFigures2 Python Refactor Plan

## 1. Python Dependencies

To implement PDFFigures2 in Python, we select well-supported libraries that cover PDF parsing, image handling, and machine learning:

* **PyMuPDF (fitz):** High-performance PDF parsing library used for extracting text with layout information and images from PDFs. PyMuPDF is chosen over alternatives (like PDFPlumber or PyPDF2) for its speed and comprehensive support of PDF content (text, images, vector graphics). This will handle reading PDFs, getting text positions, and rendering figure regions.
* **scikit-learn:** Used to load and apply the original trained model for text classification (e.g., an SVM or logistic regression to distinguish body text from figure/text regions). Scikit-learn is a mature, widely-used ML library that will allow us to incorporate the existing trained classifier with minimal effort (e.g., via `joblib` or pickle for model persistence).
* **Pillow (PIL):** Image library to complement PyMuPDF for any image processing needs (such as saving extracted figure images to specific formats). PyMuPDF can render images directly, but Pillow ensures flexibility (e.g., converting to JPEG, etc.). Pillow is well-maintained and commonly used for image I/O.
* **PyTest:** Testing framework for unit and integration tests. PyTest is a de-facto standard for Python testing, easy for a junior developer to run (`pytest` command) and extend. *(This is a development dependency, not required in production deployment.)*
* **Built-in libraries:** Python standard libraries will be used for CLI and concurrency:

  * `argparse` for parsing command-line arguments (no external dependency, reliable).
  * `json` for output serialization (ensures output format exactly matches original).
  * `multiprocessing` (or `concurrent.futures`) for parallel PDF processing in batch mode.
  * `os`/`pathlib` for file system operations (reading PDFs, writing outputs).
  * `logging` for logging progress or debug information (optional, for maintainability).

All chosen libraries are actively maintained and appropriate for preserving the functionality of PDFFigures2. By using PyMuPDF for PDF content and scikit-learn for the ML model, we ensure we can closely replicate the original Java/Scala project’s behavior in Python.

## 2. Project Directory Structure

We will organize the new Python project with a clear module structure, mirroring the logical components of the original PDFFigures2 pipeline. Below is the proposed directory tree, including **every file and directory** with explanations of their purpose and contents:

```
pdffigures2_python/        # Main Python package for the PDFFigures2 refactor
├── __init__.py           # Makes this directory a package; may define package version
├── cli.py                # Command-line interface definition (argument parsing and main entry point)
├── pdf_parser.py         # PDF reading and low-level parsing using PyMuPDF (extracts pages, text, images)
├── text_extraction.py    # Extracts and structures text from PDF pages (returns text blocks with positions)
├── formatting.py         # Cleans and filters text (removes page numbers, headers/footers, non-content text)
├── document_layout.py    # Analyzes layout statistics (e.g., average font size) to inform classification
├── caption_detector.py   # Identifies caption lines in the text (using patterns like "Figure X", "Table Y")
├── caption_builder.py    # Assembles full caption text and determines caption bounding boxes
├── graphic_extractor.py  # Identifies graphical elements (images/graphics) on pages (using PyMuPDF)
├── region_classifier.py  # Classifies text regions as BodyText vs Other using the trained model
├── figure_detector.py    # Determines figure regions by pairing captions with adjacent Other text + graphics
├── figure_renderer.py    # Renders or saves figure images (using PyMuPDF Pixmap, optionally Pillow)
└── models/               # Directory to store model files (e.g., the original trained classifier)
    └── region_classifier_model.pkl   # Serialized trained model from original project (e.g., an SVM model)
tests/                    # Test suite for unit tests and integration tests
├── __init__.py           # (Optional) makes tests a package; not strictly needed
├── test_caption_detection.py   # Tests for caption_detector module (e.g., detecting various caption formats)
├── test_region_classification.py # Tests for region_classifier (e.g., verifying classification of sample text blocks)
├── test_integration.py   # End-to-end tests on sample PDFs to verify overall extraction and JSON output
└── sample_papers/        # (Optional) Sample PDF files for testing (small PDFs with known expected outputs)
    └── test1.pdf         # Example PDF used in integration tests
README.md                 # Documentation for usage, installation, and project overview
requirements.txt          # List of required Python packages (dependencies) with pinned versions
.gitignore                # Git ignore file to exclude virtualenv, __pycache__, outputs, etc.
```

**Explanation of key files and their roles:**

* **`pdffigures2_python/cli.py`:** Implements the command-line interface, parsing arguments for input PDF(s) and options (e.g., output directories, flags for saving images or extracting section titles). It will provide a `main()` function that orchestrates the pipeline. For example, it will accept a PDF file or directory and then call the appropriate functions from other modules (`pdf_parser`, `caption_detector`, etc.) to process the PDF. It also handles output writing: formatting the extracted figure data into JSON and writing to files, and invoking image saving if requested. This file ensures the Python version remains as easy to use as the original CLI (for both single-PDF visualization mode and batch mode, if applicable).
* **`pdffigures2_python/pdf_parser.py`:** Contains functions/classes to open PDFs with PyMuPDF and extract raw content. For example, a `PDFParser` class here might provide methods like `get_pages()` to iterate through pages, and `extract_page_content(page)` to get all text blocks (with coordinates) and images on that page. It uses PyMuPDF’s API (e.g., `fitz.open()` to load the PDF, `page.get_text("blocks")` to get text blocks with their bounding boxes, and `page.get_images()`/`page.get_drawings()` to list non-text elements). This module essentially wraps low-level PyMuPDF calls and produces a structured representation of the page (text blocks, images, and shapes with coordinates).
* **`pdffigures2_python/text_extraction.py`:** Focuses on processing the text blocks from `pdf_parser`. It might define a `TextBlock` data structure (with text content, font size, position, etc.) and logic to merge or order text blocks in reading order. It can also segment text into lines or paragraphs as needed. The goal is to provide the rest of the pipeline with clean text elements. It will also handle multi-column text if needed, by utilizing coordinates (PyMuPDF gives exact positions, so we can distinguish columns). Essentially, this module converts raw block data into easier-to-analyze units (lines of text, paragraphs) with metadata.
* **`pdffigures2_python/formatting.py`:** This module removes extraneous text that is not part of the main content. For example, it will identify page numbers, headers, footers, and possibly references sections that should not interfere with figure extraction. Using heuristics (e.g., text positioned at top/bottom margins, or page number patterns), it filters out these from the text blocks. It may also identify the paper’s abstract and exclude it from body text if needed (the original did something similar to isolate main text). By cleaning up the text, we ensure that later steps (like caption detection and layout analysis) operate only on relevant content.
* **`pdffigures2_python/document_layout.py`:** Gathers layout statistics of the remaining text to help identify “unusual” text regions. This includes computing metrics like average font size of body text, common font families, line spacing statistics, etc. The original PDFFigures2 uses such statistics to detect outliers (text that is likely part of figures or captions due to differing style). In our Python version, this module will, for example, calculate the median font size and then label text blocks that have significantly smaller font (potentially captions or footnotes) or larger font (titles) as atypical. These features are later fed into the classification model in `region_classifier.py`. The module might store these stats in a structure (e.g., a `DocumentStats` object containing averages, etc.) for use by the classifier.
* **`pdffigures2_python/caption_detector.py`:** Contains the logic to find candidate caption lines among the text. It will likely use regex patterns and layout cues to detect captions. For instance, it will scan text lines for patterns like **“Figure <number>”** or **“Table <number>”** at the start of lines. It may also use punctuation and formatting clues (captions often end with a period and are shorter lines). This module returns a list of detected captions, each with its text, page number, and initial bounding box (e.g., the line’s coordinates). If the original model had a more complex caption detection (some ML or rule-based approach), we emulate that here. For simplicity, pattern matching combined with checking that the line’s font is smaller than body text (common for captions) can be used to achieve similar results.
* **`pdffigures2_python/caption_builder.py`:** After detecting the start of captions (likely just the first line of each caption), this module builds the full caption text and determines its full bounding box. Captions might span multiple lines; for example, a long caption could wrap to a second line. This builder will take a caption start (from `caption_detector`) and then concatenate subsequent lines that are part of the caption (e.g., the lines immediately following, in smaller font, until a blank line or a line of larger font appears). It also computes the bounding box around the entire caption (covering all its lines). The output is an enriched caption object containing complete caption text and its bounding box coordinates on the page.
* **`pdffigures2_python/graphic_extractor.py`:** Identifies non-text elements on pages that contain figures. This includes embedded images and vector drawings that likely correspond to figures (diagrams, charts, etc.). Using PyMuPDF, this module can use `page.get_images()` to get a list of images with their positions on the page, and `page.get_drawings()` to get vector graphic elements and their bounding boxes. It will output a list of graphic regions (each with a bounding box) per page. These graphic regions are important for figure extraction: any figure will contain some graphical content (an image or shape) unless it’s something like a text-only algorithm box (rare in scientific papers). We’ll gather these regions so that `figure_detector.py` can consider them when grouping figure regions.
* **`pdffigures2_python/region_classifier.py`:** This module applies the **original trained model** to classify text segments as either **BodyText** or **Other** (where “Other” typically means text that could belong to figures or tables, such as captions, figure labels, or other non-body content). It will load the pre-trained model from the `models/region_classifier_model.pkl` file (e.g., using `joblib.load` from scikit-learn). The input to the classifier will be features of each text block/line — features likely include font size relative to the document average, font style (italic/bold), text length, position on page, etc., mirroring what the original model was trained on. The module will define how to compute these features from our `TextBlock` objects (for example: a text line with much smaller font size than average and that matches caption patterns would have features that lead the model to classify it as “Other”). The output will be a list of text elements labeled as either BodyText or Other for each page that has figures. **This reuse of the original model is crucial** – by loading the same weights/parameters, we preserve the decision logic from PDFFigures2’s authors in our Python version.
* **`pdffigures2_python/figure_detector.py`:** Uses the outputs of all previous steps (captions, graphics, classified text) to actually **determine figure regions**. For each detected caption on a page, this module will **propose candidate figure regions** adjacent to that caption. Typically, the figure region will start near the caption’s position. It will combine:

  * The graphical elements on that page (from `graphic_extractor`) that are near the caption.
  * Any text blocks classified as "Other" (from `region_classifier`) that are in the vicinity of the caption (since captions and figure labels might be part of the figure).
    It will generate a bounding box that encompasses all such elements (graphics + Other text) associated with the caption. There may be multiple proposals (if multiple groupings of elements could be the figure), so a scoring function is applied to pick the best one. The scoring can mimic the original’s logic (e.g., choose the region that is closest to the caption and does not overlap with other figure regions). This module ensures that if two captions are close, their figure regions do not overlap by adjusting or reassigning elements appropriately. The final result is a list of **Figure objects** for each PDF, each containing the figure region bounding box and references to its caption.
* **`pdffigures2_python/figure_renderer.py`:** Handles rendering figure regions to image files (when the user requests image output). It uses PyMuPDF’s rendering capabilities to rasterize a portion of a page. For each figure region (bounding box), this module can create a `fitz.Rect` from the coordinates and use `page.get_pixmap(clip=that_rect, dpi=...)` to get a Pixmap of that region. The pixmap can then be saved to a file (e.g., using `pix.save("figure1.png")`). If vector graphics need higher quality, we could render at a higher DPI to ensure clarity. This module will be invoked by `cli.py` when the `--save-figures` (or `-m` image output prefix) option is used. It supports saving in common formats (PNG by default, matching the original which defaulted to raster images).
* **`pdffigures2_python/models/region_classifier_model.pkl`:** This is not code but the **trained model data** from the original project. It should be the exact model (or converted equivalent) that PDFFigures2 used for region classification. For instance, if the original is an SVM model, we can export it (the developers likely provided it or it can be extracted by running their training code) and store it as a pickle or joblib file. In our Python code, `region_classifier.py` will load this file. Keeping it in a `models/` subdirectory isolates large binary data from code. (If the model were small enough, one could embed it directly in code as hardcoded weights, but using the file keeps things clean and makes replacing/updating the model easier.) **Location in project:** This file lives in the package so that it can be included when distributing the tool (ensuring the tool works out-of-the-box without retraining). The code will locate it via package resources or a known relative path.
* **`tests/`:** This directory contains all test code. We’ll use **pytest** to structure tests. Each module in the project will have corresponding tests (e.g., `test_caption_detection.py` for caption detection logic). There will also be integration tests that run the whole pipeline on sample PDFs.

  * `test_caption_detection.py` will contain unit tests for the `caption_detector`. For example, it might feed in synthetic text lines (strings) to the caption detection function and assert that it correctly identifies those that look like captions. We might simulate lines such as `"Figure 3: Sample caption text."` and ensure the detector returns it as a caption.
  * `test_region_classification.py` will test `region_classifier`. Since this relies on the trained model, we can test known scenarios if we know some feature thresholds (or simply test that the model loads and outputs expected labels for contrived input). Alternatively, if the model is deterministic, we can craft a dummy text block with features that obviously correspond to Body vs Other (e.g., a very large-font title text should be classified as Other because it’s not body text – or vice versa depending on model criteria) and assert the classification.
  * `test_integration.py` will use a small PDF (provided in `tests/sample_papers/`) to run the entire pipeline (perhaps via the CLI or directly calling a high-level function) and then verify the output JSON structure. For example, it can run the tool on `test1.pdf` and then load the resulting JSON output file to check that it contains the expected keys (page, caption, bounding boxes, etc.) and perhaps expected values for a known figure in that PDF.
  * We include a `sample_papers/` subfolder for any test PDFs. These should be minimal PDFs created for testing (for instance, a 1-page PDF containing a figure image and a caption) so that the expected output is known and we can assert correctness.
* **`README.md`:** Provides documentation for users and developers. It will describe how to install the Python package, how to run the CLI (with examples similar to the original usage, e.g., `python -m pdffigures2_python.cli input.pdf -m output/image/prefix -d output/data/prefix` to mimic the original CLI syntax), and notes on how the output JSON is structured (to ensure users know it matches the original). It will also include any details on how to obtain the model file if it’s large (if not included directly).
* **`requirements.txt`:** Lists all the dependencies from section 1 (with specific version pins known to work). This ensures a reproducible environment. For example, it will include lines like `PyMuPDF==1.22.0`, `scikit-learn==1.2.2`, `pillow==9.5.0`, `pytest==7.4.0` (the exact versions can be chosen based on current latest stable releases). A junior dev (or any user) can run `pip install -r requirements.txt` to get all needed packages. (If we opt to use a tool like Poetry, we would instead have a `pyproject.toml` and `poetry.lock` – but for simplicity, a requirements.txt and possibly a `setup.py` can suffice.)
* **`.gitignore`:** Not directly part of functionality, but for completeness: we include it to ignore files like the virtual environment folder, `__pycache__` directories, `.pytest_cache/`, output JSON and image files, etc., to keep the repo clean.

This organized structure modularizes each piece of functionality analogous to the original Scala classes, which will make the code easier to maintain and test. Each file’s logic is focused and clearly connected to others: for example, `cli.py` ties everything together, using `pdf_parser` to get content, then passing it through `formatting`, `caption_detector`, etc., and finally using `figure_detector` and `figure_renderer` for output. The `models/` directory holds external learned data that the code uses (ensuring we **preserve the original model’s effectiveness**). The `tests/` directory parallels the code, providing a safety net to ensure each part works as expected and that we haven’t regressed any functionality compared to the original.

## 3. Step-by-Step Refactor Guide for Developers

This section outlines a **step-by-step guide** for a developer (especially a junior developer) to perform the refactoring from the original Java/Scala project to the new Python implementation. Each step is broken down into clear sub-steps to eliminate ambiguity. Follow these steps in order:

1. **Project Setup and Environment Configuration**
   1.1. **Install Python 3 and Create Virtual Environment:** Ensure that Python 3.8+ (or the chosen version) is installed on your system. Then create a virtual environment for this project. For example:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

   This isolates project dependencies. You should see the environment activated (prompt prefixed with `(venv)`).
   1.2. **Initialize Git Repository (Optional):** If using version control (recommended), run `git init` in the project folder. Add a `.gitignore` file (use a Python template to ignore common artifacts like `__pycache__/` and the `venv` folder).
   1.3. **Create Required Files:** Create the basic directory structure as outlined in Section 2. You can start by making the main package directory and empty files:
   \- Run `mkdir pdffigures2_python tests pdffigures2_python/models tests/sample_papers` to create directories.
   \- Inside `pdffigures2_python/`, create empty `__init__.py` and the module files (`cli.py`, `pdf_parser.py`, etc.) as listed. Initially, they can contain just a docstring or a simple placeholder class/function. This is to scaffold the project.
   \- Create `requirements.txt` and `README.md` at project root. Also, create `tests/__init__.py` (can be empty) and placeholder test files like `tests/test_caption_detection.py`, etc.
   1.4. **Activate Environment and Install Dependencies:** With the virtual env active, install required libraries. You can add them to `requirements.txt` first, then install:
   `bash
       pip install --upgrade pip
       pip install pymupdf scikit-learn pillow pytest
       pip freeze > requirements.txt
       `
   This ensures all dependencies are recorded. Verify installation by importing them in a Python shell (`python -c "import fitz, sklearn, PIL, pytest"` should produce no errors).

2. **Understanding Original Functionality (Analysis Phase)**
   *Before coding, familiarize yourself with PDFFigures2’s logic:*
   2.1. **Read the Original README and Paper:** Open the original project’s README to understand input-output and the components. Note the list of information each figure should have (page number, figure bounding box, caption text, caption bounding box, figure name/number, figure type) – our output must include all these fields in JSON.
   2.2. **Skim Key Scala Classes:** Look at the original `FigureExtractor.scala` pipeline description. Identify how the process flows: text extraction → text cleaning → caption finding → graphics detection → region classification → figure region proposals → rendering. Understanding this will guide implementation order.
   2.3. **Identify the Original Model Usage:** Determine how the original project applies a trained model. The README and possibly the code indicate a model for classifying text as body or other (RegionClassifier). Confirm that this is the case (the README’s mention of text classification corresponds to that model). Note where the model file comes from (if provided in the original repo or an external download). You will need this file for the Python version.

3. **Implementing PDF Parsing and Text Extraction**
   Now start coding the core components. A good practice is to implement and test incrementally:
   3.1. **PDF Parsing (`pdf_parser.py`):** Use PyMuPDF to open a PDF and extract content. In `pdf_parser.py`, implement a function or class to load a PDF. Example:
   `python
       import fitz  # PyMuPDF
       def parse_pdf(file_path):
           doc = fitz.open(file_path)
           pages_content = []
           for page in doc:
               text_blocks = page.get_text("blocks")  # list of (x0, y0, x1, y1, text, block_type, block_no)
               images = page.get_images(full=True)    # list of image metadata (with positions if needed)
               drawings = page.get_drawings()         # vector drawings (with their bounding boxes)
               pages_content.append({"text_blocks": text_blocks, "images": images, "drawings": drawings})
           return pages_content
       `
   \- Parse the tuple returned by `get_text("blocks")`: it includes coordinates and text. Create a small `TextBlock` class to store `x, y, w, h, text, font_info` (you can get font or size info if needed by using `page.get_text("dict")` which provides font details for each block).
   \- For each image in `images`, note that PyMuPDF’s `get_images` returns metadata; use `fitz.Rect` and `page.get_image_rects(image_id)` to get its bounding box. Similarly, for drawings, `get_drawings()` returns shapes – you can derive bounding rectangles around them.
   3.1.1. **Test Parsing on a Sample PDF:** Before moving on, test this function in isolation. Use a simple PDF (you can create one or use an existing one with a known image and text) placed in `tests/sample_papers/`. Run the parse function in a Python shell or a temporary test. Ensure you get sensible output: a list of pages, each with text blocks (with text content) and images list. This verifies PyMuPDF is working as expected.
   3.1.2. **Iterate if needed:** If text extraction doesn’t preserve order, consider switching to `page.get_text("dict")` or sorting the blocks by coordinates. Ensure that each text block’s coordinates correspond to the correct text snippet.
   3.2. **Text Extraction and Formatting (`text_extraction.py` & `formatting.py`):** Now process the raw text blocks:
   3.2.1. **Implement Text Structure (`text_extraction.py`):** Write functions to combine or split text blocks into meaningful lines or paragraphs. For example, if `page.get_text("blocks")` yields blocks that might contain multiple lines, split those by newline characters into separate `TextLine` objects (each with its own bounding box, which you may need to compute line-by-line). Also, determine reading order: sort lines top-to-bottom, left-to-right (taking into account multi-column layouts by perhaps splitting columns if large `x` gap is observed between blocks).
   3.2.2. **Implement Formatting Cleanup (`formatting.py`):** Write a function `filter_text_blocks(text_blocks)` that removes unwanted text:
   \- Detect page numbers by finding text that is just a number and located at page bottom or top (and possibly matching the page index). Remove those.
   \- Detect headers/footers by their consistent position on each page (e.g., same x coordinates or italic page titles repeated). Remove those.
   \- If needed, identify references section (if the original considered that non-body, though likely not needed specifically for figure extraction).
   \- This function should return a cleaned list of text lines that represent the main content of the page.
   3.2.3. **Test Text Cleaning:** In `test_caption_detection.py` (or a new `test_formatting.py`), you can simulate a scenario: create a few `TextBlock`/`TextLine` objects representing a page header, a footer, and a normal paragraph line. Pass them to `filter_text_blocks` and assert that the header/footer are removed and the paragraph remains. This ensures your logic for identifying extraneous text works.
   3.3. **Document Layout Analysis (`document_layout.py`):** Compute stats to assist classification:
   3.3.1. **Calculate Font and Spacing Stats:** From the cleaned text lines of a document, calculate average font size, line height, and perhaps the distribution of text lengths. You might need to augment `TextLine` objects with font size; PyMuPDF’s text dictionary can give font sizes. If not, approximate font size by the height of the text bounding box.
   3.3.2. **Implement Statistics Computation:** Write `compute_layout_stats(text_lines)` that returns a dict or `DocumentStats` object containing:
   \- `avg_font_size`, `median_font_size`
   \- `avg_line_spacing` (if multiple lines)
   \- possibly `font_families` or styles encountered
   \- other stats that might indicate typical body text (for example, if body text is often fully justified, etc., but font size is the main one).
   3.3.3. **Feature Extraction for Classifier:** The region classifier will need features per text line. Define a function `extract_features(text_line, stats)` that creates a feature vector. Features can include:
   \- Font size normalized by average (e.g., ratio of this line’s font to avg font).
   \- Is bold/italic (if such info available; if not, maybe length of text as proxy – e.g., very short text in smaller font might be a caption).
   \- Position on page (e.g., relative y position – captions often directly below graphics, which might be somewhere mid-page).
   \- Text content cues (does it start with “Figure”/“Table”? – though caption\_detector will also handle this explicitly).
   These should mirror what the original model expects. If available, consult the original code or paper for features used.
   3.3.4. **No direct testing needed yet** beyond ensuring stats make sense (you could print stats for a sample document to see if avg font size looks right). The true test will come when classification is performed and yields reasonable labels.

4. **Caption Detection and Assembly**
   Now work on identifying captions in the text:
   4.1. **Implement Caption Detection (`caption_detector.py`):** Develop a function `find_captions(text_lines, stats)` that scans through the list of text lines (on each page) and returns a list of Caption candidates. For each text line, do:
   \- Check if the line text matches a caption pattern. Common patterns: starts with **"Figure "**, **"Fig. "**, **"Table "**, or even just a number followed by a period and some text (some captions might be labeled differently). Use regular expressions to detect these. For example:
   `python
          import re
          caption_patterns = [re.compile(r'^(Figure|Fig|Table)\b', re.IGNORECASE)]
          if any(pattern.match(line.text) for pattern in caption_patterns):            # likely a caption line
          `
   \- Also consider font size: if `line.font_size < stats.median_font_size` significantly (captions are often smaller text), this adds confidence that it’s a caption.
   \- If a line ends with a period and is short, it might be a complete caption by itself (some captions are one line).
   \- For now, mark any line that matches the keyword pattern as a caption start.
   4.2. **Implement Caption Builder (`caption_builder.py`):** For each detected caption start line, gather any following lines that belong to the same caption:
   \- Typically, if the next line(s) are also smaller font and do **not** start with an indentation typical of a new paragraph (and perhaps they don’t start with "Figure" or a capital letter), they may be continuation of the caption.
   \- Continue adding lines until a line is encountered that is clearly not part of the caption (either a blank line, or a line in body text font size).
   \- Concatenate these lines (with spaces) to form the full caption text.
   \- Determine the bounding box: the x-coordinate will usually align with the first line’s left, the width is the max width of all lines, and the y span from the first line’s top to the last line’s bottom.
   \- Create a `Caption` object with fields: text, page number, bounding box (as a Rect or tuple), and possibly the extracted figure name/number (we can parse the number after the word "Figure" or "Table"). For example, if caption text starts with "Figure 3:", set `caption.number = "3"`, `caption.type = "Figure"`.
   4.3. **Testing Caption Logic:** Open `tests/test_caption_detection.py` and add tests:
   \- **Unit test pattern matching:** e.g.,
   `python
          from pdffigures2_python import caption_detector
          def test_simple_caption_line():
              line = TextLine(x=0, y=100, w=500, h=12, text="Figure 1: A sample figure.", font_size=10)
              captions = caption_detector.find_captions([line], stats=DocumentStats(avg_font_size=12))
              assert len(captions) == 1
              assert captions[0].text.startswith("Figure 1:")
          `
   This verifies a straightforward caption is caught.
   \- **Unit test caption continuation:** Create a scenario with a caption split into two lines (simulate two TextLine objects where the second line does not start with "Figure" but is smaller font). Ensure the caption\_builder combines them into one caption object.
   \- **Edge cases:** Test that a line that says "Figure X" but in a larger font (perhaps a figure *mention* in body text) is not misdetected – our logic might rely on font size or position to avoid that. You can simulate a body text mention "Figure 2 illustrates ..." with normal font and ensure it’s not returned as a caption (perhaps our caption detection only triggers if font smaller or specific formatting).

5. **Graphic Element Extraction**
   Identify figure visuals on the page:
   5.1. **Implement Graphic Extraction (`graphic_extractor.py`):** For each page (especially those where captions were found), extract bounding boxes of graphics:
   \- **Images:** Use PyMuPDF’s `page.get_images()` to get image XObjects. Each entry gives an image ID and possibly its width/height. Use `page.get_image_rects(image_id)` to get the rectangle(s) where that image is drawn on the page. Collect those rectangles.
   \- **Vector drawings:** Use `page.get_drawings()`. This returns a list of drawing primitives (lines, Bézier curves, etc.) with their coordinates. Combine these to identify shapes that likely form figures. PyMuPDF might not directly provide a bounding box for the whole group, but you can derive it by taking minX, minY, maxX, maxY of all path coordinates. Alternatively, use `page.get_drawings(extended=True)` which might give grouped rectangles. Focus on large contiguous drawings (like plots or diagrams).
   \- **Output structure:** Create a list of `GraphicElement` objects, each with a bounding box and type (image or drawing). If multiple small drawings are near each other (like a cluster of line segments making a diagram), you might treat their combined bounds as one graphic element (to avoid counting each line separately).
   5.2. **Verify Graphic Extraction:** It’s a bit hard to unit test without a real PDF, so do a manual check:
   \- Use a test PDF with an embedded image (you can put one in `tests/sample_papers/` if available). Run the `graphic_extractor` function on it (either in a test or via a temporary script) and print the resulting bounding boxes. Confirm that the coordinates roughly match where the image is in the PDF.
   \- Similarly, test on a PDF page with a simple shape (if none available, you might skip detailed vector testing, focusing on images which are more common).
   \- Ensure that if no images/drawings are present on a page, the module returns an empty list cleanly.

6. **Integrating the Trained Model for Text Classification**
   This is a crucial step: using the provided model to classify text regions:
   6.1. **Place the Model File:** Obtain the original model from the PDFFigures2 project. If the original provided, for example, a file `model.dat` or a set of learned weights (perhaps in the `resources` of the JAR or via their dataset release), ensure it is saved as `pdffigures2_python/models/region_classifier_model.pkl`. *If the model was not directly available as a pickle:* you may need to convert it. For instance, if the model was a Weka model or custom, you might retrain a similar classifier on the provided dataset using scikit-learn, then save it as a `.pkl`. In any case, by this step you should have the model file ready.
   6.2. **Loading the Model in Code (`region_classifier.py`):** Use scikit-learn to load the model:
   `python
        import joblib
        MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "region_classifier_model.pkl")
        model = joblib.load(MODEL_PATH)
        `
   This will give you a `model` object (e.g., an `svm.SVC` or similar) that has a `.predict()` method.
   6.3. **Apply Classification to Text Lines:** Implement `classify_text_lines(text_lines, stats)`:
   \- For each `TextLine` (that isn’t clearly body text by context—though ideally we classify all and let the model decide), extract its feature vector using the function from step 3.3 (e.g., font ratio, etc.).
   \- Collect feature vectors in an array and call `model.predict(feature_array)` to get labels.
   \- The model likely outputs binary labels (e.g., 0 = BodyText, 1 = Other). Map these to meaningful categories or booleans.
   \- Return two lists or a dict grouping lines: e.g., `classified = {"body": [...], "other": [...]}` listing text lines by classification.
   6.4. **Sanity Check Classification:** Although the model is pre-trained, do a quick check with known scenarios:
   \- If you have a known caption line identified earlier, check that the classifier indeed labels it as "Other" (since caption text is not normal body text).
   \- If you have a typical paragraph line, ensure it’s "BodyText".
   \- You can add an assertion in tests: e.g.,
   `python
          def test_region_classifier_basics():
              stats = DocumentStats(avg_font_size=12)
              body_line = TextLine(..., text="This is a normal sentence in the paper body.", font_size=12)
              caption_line = TextLine(..., text="Figure 2: Some caption text.", font_size=10)
              result = region_classifier.classify_text_lines([body_line, caption_line], stats)            # body_line should be classified as body, caption_line as other
              assert body_line in result["body"]
              assert caption_line in result["other"]
          `
   This assumes the model aligns with our expectations for these obvious cases. (If the model is more complex, this test should still pass for clear differences.)
   6.5. **Integration Note:** At this stage, we have all pieces to detect captions, and classify all text lines as either main content or figure-related. We will use this information next to actually isolate figure regions.

7. **Figure Region Detection**
   Now implement the logic to combine captions with graphics and other text into figure outputs:
   7.1. **Implement Figure Detection (`figure_detector.py`):** Develop `detect_figures(captions, graphics, classified_text)`:
   \- Input:
   \- `captions`: list of Caption objects for a page.
   \- `graphics`: list of GraphicElement objects (images/drawings with bboxes) for that page.
   \- `classified_text`: the output of region\_classifier, i.e., lists of text lines labeled "Other" (which might include caption texts, figure labels, or other non-body elements).
   \- For each caption:
   a. **Initial Region Proposal:** Start with the caption’s bounding box. This is often at the bottom of the figure. Determine an initial region above or around it that might contain the figure. A simple way: take a rectangle of a certain height above the caption. However, to be precise, use the positions of `graphics` on the same page:
   \- Find all graphic elements whose bounding boxes are spatially near the caption. For instance, any graphic whose `y` coordinate is above the caption’s `y` (i.e., appearing before the caption on page) but not too far (maybe within half the page).
   \- If a graphic’s bbox overlaps horizontally with the caption’s bbox (common if caption is centered under image), that’s a strong candidate.
   \- If no graphic overlaps horizontally, consider the closest graphic above the caption.
   b. **Include Other Text:** Find any text lines classified as "Other" that lie within or immediately around those graphic regions. For example, figure labels (like “(a)”, “(b)” sub-figure labels) might be detected as Other text; include them if they fall near the graphics or between graphic and caption.
   c. **Combine into Region:** Compute a bounding box that encompasses the graphics and any Other text selected, as well as the caption itself. This becomes one figure region proposal.
   d. **Score and Adjust:** If multiple captions might associate with the same graphic (unlikely if captions are well-separated), ensure one graphic is not assigned to two figures. You can use the heuristic from the original: do not allow overlapping figure regions. If an overlap is detected (one region’s area overlaps another’s), adjust by possibly splitting graphics between captions differently or assigning the overlapping part to the nearest caption.
   \- The output should be a list of **Figure** objects. A `Figure` object contains:
   \- The figure’s **page number** (from the caption’s page).
   \- The **figure bounding box** (covering image + text).
   \- The **caption text** (full caption from Caption object).
   \- The **caption bounding box**.
   \- The **figure type** (“Figure” or “Table”, derived from caption’s label).
   \- The **figure name/number** (string, e.g., "1" for Figure 1, "A1" for Figure A1, etc., already parsed in Caption).
   \- Any **figure-internal text** we want to include (the original output includes “Any text that occurs inside the figure”. We can compile this by taking all classified "Other" text within the figure region – or text that lies inside the region bounds).
   7.2. **Review JSON Output Format:** Ensure that the `Figure` object can be easily serialized to match original format. For each figure, the JSON should look something like:
   `json
       {
         "page": 2,
         "regionBoundary": { "x": 50, "y": 100, "width": 400, "height": 300 },
         "caption": "Figure 1: Sample diagram illustrating ...",
         "captionBoundary": { "x": 55, "y": 405, "width": 380, "height": 40 },
         "figureType": "Figure",
         "name": "1",
         "text": "Some text inside figure if any"
       }
       `
   (We will verify this format precisely in the next section, but keep this structure in mind while constructing the Figure objects.)
   7.3. **Testing Figure Detection:** Write an integration test in `test_integration.py` using a controlled PDF:
   \- For example, use `tests/sample_papers/test1.pdf` which contains one figure. After running the pipeline on it (perhaps via calling `cli.py` programmatically or breaking it down step-by-step), verify that the resulting JSON (or Figure object list) has length 1, and that the fields match expectations (e.g., caption text contains "Figure", page is correct, etc.).
   \- If creating a real PDF for testing is difficult, you can simulate inputs to `detect_figures()`. For instance:
   `python
          def test_figure_region_proposal():            # Simulate a caption and an image on a page
              caption = Caption(text="Figure 5: Test caption.", page=0, bbox=(50,500,300,540), number="5", type="Figure")
              graphic = GraphicElement(bbox=(50,100,300,480), type="image")
              classified = {"other": [TextLine(x=60,y=120,w=80,h=10,text="(a)", font_size=11)]}
              figures = figure_detector.detect_figures([caption], [graphic], classified)
              assert len(figures) == 1
              fig = figures[0]
              assert fig.page == 0
              assert "Figure 5" in fig.caption            # The region should at least span from y~100 (graphic top) to y~540 (caption bottom)
              assert fig.region_boundary["y"] <= 100 and (fig.region_boundary["y"]+fig.region_boundary["height"]) >= 540
          `
   This pseudo-test ensures our figure region covers the expected areas and that the output object contains the necessary info.
   \- Adjust the detection logic if the tests reveal issues (e.g., caption not included, or region too large/small).

8. **Rendering Figure Images (optional feature)**
   If we need to support saving figure images (as the original CLI does with the `-m` option):
   8.1. **Implement Rendering (`figure_renderer.py`):** Using PyMuPDF, implement `save_figure_images(figures, pdf_path, output_prefix)`:
   \- Open the PDF once (to avoid reopening for each figure).
   \- For each Figure object, use its page number to get the page. Create a `fitz.Rect` from the figure’s bounding box coordinates (remember, original coordinates assume 72 DPI, which PyMuPDF uses by default for coordinate units).
   \- Use `page.get_pixmap(matrix=fitz.Matrix(1,1), clip=rect)` to get a pixmap of the figure region. (The matrix can scale the resolution if needed; at 72 DPI 1:1, the figure will render in roughly the size as in PDF).
   \- Save the pixmap to a PNG file. Construct the filename from `output_prefix` plus maybe the figure’s name or index. For example, if `output_prefix = "output/fig"` and this is Figure 5 on page 2, filename could be `output/fig_page2_fig5.png`. (Ensure unique naming if multiple PDFs or multiple figures; often original used a combination of PDF name and figure index.)
   \- If needed, allow different formats (the original mentioned support for jpeg, etc. If Pillow is installed, we could convert or just let user convert the PNG if needed).
   8.2. **Test Image Saving:** This can be done manually or with an automated test:
   \- If `test1.pdf` has a figure, run the renderer on the Figure object from detection and check that a file was created in a temp directory.
   \- Or simulate by creating a Pixmap directly of known size and testing the save function (not extremely necessary to test saving, as PyMuPDF’s internal functions are well-tested, but you can test that our code constructs correct file paths).
   8.3. **Integrate with CLI:** In `cli.py`, add an option like `--save-images` or detect if `-m` argument (prefix) is provided. If yes, after figure detection, call `figure_renderer.save_figure_images(figures, pdf_path, image_prefix)`.

9. **Finalize CLI Implementation**
   Bring everything together in `cli.py`:
   9.1. **Argument Parsing:** Use argparse to define options:
   \- Positional argument: input path (could be a single PDF file or a directory of PDFs, similar to original BatchCli behavior).
   \- `-d` or `--data-prefix`: path prefix for output JSON data files.
   \- `-m` or `--image-prefix`: path prefix for output figure image files (if provided, triggers saving images).
   \- Possibly `-s` for a stats JSON (like original had stat\_file.json for run statistics). We can include a simple count of figures extracted, etc., if needed.
   \- `-g` flag if we implement section title extraction (this could be an advanced/optional feature; if not doing section titles, skip it).
   9.2. **Main Routine Logic:** Pseudocode for `main()`:
   `python
        def main():
            args = parse_arguments()
            input_path = args.input
            pdf_files = []
            if os.path.isdir(input_path):
                pdf_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.lower().endswith('.pdf')]
            else:
                pdf_files = [input_path]
            stats = {"processed": 0, "figures_extracted": 0}  # For stat_file.json if needed
            for pdf in pdf_files:
                figures = process_pdf(pdf)  # call pipeline steps
                stats["processed"] += 1
                stats["figures_extracted"] += len(figures)              # Write JSON output
                data_out = f"{args.data_prefix}_{os.path.basename(pdf)}.json" if args.data_prefix else None
                if data_out:
                    with open(data_out, 'w') as f:
                        json.dump([fig.to_dict() for fig in figures], f, indent=2)
                else:                  # If no prefix given, print to stdout or use default naming
                    print(json.dumps([fig.to_dict() for fig in figures], indent=2))              # Save images if requested
                if args.image_prefix:
                    image_prefix = f"{args.image_prefix}_{os.path.basename(pdf).replace('.pdf','')}_figure"
                    figure_renderer.save_figure_images(figures, pdf, image_prefix)
            if args.stat_file:
                with open(args.stat_file, 'w') as f:
                    json.dump(stats, f, indent=2)
        `
   Where `process_pdf(pdf)` internally uses our modules:
   \- Parse PDF (`pdf_parser.parse_pdf`),
   \- Clean text (`formatting.filter_text_blocks`),
   \- Compute stats (`document_layout.compute_layout_stats`),
   \- Detect captions (`caption_detector.find_captions` then `caption_builder.build_captions`),
   \- Extract graphics (`graphic_extractor.find_graphics`),
   \- Classify text (`region_classifier.classify_text_lines`),
   \- Detect figures (`figure_detector.detect_figures`),
   and returns the list of Figure objects.
   9.3. **Ensure CLI Parity with Original:** Test the CLI on a sample PDF via command line:
   \- Running: `python -m pdffigures2_python.cli sample.pdf -d output/data/prefix -m output/image/prefix -s output/stat.json`
   should produce the JSON and images similar to using the original tool’s `FigureExtractorBatchCli`.
   \- Try without `-m` to ensure it works when not saving images (just produces JSON).
   \- If implementing visualization mode (the original `FigureExtractorVisualizationCli`), it could be an extra mode in CLI (e.g., `--visualize` flag). This would generate debug images or an interactive output. This is advanced, so it could be skipped initially or logged for future improvement. However, we can simulate a simple visualization by outputting annotated PDF pages (for instance, drawing boxes around detected figures and captions). This would use PyMuPDF’s drawing functions or output an HTML/markdown with positions, but given time, document that this can be done later.

10. **Testing and Verification**
    10.1. **Run Unit Tests:** Execute `pytest` in the project root. All tests in `tests/` should run. Initially, some might be placeholders; gradually implement them as you code each module. Achieve passing tests for each unit. For example:
    \- `pytest tests/test_caption_detection.py::test_simple_caption_line` to run a specific test.
    \- Add more tests if any bug is found during manual runs to prevent regression.
    10.2. **Real-world PDF Testing:** Take a few sample research PDFs (especially ones used in the original project evaluation if available) and run the CLI on them. Compare the JSON output to the original Java tool’s output (if you have it). The structure and values should match closely:
    \- The number of figures detected should be the same.
    \- Captions should match exactly (since we reused the model and similar logic, any differences in text extraction could cause minor variations – check if multi-line captions are captured fully, etc.).
    \- Figure and caption coordinates should be comparable (note: due to different PDF rendering libraries, coordinates might differ slightly by a few pixels; ensure they are in the same coordinate system (72 DPI) as the original).
    10.3. **Performance check (if needed):** If processing many PDFs, test the batch mode with, say, 10 PDFs in a directory. Use the `time` command to see that the processing is reasonably fast and that the multi-processing (if enabled) utilizes multiple CPU cores (see next section for concurrency setup). Adjust chunk sizes or number of processes if needed to optimize throughput.

By following these steps methodically, a junior developer will implement a fully functional Python version of PDFFigures2, with clarity at each stage and thorough testing to catch issues early. Each step builds on previous ones, ensuring that by the time we integrate everything in the CLI, all components have been vetted.

## 4. Environment Setup and Dependency Management

Setting up a reproducible environment is critical for this project. Below are explicit instructions for managing dependencies and running the application:

* **Python Version:** Use Python 3.8 or higher. This ensures compatibility with PyMuPDF and scikit-learn versions.
* **Virtual Environment:** (As done in step 1.1 above) create and activate a virtual env (`python3 -m venv venv`). This keeps project libraries isolated.
* **Installing Dependencies:** We maintain a `requirements.txt` with all needed packages and versions. To install everything in one go, run:

  ```bash
  pip install -r requirements.txt
  ```

  This will fetch PyMuPDF, scikit-learn, Pillow, etc. If you add or upgrade dependencies, update this file (you can use `pip freeze > requirements.txt` to capture the exact versions).
* **Alternative (Poetry):** If you prefer Poetry for dependency management, you can create a `pyproject.toml` with these dependencies under `[tool.poetry.dependencies]`. Running `poetry install` would then set up the env. However, using pip + requirements.txt is perfectly fine and more straightforward for a junior developer.
* **Activating the Environment:** Don’t forget to activate the venv every time you start a new terminal for development, otherwise Python won’t use the installed packages. The command `source venv/bin/activate` (or the Windows equivalent) should be run in your project folder each session.
* **Running the Application (CLI):** After implementing, to run the tool:

  * If installed as a package (via `pip install .` or using Poetry), you could have a console script `pdffigures2` available. If not, you can run it with the module syntax or via the CLI file. Two common methods:

    1. **Direct module execution:**

       ```bash
       python -m pdffigures2_python.cli /path/to/input.pdf -d output/data -m output/image
       ```

       This finds the `cli.py` in the package and runs the `main()` function with the given arguments.
    2. **Using the script file:** Alternatively, add a shebang to `cli.py` and make it executable. Or create a small wrapper in a `scripts/` directory that calls `pdffigures2_python.cli.main()`. For simplicity, using `python -m ...` is reliable.
  * **Command-line Examples:**

    * To process a single PDF and print result to console:
      `python -m pdffigures2_python.cli paper.pdf` (this will output JSON to stdout if no `-d` given).
    * To process a directory of PDFs, saving JSON and figures:
      `python -m pdffigures2_python.cli /myPapers/ -d results/data/prefix -m results/image/prefix -s run_stats.json`
      This will create JSON files like `results/data/prefix_paper1.json` for each PDF and images like `results/image/prefix_paper1_figure1.png`, and a summary stats file.
  * Ensure the usage message from argparse is clear. Run `python -m pdffigures2_python.cli -h` to see the help and verify all options are documented.
* **Checking Installation:** If you plan to distribute this, you might create a `setup.py` so that `pip install .` installs the package. In that case, verify that the `models/region_classifier_model.pkl` is included in the package (you might need to add it in `setup.py` or `MANIFEST.in` as data files). After installation, the usage would be simply calling the installed command if set up (e.g., `pdffigures2 /path/to/file.pdf -d ...` if we defined an entry point).
* **Troubleshooting Environment Issues:** If you encounter errors like “module not found,” double-check that the venv is active and that the package name is correct (`pdffigures2_python`). If PyMuPDF has installation issues (it may require some system libraries for MuPDF), consult PyMuPDF docs for platform-specific instructions (usually `pip` handles it, as it provides pre-built wheels for major OSes).
* **Upgrading Dependencies:** Over time, you may need to update libraries for bug fixes. Do so cautiously – run tests after each upgrade. For example, if upgrading PyMuPDF to a new major version, re-run extraction tests to ensure nothing changed in the API or results.

By following these steps, you will set up a clean development environment and be able to run the PDFFigures2 Python tool consistently. The `requirements.txt` ensures anyone else (or a deployment pipeline) can replicate the environment.

## 5. Reusing the Original Trained Model

An essential requirement is to **preserve the original trained model** from PDFFigures2 in our Python rewrite. Here’s how we achieve that:

* **Model File Acquisition:** The PDFFigures2 authors have provided a trained model (as mentioned in their paper/release). This model is likely a classifier for distinguishing body text vs figure text (used in RegionClassifier). We assume this model’s parameters are available (either included in the original repository or via their dataset). Obtain the model file:

  * If it’s in the original repository (sometimes as a resource file or produced by their SBT build), copy that file into our project’s `pdffigures2_python/models/` directory. It might have an extension like `.model`, `.dat`, or `.svm`. If it’s not directly usable in Python, see next point.
  * If the model is provided in another format (e.g., a Weka model or simply a list of parameters in code), you may need to **convert it**. One approach is to use the original training dataset with scikit-learn to train an equivalent model. However, since we want the exact same behavior, it’s best to extract the model coefficients. For example, if the original used a Linear SVM, find the weights and intercepts and rebuild a scikit-learn model with those (or use those in a custom classifier).
* **Storing the Model:** The model file is placed in our project under `pdffigures2_python/models/region_classifier_model.pkl`. We use a `.pkl` (pickle) or `.joblib` format because scikit-learn can easily load models in that form. If the original model was not in pickle format, perform a one-time conversion:

  * Write a small script (not part of final project) that loads the original model (e.g., if it was in Weka’s ARFF, use a converter, or if it was just a JSON of weights, use that) and then uses `joblib.dump()` to create `region_classifier_model.pkl`.
  * Verify the pickle loads correctly in Python.
* **Loading and Using the Model:** In `region_classifier.py`, load the model at module import or within a setup function:

  ```python
  import os
  import joblib
  MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "region_classifier_model.pkl")
  model = joblib.load(MODEL_PATH)
  ```

  This gives us a trained classifier object in Python. When classifying text lines, we extract features as per the model’s expectations and call `model.predict(features)`. Because we are using the exact model, the output labels will mirror the original tool’s logic.
* **Model Features Alignment:** It’s crucial that the features we compute for each text line match what the model was trained on. Check the original documentation or code for RegionClassifier to identify features. Common features might include:

  * Font size ratio (line font size / average font size in doc).
  * Font style (maybe binary flags for italic, bold).
  * Relative position (e.g., distance from top or bottom of page, or from nearest graphic).
  * Text content features (does it start with a capital letter, number, etc., which could differentiate captions vs normal sentences).
    We must implement the `extract_features` function to produce a feature vector in the same order and scale as the original. For instance, if the original normalized font sizes or used log values, do the same.
* **Where the Model Lives in Project:** We keep it in the `models/` subdirectory of the package so it gets installed alongside the code. In Python packaging, we may need to include it as package data (in setup or MANIFEST). At runtime, we reference it via a path constructed relative to `__file__` (as shown above) so it works regardless of current working directory.
* **Calling the Model:** Within `classify_text_lines`, after we compute the feature array (shape `[n_lines, n_features]`), do:

  ```python
  predictions = model.predict(feature_array)
  ```

  The result is an array of labels. If the model was a binary classifier, we might map label `1` -> "Other", `0` -> "BodyText" (or vice versa, depending on how it was trained). Use the original code or README to confirm which label corresponds to figure-related text. It’s likely that “Other” = figure/table text got the positive class. You can verify by checking a known caption: running it through predict and seeing if it returns 1 (then 1 = Other).
* **Verification:** Test the model’s integration by running the classifier on known inputs (as we did in step 6.4 of the guide). Additionally, once the whole pipeline is running on a real PDF, check that the classifier isn’t misbehaving (e.g., if it mislabels a lot of normal body text as Other, then maybe our feature alignment is off). Since we’re using the exact original model, any misclassifications would also have been present in the original tool – the goal is to match, not necessarily to “fix” those, to preserve functionality. If needed, adjust only the feature computation, not the model.
* **No Retraining:** We explicitly **do not retrain** the model – we reuse the trained parameters to have identical performance as PDFFigures2. This saves time and ensures the output quality is proven (the original had \~94% precision at 90% recall on their dataset, which we want to maintain).
* **Future Model Updates:** Document in the README how a user could update the model (for instance, if they have new training data). They could retrain a classifier in Python using scikit-learn and drop in a new `region_classifier_model.pkl`. But by default, we ship with the original.

In summary, the model acts as a black-box component in our Python code – we feed it the same kind of inputs and expect the same outputs. Its presence is in the `models` folder, and its usage is encapsulated in `region_classifier.py`. This way, the heavy lifting (distinguishing figure text from main text) is done exactly as before, yielding the same figure identification results.

## 6. JSON Output Format Matching Original

We must ensure that the output JSON from the Python version exactly matches the format of the original PDFFigures2, so that any downstream tools or analyses see no difference. The structure (as described in the original README) should be a list of figure objects, each with specific fields. Here is the required JSON format and how to produce it:

* **Output as a JSON Array:** The top-level output for each PDF will be a JSON array (list) of figure objects. If the CLI processes multiple PDFs, typically it creates one JSON file per PDF (the original `-d` option saved one JSON per PDF file, named with a prefix).
* **Fields for Each Figure Object:** Each figure in the list has the following keys (exact naming and data types must match):

  1. `"page"`: (Integer) The 0-based page index where the figure is found.
  2. `"regionBoundary"`: (Object) The bounding box of the figure on the page. This can be represented with keys `"x1", "y1", "x2", "y2"` (top-left and bottom-right coordinates) or `"x", "y", "width", "height"`. We need to confirm how the original JSON structured it. Often, PDF figures tools use `x1,y1,x2,y2`. Given the README description uses top-left as origin and pixel coords at 72 DPI, we will output coordinates in that system. For clarity, we can output as:

     ```json
     "regionBoundary": { "x": <left>, "y": <top>, "width": <width>, "height": <height> }
     ```

     where (x, y) is top-left corner. This is an interpretation; if the original used a different naming, use that. (We might peek at an example output from PDFFigures2. If not available, this approach is clear.)
  3. `"caption"`: (String) The full caption text of the figure. This should include figure number and description exactly as in the PDF (e.g., `"Figure 1: Sample Diagram showing ..."`). Maintain all punctuation and wording from the PDF.
  4. `"captionBoundary"`: (Object) The bounding box of the caption text, in the same format as regionBoundary. This box covers the caption area (often below the figure).
  5. `"name"`: (String) The figure’s identifier as deduced from the caption. Typically this is the number or label of the figure. For example, caption "Figure 1: ..." -> name is `"1"`. If a caption was "Figure A1", name would be `"A1"`. We extract this by removing non-alphanumeric from the caption title. (The original note: usually a number, but could be something else for special cases.)
  6. `"figureType"`: (String) Either `"Figure"` or `"Table"`, indicating what the caption labeled it as. We determine this by checking the beginning of the caption string – if it starts with "Table", then figureType is "Table", otherwise "Figure". (This covers cases like "Figure", "Fig.", etc., all map to "Figure"). The original explicitly labels tables vs figures in output.
  7. `"text"`: (String) Any text content that is inside the figure region. This includes text that was part of the figure (for example, if the figure is a diagram with embedded text labels, or a table’s cell text, those would be extracted). In our pipeline, we can gather this by taking all text lines classified as Other (non-body) that lie within the figure’s regionBoundary (excluding the caption text itself). Concatenate them or structure them appropriately. The original might output this as one string (possibly concatenated with newlines or spaces). This field might be empty if the figure has no readable text inside (like a pure photograph).
* **Example JSON Entry:** For clarity, here’s an example (this is illustrative; actual coordinates depend on PDF content):

  ```json
  {
    "page": 0,
    "regionBoundary": { "x": 100, "y": 150, "width": 400, "height": 300 },
    "caption": "Figure 2: Architecture of the proposed model.",
    "captionBoundary": { "x": 100, "y": 460, "width": 380, "height": 40 },
    "name": "2",
    "figureType": "Figure",
    "text": "Input Layer\nHidden Layer\nOutput Layer"
  }
  ```

  This indicates Figure 2 on page 1 (0-indexed) spans a region on the page, has a caption, and contains some text labels inside the figure (here three lines inside the figure diagram).
* **Consistency with Original:** It’s important to format exactly. For instance, if the original JSON used `"figType"` instead of `"figureType"` or used a list for region boundary, we should do the same. If possible, run the original Java tool on a PDF and observe the JSON keys and format, then mirror that.
* **Serializing in Code:** Use Python’s built-in `json` module. You can add a method `to_dict()` in the Figure class to produce a dict with these keys. Then:

  ```python
  import json
  figures_data = [fig.to_dict() for fig in figures]
  json.dump(figures_data, output_file, indent=2)
  ```

  Use `indent=2` for readability (original likely didn’t indent when writing to file, but indenting doesn’t affect correctness; we can omit indent if exact match is needed).
* **Coordinate Units:** As noted, coordinates are in PDF points (1/72 inch) with origin (0,0) at top-left of the crop box. PyMuPDF by default gives coordinates in this space, so we can use them directly. Just ensure not to confuse with any pixel resolution from rendering (we are not using rendered image coordinates, but PDF’s own coordinate system).
* **Order of Figures:** The output list can be in the order figures are found in the document (which is usually top-to-bottom by page, and within a page, by caption occurrence). The original likely outputs in reading order of captions. Our detection likely finds captions in order anyway.
* **Validation:** After generating JSON for a test PDF with the Python tool, compare field-by-field with the original tool’s JSON for the same PDF (if available). They should be identical in content. Minor differences such as whitespace in the caption text (e.g., PDF extraction might add a newline in the caption if line-wrapped) should be addressed: we want the caption text exactly as in the PDF visually (the original likely reconstructed multi-line captions into a single line string). Our `caption_builder` already handles that by concatenation.
* **Documenting the Format:** In the README.md, include an explanation of the JSON format and possibly a small snippet as example, so users understand it without referencing the original README. This includes explaining the coordinate system (mention 72 DPI points, which is the PDF standard coordinate space).

By matching this JSON format, users can switch from the old tool to the new Python tool seamlessly – their downstream code expecting fields like `"caption"` or `"regionBoundary"` will continue to work without modifications.

## 7. Concurrent PDF Processing (Multiprocessing/Multithreading)

To improve performance for batch processing many PDFs, we will incorporate **multiprocessing** to utilize multiple CPU cores (the original Batch CLI supported multi-threading for speed). In Python, due to the GIL, true parallelism for CPU-bound tasks is achieved with multiprocessing (separate processes), or using threads if the I/O is the bottleneck. Here’s how we add concurrency:

* **When to Use Concurrency:** If the user supplies a directory of PDFs, and there are multiple files to process, we can process them in parallel. Each PDF processing is largely independent of others (no shared state except writing outputs, which we handle carefully).
* **Multiprocessing with `concurrent.futures`:** We can use the `ProcessPoolExecutor` for simplicity. In `cli.py`, after gathering the list of PDF files to process (as in step 9.1), do:

  ```python
  import concurrent.futures
  def process_and_save(pdf_path):
      figures = process_pdf(pdf_path)
      # (Write JSON and images for this PDF as done in main loop earlier)
      return len(figures)

  if args.jobs and args.jobs > 1:
      with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as executor:
          results = list(executor.map(process_and_save, pdf_files))
      total_figs = sum(results)
  else:
      # single-threaded processing (as before)
  ```

  Here, `args.jobs` could be an optional argument for number of parallel processes (similar to a `-j` flag). If not provided, we default to, say, use all available cores.
* **Managing Shared Resources:**

  * Each process will open the PDF and perform extraction. PyMuPDF can be used in multiple processes, but note that large model loading in each process is overhead. However, since the model is \~ few MB at most, it’s okay. Alternatively, one could load the model outside the pool and pass it, but joblib model can’t be easily pickled to send to workers. Better to just let each worker load it once at start (the `region_classifier.model` load call will happen on first use in that process).
  * Ensure that writing to files doesn’t collide: Since each PDF has unique output filenames (we include PDF name in the prefix), multiple processes writing different files is fine. Just avoid two processes writing the same `stat_file.json`. For stats, it's easier to collect results from each future as shown and aggregate in the main process.
* **Multi-threading Consideration:** Alternatively, one might try `ThreadPoolExecutor`, but since PDF parsing and our pipeline are CPU-heavy (text extraction, model prediction), threads would be limited by GIL. PyMuPDF does release GIL during some operations (like rendering images), but much of our pipeline (Python-level logic, scikit model prediction) will use CPU Python code, so process pool is safer for speedup.
* **Controlling Parallelism:** Provide an option to user for number of workers. The original might not have exposed thread count (it may have auto-chosen or used a fixed number). We can introduce an argument `-j N` (like make) or `--jobs N`:

  * `-j 4` means use 4 processes.
  * If not specified, default to number of CPUs or a sensible default (maybe default 2 or 4 to avoid overloading system by default).
* **Implementing in Code:** Wrap the parallel logic so that if only one PDF or jobs=1, it doesn’t spawn unnecessary processes:

  ```python
  if len(pdf_files) > 1 and args.jobs != 1:
      max_workers = args.jobs or os.cpu_count() or 2
      with ProcessPoolExecutor(max_workers=max_workers) as executor:
          for pdf_path, fig_count in zip(pdf_files, executor.map(process_pdf, pdf_files)):
              write_output(pdf_path, fig_count)  # handle file writing in main to avoid file conflicts
  else:
      for pdf_path in pdf_files:
          fig_count = process_pdf(pdf_path)
          write_output(pdf_path, fig_count)
  ```

  Here, `process_pdf` would return the Figure objects or count, and `write_output` handles writing JSON and images. Alternatively, do everything (process and write) inside the worker function, but be mindful of sharing the `args` for output prefixes (we can capture those in a closure).
* **Thread Safety:** Most of our modules are functional (they process data without global state), so running them in parallel on separate data is safe. PyMuPDF objects cannot be shared across processes (each process must open its own PDF), which we are doing by opening inside `process_pdf`.
* **Testing Concurrency:** To test, create a scenario with multiple small PDFs. Run the CLI with `-j 2` (for example) and time it vs `-j 1`. Also, insert debug prints or logging to verify that multiple processes are indeed running (you can print the process PID in `process_pdf` to see different PIDs). Check that all output files are produced correctly.
* **Multiprocessing on Windows:** If using Windows, the `ProcessPoolExecutor` requires the `if __name__ == "__main__":` guard in the `cli.py` when launching, to avoid recursive process spawning. Since we likely call `cli.py` via `python -m`, we should ensure that our code is inside a `main()` function and that at the bottom we have:

  ```python
  if __name__ == "__main__":
      main()
  ```

  This way, on Windows it won’t re-import the module in each subprocess in a way that calls main again erroneously. This is a common gotcha.
* **Memory Considerations:** Each process will load the PDF and the model. If processing many large PDFs or using many processes, watch memory usage. Typically, text extraction is not extremely memory heavy, and our model is small, so it's fine. But if needed, the `max_workers` could default to a smaller number or user-defined to allow tuning.
* **Timeouts:** If some PDF takes too long or hangs (perhaps due to a malformed PDF), it might stall a worker. The original mentioned the ability to timeout threads. We can implement timeouts in the executor by using `future.result(timeout=seconds)` for each future if needed. Alternatively, since PDFFigures2 runs generally should be quick (a few seconds per PDF), we might not implement explicit timeouts unless needed.
* **Graceful Termination:** Ensure that if the user presses Ctrl+C, the program terminates all worker processes. The `ProcessPoolExecutor` should handle shutdown on main process interrupt, but be aware that KeyboardInterrupt might not immediately stop child processes. In testing, verify that Ctrl+C stops everything; if not, consider capturing KeyboardInterrupt and calling `executor.shutdown(cancel_futures=True)`.

By including multiprocessing, users processing a batch of PDFs will see a significant speed-up on multi-core machines, similar to the original’s multithreaded batch mode. This is especially beneficial when extracting figures from hundreds of PDFs in one go.

## 8. Unit Testing with PyTest (and Sample Test)

We will use **pytest** to structure and run tests. The test suite not only validates correctness during development but also serves as an additional documentation for usage. Here’s how we set up and organize testing, along with a sample test case:

* **Test Organization:** Tests are in the `tests/` directory, and each module in our code has a corresponding test module:

  * `test_text_extraction.py` for `text_extraction.py`,
  * `test_caption_detection.py` for `caption_detector.py`, etc.
  * Integration tests in `test_integration.py` covering end-to-end flows.
* **PyTest Conventions:** Each test file is named `test_*.py`, and test functions within are named `test_*`. This way, pytest auto-discovers them.
* **Fixtures:** We can use pytest fixtures for reusable setup. For instance, a fixture to load a small PDF from `tests/sample_papers/` for integration tests:

  ```python
  import pytest
  import os
  @pytest.fixture
  def simple_pdf_path():
      return os.path.join(os.path.dirname(__file__), "sample_papers", "test1.pdf")
  ```

  Then test functions can accept `simple_pdf_path` as an argument and get that value.
* **Sample Test File (Caption Detection):** Below is an example of a test file content, `tests/test_caption_detection.py`. It tests the caption detection and building functionality:

  ```python
  import pytest
  from pdffigures2_python import caption_detector, caption_builder, document_layout
  from pdffigures2_python.common import TextLine, Caption  # assuming we have a common definitions module for data classes

  def test_single_line_caption_detection():
      # Simulate a typical caption line
      line = TextLine(x=50, y=500, width=400, height=12,
                      text="Figure 1: An example figure caption.",
                      font_size=10)
      # Document average font size is larger (meaning this is smaller text)
      stats = document_layout.DocumentStats(avg_font_size=12, median_font_size=12)
      captions = caption_detector.find_captions([line], stats)
      assert len(captions) == 1
      caption = captions[0]
      assert isinstance(caption.text, str)
      assert caption.text.startswith("Figure 1:")
      assert caption.page == line.page if hasattr(line, "page") else 0

  def test_multi_line_caption_building():
      # Simulate a caption split into two lines in PDF
      line1 = TextLine(x=50, y=300, width=450, height=12,
                       text="Figure 2: This is a long caption that goes on", font_size=9)
      line2 = TextLine(x=50, y=312, width=450, height=12,
                       text="to a second line of the caption.", font_size=9)
      stats = document_layout.DocumentStats(avg_font_size=11, median_font_size=11)
      captions = caption_detector.find_captions([line1, line2], stats)
      # find_captions should identify line1 as a caption start
      assert len(captions) == 1 and captions[0].text.startswith("Figure 2:")
      # Now build full caption
      full_caption = caption_builder.build_caption(captions[0], [line1, line2])
      # After building, the caption text should include both lines
      assert "goes on to a second line" in full_caption.text
      # The bounding box height should cover both lines (should be >= 24 in this case)
      assert full_caption.bbox["height"] >= (line2.y + line2.height - line1.y)
  ```

  *(This assumes we have a `TextLine` data class with attributes like x, y, width, height, font\_size, and possibly page. Also `build_caption` might need the list of all lines to know the continuation. The exact implementation of `build_caption` could differ, but the test is written to match our plan.)*

  This test ensures that a single-line caption is detected and that multi-line captions are concatenated properly with their bounding box adjusted.
* **Running Tests:** We instruct the developer to run `pytest` in the project directory. PyTest will output any failures with a traceback. All tests should pass before considering the implementation complete.
* **Writing Additional Tests:** Encourage writing tests for:

  * `graphic_extractor` (e.g., if we have an image in a test PDF, ensure its bbox is found).
  * `region_classifier` (this one is trickier because it depends on the model; but we can test that the model loads and that obvious inputs produce expected labels as done in step 6.4).
  * `figure_detector` logic (the synthetic test as shown in step 7.3).
  * CLI end-to-end (using Python’s `subprocess` module to call the CLI with a sample PDF and then checking the output file exists). For example:

    ```python
    import subprocess, json, os
    def test_cli_end_to_end(simple_pdf_path, tmp_path):
        output_json = tmp_path / "out.json"
        subprocess.run(["python", "-m", "pdffigures2_python.cli", simple_pdf_path, "-d", str(tmp_path/"out")], check=True)
        # The CLI should produce a file named out<PDFName>.json
        assert output_json.exists()
        data = json.loads(output_json.read_text())
        assert isinstance(data, list)
        # if we know how many figures in simple_pdf, assert len(data) == expected_count
    ```

    This kind of test actually runs the whole program as a black box.
* **Test Data:** For tests to be meaningful, especially integration, we need at least one sample PDF in `tests/sample_papers`. Create a minimal PDF (you can do this by hand or using a tool) that includes a figure. For example, create a PDF with one page, insert an image (just a placeholder) and below it a text "Figure 1: Test caption." You can do this with LaTeX or even Word to PDF. This PDF, when run through our tool, should yield one figure with that caption. We then know expected values to assert (e.g., caption text exactly, page=0, figureType="Figure", etc.).
* **Continuous Testing:** Advise the developer to run tests frequently while building each component. For instance, when finishing `caption_detector.py`, run `pytest tests/test_caption_detection.py` to see if it passes. This will catch issues early.
* **Coverage:** Aim to cover each major function with at least one test. This not only checks correctness but also demonstrates how to use the function (useful for the junior dev to understand the intended behavior).
* **PyTest Usage:** No need to write a main or anything for tests; simply running `pytest` will find and execute them. We included `pytest` in requirements to ensure the dev has it.

By following this testing strategy, we ensure the refactored code works as intended and matches the original’s outputs. The tests serve as both verification and as an additional form of documentation (showing examples of inputs/outputs for various functions).

Finally, once all tests pass and sample PDFs yield correct results, the junior developer can be confident that the Python rewrite of PDFFigures2 is successful and fully functional. Each requirement – CLI usability, same output format, use of original model – will have been validated through these tests and comparisons with the original tool’s behavior.

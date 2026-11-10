# Mobile Sales Data Analysis

This repository contains the source PDF supplied for the assignment, the analysis script, and the PowerPoint presentation.

## Project files
- `dataset/Mobile_Sales_Data_Source.pdf` — original 3-page dataset document supplied for the task.
- `src/analyze_mobile_sales.py` — Python analysis for the 10 assignment questions.
- `Mobile_Sales_Analysis_Presentation.pptx` — presentation created from the available source.
- `requirements.txt` — Python dependencies.

## Important dataset note
The supplied source is a PDF, not an original spreadsheet/CSV. Some table cells are visually merged or misaligned in the PDF extraction. To avoid presenting a guessed or corrupted CSV as the original dataset, the source PDF is preserved unchanged. Before running the script, export or carefully transcribe the table into `dataset/mobile_sales.csv` with these exact column headers:

`Brands, Models, Mobile, Memory, Storage, Selling Price, Original Price, Discount, Rating, R`

## Run the analysis
```bash
pip install -r requirements.txt
python src/analyze_mobile_sales.py dataset/mobile_sales.csv
```

The script creates an `outputs/` folder with CSV results for questions 1–10.

## Value-for-money score
The script uses a transparent weighted percentile score:
- Customer rating: 40%
- Discount percentage: 20%
- Storage: 20%
- Memory: 10%
- Affordability (lower selling price): 10%

The score is a project-defined comparison, not an industry-standard measure.

## Note about the `R` column
The source contains a column named `R`, but its definition is not included in the PDF. The script treats it as the supplied class label for exploratory analysis. Confirm its meaning with the dataset provider before making a final classification claim.

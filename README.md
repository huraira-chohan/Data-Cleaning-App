# 🧹 Data Cleaning Application

A comprehensive, modular Streamlit application designed for data scientists and students to clean, process, and prepare messy datasets with ease.

## Features

### 📤 Data Loading
- Support for multiple file formats: CSV, Excel (.xlsx, .xls), JSON
- Quick data preview and statistics
- Automatic detection of missing values and duplicates

### 📊 Exploratory Data Analysis (EDA)
- Statistical summary of your data
- Distribution analysis with interactive visualizations
- Correlation matrix heatmaps
- Missing data visualization

### ⚠️ Missing Values Handling
- Multiple imputation strategies:
  - Drop rows with missing values
  - Drop columns with high missing percentages
  - Fill with mean, median, or mode
  - Forward/backward fill
  - KNN Imputation
  - Custom value filling

### 🔄 Duplicate Handling
- Identify duplicate rows and values
- Remove duplicates with flexible criteria
- Keep first/last duplicate options
- Visualize duplicate patterns

### 📈 Outlier Detection & Treatment
- Multiple detection methods:
  - IQR (Interquartile Range) method
  - Z-Score method
  - Isolation Forest
  - Visual inspection with plots
- Treatment options: Remove, cap, or replace with median

### 🏷️ Data Type Management
- Auto-detect and convert data types
- Manual type conversion
- String operations (trim, case conversion, special character removal)
- DateTime parsing

### ⚡ Feature Engineering
- Create new features from existing columns
- Binning/Discretization (equal width and equal frequency)
- Normalization (Min-Max scaling)
- Standardization (Z-score scaling)
- Log transformations
- Categorical encoding (Label & One-Hot)

### 💾 Data Export
- Multiple export formats: CSV, Excel, JSON, Parquet
- Side-by-side export of original and cleaned data
- Automatic data cleaning report generation

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download the repository**
   ```bash
   cd "Data Cleaning App"
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** (usually opens automatically at `http://localhost:8501`)

3. **Follow the workflow:**
   - Load your messy dataset
   - Explore data with EDA tools
   - Process data step-by-step through various cleaning modules
   - Export your cleaned dataset

## Project Structure

```
Data Cleaning App/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
└── modules/
    ├── __init__.py                 # Module initialization
    ├── data_loader.py              # Load data from various formats
    ├── eda.py                      # Exploratory Data Analysis
    ├── missing_values.py           # Handle missing values
    ├── duplicates.py               # Handle duplicate records
    ├── outliers.py                 # Detect and handle outliers
    ├── data_types.py               # Fix and convert data types
    ├── feature_engineering.py      # Feature engineering tools
    └── data_export.py              # Export processed data
```

## Module Descriptions

### data_loader.py
Handles file upload and initial data exploration. Supports CSV, Excel, and JSON formats.

### eda.py
Provides interactive exploratory data analysis including statistics, distributions, correlations, and missing data patterns.

### missing_values.py
Offers 9+ strategies for handling missing values, from simple deletion to advanced KNN imputation.

### duplicates.py
Identifies and removes duplicate rows with customizable criteria.

### outliers.py
Detects outliers using multiple methods (IQR, Z-Score, Isolation Forest) and provides treatment options.

### data_types.py
Manages data type conversions, string operations, and automatic type detection.

### feature_engineering.py
Creates new features, applies scaling transformations, encoding, and binning operations.

### data_export.py
Exports cleaned data in multiple formats with automatic report generation.

## Example Workflow

1. **Load** → Upload your messy CSV file
2. **Explore** → Run EDA to understand data patterns
3. **Clean** → Handle missing values and duplicates
4. **Process** → Fix data types and handle outliers
5. **Engineer** → Create new features if needed
6. **Export** → Download cleaned dataset

## Supported Data Formats

**Input:** CSV, Excel (.xlsx, .xls), JSON

**Output:** CSV, Excel, JSON, Parquet

## Technologies Used

- **Streamlit** - Web framework for data apps
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning algorithms
- **Plotly** - Interactive visualizations
- **SciPy** - Scientific computing

## Tips for Best Results

1. **Start with EDA** - Understand your data before cleaning
2. **Process step-by-step** - Don't rush through cleaning steps
3. **Keep original data** - Always compare original vs. cleaned
4. **Validate changes** - Review data after each transformation
5. **Use appropriate methods** - Different data requires different strategies

## Troubleshooting

### Common Issues

**"File format not supported"**
- Ensure your file is CSV, Excel, or JSON
- Check file encoding (UTF-8 recommended)

**"No numeric columns found"**
- Some operations require numeric data
- Check data types in the Data Types tab

**"Conversion failed"**
- Ensure column contains compatible data for conversion
- Check for special characters or malformed values

## Future Enhancements

- [ ] Database connection support
- [ ] Advanced time series cleaning
- [ ] Text data cleaning tools
- [ ] Custom transformation templates
- [ ] Data quality metrics
- [ ] Automated cleaning recommendations
- [ ] Multi-file batch processing

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the documentation or create an issue in the repository.

---

**Happy Data Cleaning! 🧹✨**

## Deployment (Docker)

Quick steps to run the app in Docker locally:

1. Build the Docker image:

```powershell
docker build -t data-clean-app:latest .
```

2. Run with Docker (port 8501):

```powershell
docker run -p 8501:8501 data-clean-app:latest
```

Or use docker-compose:

```powershell
docker-compose up --build
```

Notes:
- The app exposes port `8501`. Adjust `.streamlit/config.toml` or environment variables for production.
- Add secret values to `.streamlit/secrets.toml` (do not commit secrets to the repo).

Recommended next steps for production:
- Authentication: set credentials in `.streamlit/secrets.toml` (see `.streamlit/secrets.toml.example`). The app uses a simple login prompt in the sidebar.
- Health endpoint: the repo includes a `health_app.py` FastAPI endpoint available at `/health` on port `8000` when running with `docker-compose`.
- Configure HTTPS/SSL (via reverse proxy like Nginx or a cloud load balancer).
- Add logging and monitoring.

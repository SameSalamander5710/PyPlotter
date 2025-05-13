# PyPlotter

PyPlotter is a Python application that allows users to create customizable bar plots with individual data points, mean, and error bars (SEM or SD). The app provides a graphical user interface (GUI) for selecting plot options such as aggregation function, error type, y-axis scale, and logarithmic base.

## Features
- Generate bar plots with individual data points.
- Choose between mean and median as the aggregation function.
- Select error bars: Standard Error of the Mean (SEM) or Standard Deviation (SD).
- Customize the y-axis scale (Linear or Logarithmic) and specify the logarithmic base.

## Setup Instructions

### 1. Create a Virtual Environment
Run the following command to create a virtual environment:
```bash
python -m venv venv
```

### 2. Activate the Virtual Environment
- On **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```
- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
Install the required Python packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## Usage

1. **Run the Application**:
   Start the application by running the following command:
   ```bash
   python PyPlotter.py
   ```

2. **Copy Data**:
   Copy wide-format data (e.g., from Excel) to your clipboard. The data should have column headers and numerical values.

3. **Customize the Plot**:
   - Use the GUI to select the aggregation function (Mean or Median).
   - Choose the error type (SEM or SD).
   - Set the y-axis scale (Linear or Logarithmic) and specify the logarithmic base if needed.

4. **Generate the Plot**:
   Click the "Generate Plot" button to create and view the plot.
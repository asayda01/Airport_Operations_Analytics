# Airport Operations Analytics: Screening Machine Performance Analysis

## Overview
This repository contains a comprehensive analysis of the performance of Hold Baggage Screening X-ray Machines at **Terminal 3** during the summer season. The analysis is based on bag throughput data for the month of **July**, focusing on identifying **performance challenges, bottlenecks, and opportunities for optimization**.

### Deployed App
The analysis is available as an interactive **Streamlit app**, accessible at:

🔗 [Airport_Operations_Analytics](https://cem-saydam-airport-operations-analytics.streamlit.app/)

🔗 [https://cem-saydam-airport-operations-analytics.streamlit.app/](https://cem-saydam-airport-operations-analytics.streamlit.app/)
---
## Dataset Description
The dataset used for this analysis includes the following key attributes:

- **bag_scan_timestamp**: Date and time a bag was seen at a machine.
- **bag_license_plate**: Unique identifier for a bag.
- **scan_machine_id**: Unique identifier for a machine.
- **scan_machine_cluster**: The cluster each machine belongs to.
- **scan_machine_level**: The current screening level the bag is being processed at.
- **scan_machine_result**: The screening result of the bag at its current screening level.
- **scan_machine_result_reason**: Further detail on the screening result of the bag.

The analysis addresses several key questions, including:

✅ **Throughput and load distribution**

✅ **Peak days and times for bag screening**

✅ **System bottlenecks and time-out situations**

✅ **Machine and cluster utilization**

✅ **Screening escalations and Level 2 analysis**

✅ **Single vs. multiple screenings**

✅ **Decision-making times**

✅ **Operator interventions**

---
## Repository Structure

```
├── Cem_Saydam_Streamlit.py       # Main Streamlit app script
├── Xray_Scan_Data_Jul_2022.csv    # Dataset used for analysis
├── company_logo.JPG               # Company logo used in the app
├── README.md                      # This file
└── requirements.txt               # Dependencies required to run the app
```

---
## How to Run the App Locally
Follow these steps to run the analysis locally:

### 1️⃣ Clone the repository:
```sh
git clone https://github.com/asayda01/Airport_Operations_Analytics
cd Airport_Operations_Analytics
```

### 2️⃣ Install dependencies:
```sh
pip install -r requirements.txt
```

### 3️⃣ Run the Streamlit app:
```sh
streamlit run streamlit_app.py
```

### 4️⃣ Access the app:
Open your web browser and navigate to:
[http://localhost:8501](http://localhost:8501)

---
## Key Insights
### **1. Throughput and Load Distribution**
- **Daily Throughput**: Identifies peak days and overall daily bag processing capacity.
- **Hourly Throughput**: Highlights the busiest hours for screening.
- **15-Minute Intervals**: Detects short-term spikes in activity.

### **2. Peak Days of Week Analysis**
- Determines the busiest days and suggests operator schedule optimization.

### **3. System Bottlenecks and Time-Outs**
- Assesses machine clusters prone to time-outs.
- Identifies peak times for system slowdowns.

### **4. Machine and Cluster Utilization**
- Evaluates equitable distribution of bag processing.
- Identifies machines handling excessive loads and investigates malfunctions.

### **5. Screening Escalations and Level 2 Analysis**
- Analyzes escalation rates to Level 2 screening.
- Detects trends in escalation over time and across machines.

### **6. Single vs. Multiple Screenings**
- Investigates unnecessary bag recirculations.
- Examines causes of redundant screenings.

### **7. Decision-Making Times**
- Measures the average time operators spend on screening decisions.
- Analyzes time intervals between consecutive bag scans.

### **8. Operator Interventions**
- Identifies the percentage of bags requiring manual review.
- Examines intervention trends by machine and time of day.

---
## **Visualizations**
The app includes interactive visualizations such as:

📊 **Bar Charts** - Throughput by day, hour, and 15-minute intervals.

📈 **Line Charts** - Time-based trends in Level 2 escalations and recirculations.

🥧 **Pie Charts** - Distribution of screening results and operator interventions.

📦 **Box Plots** - Time spent per bag at each machine.

🔥 **Heatmaps** - Machine and cluster performance visualization.

---
## **Recommendations**
Based on the analysis, we provide actionable insights to optimize the screening process:

✅ **Optimizing Staffing** - Align operator schedules with peak screening times.

✅ **Improving Machine Calibration** - Reduce false positives and time-outs.

✅ **Enhancing Maintenance** - Prioritize machines with higher malfunction rates.

✅ **Training Operators** - Reduce intervention times and increase efficiency.

---
## **Contributing**
Contributions are welcome! If you have suggestions or improvements, please **open an issue** or **submit a pull request**.

---
## **License**
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---
## **Acknowledgments**
- **[Company Name Removed]** - For providing the dataset and supporting this analysis.
- **Streamlit** - For the framework enabling interactive data exploration.

---

🔗 [Airport_Operations_Analytics](https://cem-saydam-airport-operations-analytics.streamlit.app/)

🚀 **Thank you for visiting! Feel free to explore, contribute, and improve the analysis!**


# 🔍 Automated Job Alert System  

<img width="703" alt="Screenshot 2025-02-21 at 3 30 43 AM" src="https://github.com/user-attachments/assets/0a331c31-cfd8-4e98-8e52-6f130652f0c4" />


---

### 📖 **What This Project Does**  
This automated system **scrapes entry-level Data Scientist jobs** from Indeed and LinkedIn daily, filters them by experience level, and emails you a curated list. Kinda Obsolete with the rise of AI now.

---

### 🛠 **Technologies Used**  
- **Python** (with `Selenium` and `BeautifulSoup` for scraping)  
- **Mailjet API** for email alerts  
- **Google Cloud Platform (GCP)** for server hosting  
- **Cron Jobs** for daily automation  

---

### ☁️ **GCP Server Setup**  
I deployed this script to a GCP virtual machine instance and:  
1. Configured a daily cron job to run the script automatically  
2. Secured API credentials using environment variables  
3. Monitored logs via Google Cloud Operations

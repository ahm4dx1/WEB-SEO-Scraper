# WEB-SEO-Scraper 🚀

A Python tool to scrape website data, extract SEO insights, and gather social media/contact details.

## 📌 Features
- ✅ Extracts emails, phone numbers, and social media links from websites  
- ✅ Scrapes SEO data such as meta tags, page speed, and structure  
- ✅ Saves results in organized JSON files per domain  

## 🛠 Installation
1. **Clone the repository**  
   ```bash
   git clone https://github.com/YOUR_USERNAME/WEB-SEO-Scraper.git
   cd WEB-SEO-Scraper
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the input file**  
   - Add website URLs (one per line) in `websites.txt`  

## 🚀 Usage
Run the scraper:  
```bash
python seo_scraper.py
```

## 📂 Output Structure
```
WEB-SEO-Scraper/
│── websites.txt  # List of websites to scrape
│── seo_scraper.py  # Main script
│── scraped_data/
│   ├── example1.com/
│   │   ├── site_urls.json  # Extracted emails, socials, links
│   │   ├── seo_data.json  # SEO analysis results
│   ├── example2.com/
```

## 📋 Requirements
- Python 3.x  
- Required modules:  
  ```bash
  pip install requests beautifulsoup4 fake-useragent tldextract lxml
  ```

## 🤝 Contributing
Feel free to fork, modify, and submit a pull request! 🚀  



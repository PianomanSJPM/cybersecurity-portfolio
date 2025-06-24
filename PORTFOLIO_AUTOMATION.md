# Portfolio Automation Guide

## 🚀 Automated Document Management

Your portfolio now includes an automated tool to easily add new documents! This saves you time and ensures everything is properly organized.

## 📋 How to Use the Automated Tool

### **Quick Start**
```bash
cd /Users/stephenmiller/Desktop/Cybersecurity/Portfolio
python3 add_document.py
```

### **Step-by-Step Process**

1. **Run the script**: `python3 add_document.py`

2. **Select a category** (1-7):
   - 1. Incident Response
   - 2. Vulnerability Assessment  
   - 3. Access Control
   - 4. Network Security
   - 5. Tools & Automation
   - 6. Certifications
   - 7. Resume

3. **Provide file information**:
   - Source file path (where your document is located)
   - Brief description of the document
   - Skills demonstrated (comma-separated)

4. **Choose Git operations**:
   - Yes: Automatically commit and push to GitHub
   - No: Manual commit later

## 🎯 **What the Tool Does Automatically**

✅ **Copies your file** to the correct category folder  
✅ **Updates the category README** with project details  
✅ **Updates your skills matrix** with new skills  
✅ **Commits changes to Git** (optional)  
✅ **Pushes to GitHub** (optional)  
✅ **Updates your live portfolio** at https://pianomansjpm.github.io/cybersecurity-portfolio  

## 📝 **Example Usage**

```bash
$ python3 add_document.py

🛡️  Cybersecurity Portfolio Document Manager
==================================================
📁 Available Portfolio Categories:
==================================================
1. Incident Response → projects/incident_response/
2. Vulnerability Assessment → projects/vulnerability_assessment/
3. Access Control → projects/access_control/
4. Network Security → projects/network_security/
5. Tools & Automation → projects/tools_automation/
6. Certifications → certifications/
7. Resume → resume/
==================================================

🎯 Select category (1-7): 2

📄 File Information:
------------------------------
📂 Source file path: /Users/stephenmiller/Downloads/penetration_test_report.docx
📝 Brief description: Comprehensive penetration testing of web application
🛠️ Skills demonstrated (comma-separated): penetration testing, web security, OWASP Top 10

🚀 Commit and push to GitHub? (y/n): y

✅ Copied: penetration_test_report.docx → projects/vulnerability_assessment/
✅ Updated: projects/vulnerability_assessment/README.md
✅ Updated: skills_matrix/skills_assessment.md
✅ Changes committed and pushed to GitHub

🎉 Successfully added penetration_test_report.docx to your portfolio!
📁 Location: projects/vulnerability_assessment/penetration_test_report.docx
🌐 Your portfolio: https://pianomansjpm.github.io/cybersecurity-portfolio
```

## 🔧 **Manual Process (Alternative)**

If you prefer to add documents manually:

1. **Copy file** to appropriate category folder
2. **Update README** in that category
3. **Update skills matrix** if needed
4. **Commit to Git**:
   ```bash
   git add .
   git commit -m "Add new document: filename"
   git push origin main
   ```

## 📁 **File Organization Rules**

| Document Type | Category | Skills to Add |
|---------------|----------|---------------|
| Incident reports | Incident Response | incident response, documentation, threat analysis |
| Security assessments | Vulnerability Assessment | vulnerability scanning, risk assessment, penetration testing |
| Access control docs | Access Control | RBAC, identity management, authentication |
| Network analysis | Network Security | network monitoring, packet analysis, Wireshark |
| Scripts/tools | Tools & Automation | Python, automation, scripting |
| Certificates | Certifications | [certification name] |
| Resume updates | Resume | N/A |

## 🎯 **Pro Tips**

- **Use descriptive file names**: `SQL_Injection_Analysis_2024.docx` not `document1.docx`
- **Be specific with skills**: List actual technologies and methodologies
- **Keep descriptions concise**: 1-2 sentences maximum
- **Test your portfolio**: Check https://pianomansjpm.github.io/cybersecurity-portfolio after adding documents

## 🆘 **Troubleshooting**

### **Script won't run**
```bash
chmod +x add_document.py
python3 add_document.py
```

### **Git errors**
- Check your internet connection
- Ensure you're in the portfolio directory
- Try manual commit: `git add . && git commit -m "message" && git push`

### **File not found**
- Use absolute paths: `/Users/stephenmiller/Downloads/file.docx`
- Or relative paths from portfolio directory: `../Downloads/file.docx`

## 🚀 **Benefits of Automation**

- **Saves time**: No manual file organization
- **Reduces errors**: Consistent formatting and structure
- **Keeps portfolio current**: Automatic Git commits
- **Professional presentation**: Proper documentation updates
- **Easy maintenance**: Simple command-line interface

Your portfolio will stay organized and professional with minimal effort! 🛡️ 
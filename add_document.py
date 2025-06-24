#!/usr/bin/env python3
"""
Portfolio Document Manager
Automated tool to add new documents to your cybersecurity portfolio
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
import subprocess

class PortfolioManager:
    def __init__(self):
        self.portfolio_root = Path(__file__).parent
        self.categories = {
            '1': ('incident_response', 'Incident Response'),
            '2': ('vulnerability_assessment', 'Vulnerability Assessment'),
            '3': ('access_control', 'Access Control'),
            '4': ('network_security', 'Network Security'),
            '5': ('tools_automation', 'Tools & Automation'),
            '6': ('certifications', 'Certifications'),
            '7': ('resume', 'Resume')
        }
        
    def show_categories(self):
        """Display available categories"""
        print("\n📁 Available Portfolio Categories:")
        print("=" * 50)
        for key, (folder, name) in self.categories.items():
            print(f"{key}. {name} → projects/{folder}/")
        print("6. Certifications → certifications/")
        print("7. Resume → resume/")
        print("=" * 50)
        
    def get_category_choice(self):
        """Get user's category choice"""
        while True:
            choice = input("\n🎯 Select category (1-7): ").strip()
            if choice in self.categories:
                return self.categories[choice]
            print("❌ Invalid choice. Please select 1-7.")
            
    def get_file_info(self):
        """Get file information from user"""
        print("\n📄 File Information:")
        print("-" * 30)
        
        # Get source file path
        while True:
            source_path = input("📂 Source file path: ").strip()
            if os.path.exists(source_path):
                break
            print("❌ File not found. Please check the path.")
            
        # Get description
        description = input("📝 Brief description: ").strip()
        if not description:
            description = "Document added to portfolio"
            
        # Get skills demonstrated
        skills = input("🛠️ Skills demonstrated (comma-separated): ").strip()
        
        return source_path, description, skills
        
    def copy_file(self, source_path, category_folder):
        """Copy file to appropriate category folder"""
        source_file = Path(source_path)
        dest_folder = self.portfolio_root / category_folder
        dest_file = dest_folder / source_file.name
        
        # Create folder if it doesn't exist
        dest_folder.mkdir(exist_ok=True)
        
        # Copy file
        shutil.copy2(source_file, dest_file)
        print(f"✅ Copied: {source_file.name} → {category_folder}/")
        
        return dest_file
        
    def update_readme(self, category_folder, category_name, filename, description, skills):
        """Update the category README file"""
        readme_path = self.portfolio_root / category_folder / "README.md"
        
        if not readme_path.exists():
            print(f"⚠️  No README found for {category_name}. Creating one...")
            self.create_category_readme(category_folder, category_name)
            
        # Read existing README
        with open(readme_path, 'r') as f:
            content = f.read()
            
        # Find the projects section
        if "## Projects" in content:
            # Add new project before the closing of projects section
            new_project = f"""
### {len([line for line in content.split('\n') if line.startswith('### ')]) + 1}. {filename.replace('.docx', '').replace('.pdf', '').replace('_', ' ').title()}
**File**: `{filename}`
- **Description**: {description}
- **Skills Demonstrated**:
"""
            
            if skills:
                for skill in skills.split(','):
                    new_project += f"  - {skill.strip()}\n"
            else:
                new_project += "  - Document analysis and reporting\n"
                
            # Insert before the Key Competencies section
            if "## Key Competencies" in content:
                content = content.replace("## Key Competencies", new_project + "\n## Key Competencies")
            else:
                content += new_project
                
        # Write updated content
        with open(readme_path, 'w') as f:
            f.write(content)
            
        print(f"✅ Updated: {category_folder}/README.md")
        
    def create_category_readme(self, category_folder, category_name):
        """Create a new README for a category"""
        readme_content = f"""# {category_name} Projects

## Overview
This section contains {category_name.lower()} projects and documentation.

## Projects

## Key Competencies

## Industry Standards

## Tools and Methodologies
"""
        
        readme_path = self.portfolio_root / category_folder / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
            
    def update_skills_matrix(self, skills):
        """Update skills matrix with new skills"""
        if not skills:
            return
            
        skills_matrix_path = self.portfolio_root / "skills_matrix" / "skills_assessment.md"
        
        if not skills_matrix_path.exists():
            print("⚠️  Skills matrix not found. Skipping skills update.")
            return
            
        # Read existing skills matrix
        with open(skills_matrix_path, 'r') as f:
            content = f.read()
            
        # Add new skills to appropriate sections
        new_skills = [skill.strip() for skill in skills.split(',') if skill.strip()]
        
        for skill in new_skills:
            # Check if skill already exists
            if skill not in content:
                # Add to Technical Skills section
                if "### Technical Skills" in content:
                    # Find the skills list and add the new skill
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if "### Technical Skills" in line:
                            # Find the end of the skills list
                            j = i + 1
                            while j < len(lines) and (lines[j].startswith('|') or lines[j].startswith('-')):
                                j += 1
                            # Insert new skill
                            lines.insert(j, f"| {skill} | Intermediate | {skill} implementation |")
                            break
                    content = '\n'.join(lines)
                    
        # Write updated content
        with open(skills_matrix_path, 'w') as f:
            f.write(content)
            
        print(f"✅ Updated: skills_matrix/skills_assessment.md")
        
    def git_commit(self, filename, category_name):
        """Commit changes to Git"""
        try:
            # Add all changes
            subprocess.run(['git', 'add', '.'], cwd=self.portfolio_root, check=True)
            
            # Commit
            commit_message = f"Add {category_name.lower()} document: {filename}"
            subprocess.run(['git', 'commit', '-m', commit_message], cwd=self.portfolio_root, check=True)
            
            # Push to GitHub
            subprocess.run(['git', 'push', 'origin', 'main'], cwd=self.portfolio_root, check=True)
            
            print("✅ Changes committed and pushed to GitHub")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git operation failed: {e}")
            print("You can manually commit changes later using:")
            print("  git add .")
            print("  git commit -m 'Add new document'")
            print("  git push origin main")
            
    def run(self):
        """Main execution flow"""
        print("🛡️  Cybersecurity Portfolio Document Manager")
        print("=" * 50)
        
        # Show categories
        self.show_categories()
        
        # Get user choices
        category_folder, category_name = self.get_category_choice()
        source_path, description, skills = self.get_file_info()
        
        # Copy file
        dest_file = self.copy_file(source_path, category_folder)
        
        # Update documentation
        self.update_readme(category_folder, category_name, dest_file.name, description, skills)
        self.update_skills_matrix(skills)
        
        # Git operations
        git_choice = input("\n🚀 Commit and push to GitHub? (y/n): ").strip().lower()
        if git_choice == 'y':
            self.git_commit(dest_file.name, category_name)
        
        print(f"\n🎉 Successfully added {dest_file.name} to your portfolio!")
        print(f"📁 Location: {category_folder}/{dest_file.name}")
        print(f"🌐 Your portfolio: https://pianomansjpm.github.io/cybersecurity-portfolio")

def main():
    if len(sys.argv) > 1:
        # Command line mode
        print("Command line mode not implemented yet. Use interactive mode.")
        return
        
    manager = PortfolioManager()
    manager.run()

if __name__ == "__main__":
    main() 
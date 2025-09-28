import streamlit as st
import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any
import base64
import urllib.parse

class GoogleDriveExporter:
    """Simple Google Drive integration using Google Drive API"""
    
    def __init__(self):
        self.api_base = "https://www.googleapis.com/drive/v3"
        self.upload_base = "https://www.googleapis.com/upload/drive/v3"
    
    def get_auth_url(self) -> str:
        """Generate Google OAuth URL for Drive access"""
        # This would normally use your app's client ID
        # For now, we'll show instructions for manual upload
        return "https://drive.google.com/drive/my-drive"
    
    def create_shareable_link(self, content: str, filename: str, content_type: str = "text/plain") -> str:
        """Create a shareable Google Drive link (simplified approach)"""
        # For demo purposes, we'll create a data URL that can be manually uploaded
        encoded_content = urllib.parse.quote(content)
        
        # Create a simple HTML page that helps upload to Drive
        upload_helper = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Upload to Google Drive</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .button {{ background: #4285f4; color: white; padding: 12px 24px; 
                          border: none; border-radius: 4px; cursor: pointer; 
                          text-decoration: none; display: inline-block; }}
                .content {{ background: #f5f5f5; padding: 20px; margin: 20px 0; 
                           border-radius: 4px; max-height: 300px; overflow-y: auto; }}
                pre {{ white-space: pre-wrap; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>📤 Upload Chat to Google Drive</h2>
                <p>Your chat export is ready! Follow these steps:</p>
                
                <ol>
                    <li>Copy the content below</li>
                    <li>Go to <a href="https://drive.google.com" target="_blank">Google Drive</a></li>
                    <li>Click "New" → "Google Docs" (or "Upload files")</li>
                    <li>Paste the content or upload the file</li>
                    <li>Save as "{filename}"</li>
                </ol>
                
                <div class="content">
                    <h4>Content to copy:</h4>
                    <pre>{content}</pre>
                </div>
                
                <a href="https://drive.google.com" target="_blank" class="button">
                    🚀 Open Google Drive
                </a>
                
                <br><br>
                <button onclick="copyContent()" class="button">📋 Copy Content</button>
            </div>
            
            <script>
                function copyContent() {{
                    const content = `{content}`;
                    navigator.clipboard.writeText(content).then(() => {{
                        alert('Content copied to clipboard! Now go to Google Drive and paste it.');
                    }});
                }}
            </script>
        </body>
        </html>
        """
        
        return upload_helper

def show_gdrive_export(chat_content: str, filename: str):
    """Show Google Drive export options"""
    st.markdown("### 🔗 Google Drive Export")
    
    # Option 1: Manual upload instructions
    with st.expander("📋 Method 1: Copy & Paste"):
        st.markdown("""
        **Quick Upload:**
        1. Copy the chat content below
        2. Open [Google Drive](https://drive.google.com) 
        3. Create a new Google Doc
        4. Paste the content
        5. Save with your preferred name
        """)
        
        st.text_area("Chat Content (Copy this)", chat_content, height=200)
        
        if st.button("📋 Copy to Clipboard", key="copy_gdrive"):
            # JavaScript to copy content (works in some browsers)
            st.write("Content ready to copy! Select all text above and copy manually.")
    
    # Option 2: Download then upload
    with st.expander("📤 Method 2: Download & Upload"):
        st.markdown("""
        **File Upload:**
        1. Download the file using the button below
        2. Go to [Google Drive](https://drive.google.com)
        3. Click "New" → "File upload"
        4. Select your downloaded file
        """)
        
        st.download_button(
            label="📥 Download for Drive Upload",
            data=chat_content,
            file_name=filename,
            mime="text/plain"
        )
        
        st.markdown("[🚀 Open Google Drive](https://drive.google.com)")
    
    # Option 3: Share link (future enhancement)
    with st.expander("🔗 Method 3: Direct Share (Coming Soon)"):
        st.info("🚧 Direct Google Drive API integration coming in future update!")
        st.markdown("""
        **Planned features:**
        - One-click upload to Drive
        - Automatic folder organization
        - Share links generation
        - Collaboration features
        """)

def show_quick_gdrive_actions():
    """Show quick Google Drive actions in sidebar"""
    st.sidebar.markdown("### 🔗 Google Drive")
    
    # Quick actions
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("📂 Open Drive", use_container_width=True):
            st.sidebar.markdown("[🚀 Google Drive](https://drive.google.com)")
    
    with col2:
        if st.button("📝 New Doc", use_container_width=True):
            st.sidebar.markdown("[📄 New Google Doc](https://docs.google.com/document/create)")
    
    # Tips
    st.sidebar.info("""
    💡 **Quick tip:** 
    Export your chat first, then use Google Drive's upload feature!
    """)

def create_gdrive_folder_suggestion(topic: str) -> str:
    """Suggest a folder structure for Google Drive"""
    suggestions = f"""
    📁 **Suggested Google Drive Organization:**
    
    ```
    📂 AI Learning Sessions/
    ├── 📂 {topic}/
    │   ├── 📄 Chat_{datetime.now().strftime('%Y%m%d')}.txt
    │   ├── 📄 Notes_{topic}.doc
    │   └── 📂 Exports/
    └── 📂 Other Topics/
    ```
    
    This keeps your learning organized by topic and date!
    """
    return suggestions
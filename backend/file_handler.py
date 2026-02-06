"""
File upload handler with validation and processing
"""
import os
import uuid
import hashlib
from typing import Optional, List
from datetime import datetime
from pathlib import Path
import mimetypes


class FileHandler:
    """Handle file uploads with validation and storage"""

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        # Documents
        '.pdf', '.doc', '.docx', '.txt', '.md',
        # Images
        '.jpg', '.jpeg', '.png', '.gif', '.svg',
        # Audio
        '.mp3', '.wav', '.ogg', '.m4a',
        # Code
        '.py', '.js', '.ts', '.java', '.cpp', '.c',
    }

    # Maximum file size (10 MB default)
    MAX_FILE_SIZE = 10 * 1024 * 1024

    def __init__(self, upload_dir: str = "uploads"):
        """
        Initialize file handler

        Args:
            upload_dir: Directory to store uploaded files
        """
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def validate_file(
        self,
        filename: str,
        file_size: int,
        allowed_extensions: Optional[set] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Validate uploaded file

        Args:
            filename: Original filename
            file_size: File size in bytes
            allowed_extensions: Optional set of allowed extensions

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file extension
        ext = Path(filename).suffix.lower()
        extensions = allowed_extensions or self.ALLOWED_EXTENSIONS

        if ext not in extensions:
            return False, f"File type {ext} not allowed. Allowed: {', '.join(extensions)}"

        # Check file size
        if file_size > self.MAX_FILE_SIZE:
            max_mb = self.MAX_FILE_SIZE / (1024 * 1024)
            return False, f"File too large. Maximum size: {max_mb}MB"

        # Check filename
        if not filename or filename.startswith('.'):
            return False, "Invalid filename"

        return True, None

    def generate_safe_filename(self, original_filename: str) -> str:
        """
        Generate a safe, unique filename

        Args:
            original_filename: Original uploaded filename

        Returns:
            Safe filename with unique ID
        """
        # Get extension
        ext = Path(original_filename).suffix.lower()

        # Generate unique ID
        unique_id = uuid.uuid4().hex[:12]

        # Create timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        # Combine
        safe_name = f"{timestamp}_{unique_id}{ext}"

        return safe_name

    async def save_file(
        self,
        file_content: bytes,
        original_filename: str,
        user_id: Optional[str] = None
    ) -> dict:
        """
        Save uploaded file

        Args:
            file_content: File content as bytes
            original_filename: Original filename
            user_id: Optional user ID for organization

        Returns:
            Dictionary with file info
        """
        # Validate
        is_valid, error = self.validate_file(original_filename, len(file_content))
        if not is_valid:
            raise ValueError(error)

        # Generate safe filename
        safe_filename = self.generate_safe_filename(original_filename)

        # Create user subdirectory if user_id provided
        if user_id:
            user_dir = self.upload_dir / user_id
            user_dir.mkdir(parents=True, exist_ok=True)
            file_path = user_dir / safe_filename
        else:
            file_path = self.upload_dir / safe_filename

        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_content)

        # Calculate file hash
        file_hash = hashlib.sha256(file_content).hexdigest()

        # Get MIME type
        mime_type, _ = mimetypes.guess_type(original_filename)

        return {
            "filename": safe_filename,
            "original_filename": original_filename,
            "path": str(file_path),
            "size": len(file_content),
            "hash": file_hash,
            "mime_type": mime_type,
            "uploaded_at": datetime.utcnow().isoformat(),
            "user_id": user_id
        }

    def get_file_path(self, filename: str, user_id: Optional[str] = None) -> Optional[Path]:
        """Get full path to a file"""
        if user_id:
            file_path = self.upload_dir / user_id / filename
        else:
            file_path = self.upload_dir / filename

        if file_path.exists():
            return file_path
        return None

    def delete_file(self, filename: str, user_id: Optional[str] = None) -> bool:
        """Delete a file"""
        file_path = self.get_file_path(filename, user_id)
        if file_path and file_path.exists():
            file_path.unlink()
            return True
        return False

    def list_files(self, user_id: Optional[str] = None) -> List[dict]:
        """List all uploaded files"""
        if user_id:
            search_dir = self.upload_dir / user_id
        else:
            search_dir = self.upload_dir

        if not search_dir.exists():
            return []

        files = []
        for file_path in search_dir.glob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                mime_type, _ = mimetypes.guess_type(file_path.name)

                files.append({
                    "filename": file_path.name,
                    "size": stat.st_size,
                    "mime_type": mime_type,
                    "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })

        return sorted(files, key=lambda x: x['created_at'], reverse=True)


# Singleton instance
file_handler = FileHandler()

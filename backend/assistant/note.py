"""
note.py

This module defines the function note_tool, which is responsible for saving notes to a local file.
The function takes a note as input and appends it to a file named "notes.txt".
The function is designed to be used in a legal assistant application, where users can save notes for future referece.
"""

from langchain.tools import tool

@tool
def note_tool(note):
    """
    saves a note to a local file
    
    Args:
        note: the text note to save
    """
    with open("notes.txt", "a") as f:
        f.write(note + "\n")
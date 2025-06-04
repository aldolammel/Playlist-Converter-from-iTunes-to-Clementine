"""
Playlist Converter: iTunes to Clementine edition
Author: @aldolammel
Last update: Jun, 4th 2025
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import xml.dom.minidom as minidom
import os
import sys

# CUSTOMIZE YOUR PATH HERE:
MY_WINDOWS_MUSIC_FOLDER = r"U:\Shared\Music"  # Using raw string for Windows path
MY_LINUX_MUSIC_FOLDER = "/home/aldolammel/Music"  # Linux path remains the same

# DEFINE HERE:
PATH_MUST_BE_USED_NOW = MY_WINDOWS_MUSIC_FOLDER  # Define which system path you wanna use!

# App core below - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def validate_path(path, path_name):
    """Validates if the path ends with separator"""
    if path.endswith('/') or path.endswith('\\'):
        print(
            f"Error: {path_name} cannot end with '/' or '\\'. Please remove the trailing separator."
        )
        sys.exit(1)
    return path

# Validate paths before using them
MY_WINDOWS_MUSIC_FOLDER = validate_path(MY_WINDOWS_MUSIC_FOLDER, "MY_WINDOWS_MUSIC_FOLDER")
MY_LINUX_MUSIC_FOLDER = validate_path(MY_LINUX_MUSIC_FOLDER, "MY_LINUX_MUSIC_FOLDER")

def read_itunes_xml(file_path):
    """Reads iTunes XML and returns tracks data"""
    tree = ET.parse(file_path)
    root = tree.getroot()
    tracks_data = []
    
    # Navigate to tracks dictionary
    tracks_dict = root.find('dict/dict')
    if tracks_dict is None:
        return tracks_data
    
    current_track = {}
    for elem in tracks_dict:
        if elem.tag == 'dict':  # Only process the dict elements
            # Process track dictionary
            for i in range(0, len(elem), 2):
                if i+1 >= len(elem):
                    break
                key = elem[i].text
                value = elem[i+1].text
                
                # Map only relevant fields
                if key in ['Name', 'Artist', 'Album', 'Total Time', 'Track Number', 'Location']:
                    current_track[key] = value
            
            if current_track:
                tracks_data.append(current_track)
                current_track = {}
    
    return tracks_data

def create_xspf_playlist(tracks):
    """Creates XSPF format playlist"""
    root = ET.Element("playlist")
    root.set("version", "1")
    root.set("xmlns", "http://xspf.org/ns/0/")
    
    tracklist = ET.SubElement(root, "trackList")
    
    for track_data in tracks:
        if not track_data:
            continue
            
        track = ET.SubElement(tracklist, "track")
        
        field_mapping = {
            'Name': 'title',
            'Artist': 'creator',
            'Album': 'album',
            'Total Time': 'duration',
            'Track Number': 'trackNum',
            'Location': 'location'
        }
        
        for itunes_key, xspf_key in field_mapping.items():
            if itunes_key in track_data:
                elem = ET.SubElement(track, xspf_key)
                
                if itunes_key == 'Location':
                    # Extract just the filename from the full path
                    original_path = track_data[itunes_key].replace('file://localhost', '')
                    filename = os.path.basename(original_path)
                    # Create new path with custom prefix using os.path.join
                    new_path = os.path.join(PATH_MUST_BE_USED_NOW, filename)
                    
                    # Use appropriate path separator based on the chosen path
                    if PATH_MUST_BE_USED_NOW == MY_WINDOWS_MUSIC_FOLDER:
                        new_path = new_path.replace('/', '\\')  # Ensure Windows backslashes
                    else:
                        new_path = new_path.replace('\\', '/')  # Ensure Unix forward slashes
                        
                    elem.text = new_path
                else:
                    elem.text = track_data[itunes_key]
    
    return root

def format_xml(element):
    """Format XML with proper indentation and encoding"""
    # Convert to string with unicode encoding first
    rough_string = ET.tostring(element, encoding='unicode', method='xml')
    
    try:
        # Parse and format with proper indentation
        reparsed = minidom.parseString(rough_string)
        formatted_xml = reparsed.toprettyxml(indent="    ")
        
        # Clean up empty lines and extra whitespace
        lines = [line for line in formatted_xml.split('\n') if line.strip()]
        formatted_xml = '\n'.join(lines)
        
        # Ensure proper XML declaration
        if not formatted_xml.startswith('<?xml'):
            formatted_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + formatted_xml
            
        return formatted_xml
        
    except Exception as e:
        print(f"Error formatting XML: {e}")
        return None

def main():
    input_folder = "to_convert"
    output_folder = "converted"
    
    # Create output directory if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Process each .xml file in input folder
    for file in os.listdir(input_folder):
        if file.endswith('.xml'):
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, f"{file.rsplit('.', 1)[0]}.xspf")
            
            # Convert playlist
            tracks = read_itunes_xml(input_path)
            playlist = create_xspf_playlist(tracks)
            
            # Format and write the output file
            formatted_xml = format_xml(playlist)
            if formatted_xml is not None:
                try:
                    # Write file in text mode with explicit UTF-8 encoding
                    with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
                        f.write(formatted_xml)
                    print(f"Converted {file} to {output_path}")
                except Exception as e:
                    print(f"Error writing file {output_path}: {e}")
            else:
                print(f"Failed to convert {file}")

if __name__ == "__main__":
    main()
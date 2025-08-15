#!/usr/bin/env python3
"""
GIF Frame Extractor for TuxTray
Extracts animation frames from GIF files and organizes them into appropriate directories.
"""

import os
from pathlib import Path
from PIL import Image
import re

def extract_gif_frames(gif_path, output_dir, target_width=450, target_height=595):
    """
    Extract frames from a GIF file and save as PNG sequences.
    
    Args:
        gif_path: Path to the GIF file
        output_dir: Directory to save extracted frames
        target_width: Target width for frames
        target_height: Target height for frames
        
    Returns:
        Number of frames extracted
    """
    gif_path = Path(gif_path)
    output_dir = Path(output_dir)
    
    if not gif_path.exists():
        print(f"❌ GIF file not found: {gif_path}")
        return 0
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Open the GIF
        with Image.open(gif_path) as gif:
            frame_count = 0
            
            print(f"🎬 Processing GIF: {gif_path.name}")
            print(f"   Original size: {gif.size}")
            print(f"   Target size: {target_width}x{target_height}")
            
            # Extract each frame
            try:
                while True:
                    # Convert frame to RGBA if needed
                    frame = gif.copy()
                    if frame.mode != 'RGBA':
                        frame = frame.convert('RGBA')
                    
                    # Calculate scaling to fit target dimensions while maintaining aspect ratio
                    original_width, original_height = frame.size
                    width_scale = target_width / original_width
                    height_scale = target_height / original_height
                    scale = min(width_scale, height_scale)
                    
                    # Calculate new dimensions
                    new_width = int(original_width * scale)
                    new_height = int(original_height * scale)
                    
                    # Resize frame with high quality
                    resized_frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Create canvas with target dimensions and transparent background
                    final_frame = Image.new('RGBA', (target_width, target_height), (0, 0, 0, 0))
                    
                    # Center the resized frame
                    x_offset = (target_width - new_width) // 2
                    y_offset = (target_height - new_height) // 2
                    final_frame.paste(resized_frame, (x_offset, y_offset), resized_frame)
                    
                    # Save frame with zero-padded numbering
                    frame_filename = f"frame_{frame_count:03d}.png"
                    frame_path = output_dir / frame_filename
                    final_frame.save(frame_path, 'PNG', optimize=True)
                    
                    print(f"   ✅ Extracted frame {frame_count:03d}")
                    frame_count += 1
                    
                    # Move to next frame
                    gif.seek(gif.tell() + 1)
                    
            except EOFError:
                # End of GIF reached
                pass
            
            print(f"   🎉 Successfully extracted {frame_count} frames")
            return frame_count
            
    except Exception as e:
        print(f"❌ Error processing {gif_path}: {e}")
        return 0

def determine_animation_type(gif_filename):
    """
    Determine animation type based on GIF filename.
    
    Args:
        gif_filename: Name of the GIF file
        
    Returns:
        Animation type (idle, walk, run)
    """
    filename_lower = gif_filename.lower()
    
    if 'idle' in filename_lower or 'static' in filename_lower:
        return 'idle'
    elif 'walk' in filename_lower or 'walking' in filename_lower:
        return 'walk' 
    elif 'run' in filename_lower or 'running' in filename_lower:
        return 'run'
    else:
        # Default mapping based on common patterns
        if 'walk' in filename_lower:
            return 'walk'
        elif 'run' in filename_lower:
            return 'run'
        else:
            return 'idle'  # Default fallback

def main():
    """Extract frames from all GIF files in the project."""
    print("🐧 TuxTray GIF Frame Extractor")
    print("=" * 50)
    
    # Base directories
    project_root = Path(__file__).parent
    assets_dir = project_root / "assets"
    skins_dir = assets_dir / "skins" / "default"
    
    # Find all GIF files
    gif_files = []
    
    # Check in project root
    gif_files.extend(project_root.glob("*.gif"))
    
    # Check in assets directory
    gif_files.extend(assets_dir.glob("*.gif"))
    
    if not gif_files:
        print("❌ No GIF files found!")
        return
    
    print(f"📁 Found {len(gif_files)} GIF file(s):")
    for gif_file in gif_files:
        print(f"   - {gif_file.name}")
    
    print()
    
    total_frames = 0
    
    for gif_file in gif_files:
        # Determine animation type from filename
        animation_type = determine_animation_type(gif_file.name)
        
        # Create output directory
        output_dir = skins_dir / animation_type
        
        print(f"🎯 Processing: {gif_file.name} → {animation_type}/ directory")
        
        # Extract frames
        frame_count = extract_gif_frames(gif_file, output_dir)
        total_frames += frame_count
        
        print()
    
    print("=" * 50)
    print(f"✅ Extraction complete!")
    print(f"📊 Total frames extracted: {total_frames}")
    print()
    
    # Show summary
    for anim_type in ['idle', 'walk', 'run']:
        anim_dir = skins_dir / anim_type
        if anim_dir.exists():
            frame_count = len(list(anim_dir.glob("*.png")))
            print(f"{anim_type.title()} animation: {frame_count} frames")
    
    print(f"\n🎉 Ready for TuxTray! All frames are in assets/skins/default/")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Resize all TuxTray animation frames to match the reference dimensions
Target: 450x595 pixels (width x height)
"""

import os
from pathlib import Path
from PIL import Image

def resize_frames(animation_path, target_width=450, target_height=595):
    """
    Resize all PNG frames in an animation directory.
    
    Args:
        animation_path: Path to animation directory
        target_width: Target width in pixels
        target_height: Target height in pixels
    """
    animation_path = Path(animation_path)
    
    if not animation_path.exists():
        print(f"Warning: Animation path not found: {animation_path}")
        return 0
    
    # Get all PNG files
    png_files = list(animation_path.glob("*.png"))
    
    if not png_files:
        print(f"No PNG files found in {animation_path}")
        return 0
    
    print(f"Processing {len(png_files)} frames in {animation_path.name}...")
    
    processed = 0
    
    for png_file in png_files:
        try:
            # Open the image
            with Image.open(png_file) as img:
                # Convert to RGBA if not already
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Calculate scaling to fit the target dimensions while maintaining aspect ratio
                original_width, original_height = img.size
                
                # Calculate scale factors for both dimensions
                width_scale = target_width / original_width
                height_scale = target_height / original_height
                
                # Use the smaller scale to ensure the image fits within target dimensions
                scale = min(width_scale, height_scale)
                
                # Calculate new dimensions
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)
                
                # Resize the image with high quality
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Create a new image with target dimensions and transparent background
                final_img = Image.new('RGBA', (target_width, target_height), (0, 0, 0, 0))
                
                # Calculate position to center the resized image
                x_offset = (target_width - new_width) // 2
                y_offset = (target_height - new_height) // 2
                
                # Paste the resized image onto the centered canvas
                final_img.paste(resized_img, (x_offset, y_offset), resized_img)
                
                # Save the processed frame
                final_img.save(png_file, 'PNG', optimize=True)
                
                processed += 1
                print(f"  ✓ {png_file.name}: {original_width}x{original_height} → {target_width}x{target_height}")
                
        except Exception as e:
            print(f"  ✗ Error processing {png_file.name}: {e}")
    
    return processed

def main():
    """Process all animation frames."""
    print("🐧 TuxTray Frame Resizer")
    print("=" * 50)
    print(f"Target dimensions: 450x595 pixels")
    print()
    
    # Define animation directories
    animations_base = Path("assets/skins/default")
    animations = ["idle", "walk", "run"]
    
    total_processed = 0
    
    for anim_name in animations:
        anim_path = animations_base / anim_name
        processed = resize_frames(anim_path)
        total_processed += processed
        print()
    
    print("=" * 50)
    print(f"✅ Processing complete! Resized {total_processed} frames total.")
    print()
    
    # Show summary
    for anim_name in animations:
        anim_path = animations_base / anim_name
        if anim_path.exists():
            frame_count = len(list(anim_path.glob("*.png")))
            print(f"{anim_name.title()} animation: {frame_count} frames")

if __name__ == "__main__":
    main()

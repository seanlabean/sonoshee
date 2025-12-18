from PIL import Image
import numpy as np
from scipy.ndimage import sobel
import random
# sonoshee: Pixel Sorting

def sort_rows(pixels, width):
    """Given an image, sort the pixels in each row based on the sum of their RGB values."""
    pixels = np.array(pixels).reshape(-1, width, 4)
    for row in pixels:
        # Sum RGB values along the color channels, ignoring the alpha channel
        pix_sum = row[:, :3].sum(axis=1)
        # Sort the row based on the summed RGB values
        sorted_indices = pix_sum.argsort()
        row[:] = row[sorted_indices]
    return pixels

def quick_sum_and_sort(arr):
    """Sort an array of pixels based on the sum of their RGB values."""
    # Sum RGB values along the color channels, ignoring the alpha channel
    pix_sum = arr[:, :3].sum(axis=1)
    # Sort the array based on the summed RGB values
    sorted_indices = pix_sum.argsort()
    return arr[sorted_indices]

def sort_edge_pixels(image, edge_mask):
    """Sort the pixels in the edge regions of an image (defined by edge mask) based on the sum of their RGB values."""
    pixels = np.array(image)
    edge_pixels = pixels[edge_mask]
    
    # Sum RGB values along the color channels, ignoring the alpha channel
    pix_sum = edge_pixels[:, :3].sum(axis=1)
    # Sort edge pixels based on the summed RGB values
    sorted_indices = pix_sum.argsort()
    sorted_edge_pixels = edge_pixels[sorted_indices]
    
    # Create a copy of the original pixels and replace edge regions with sorted pixels
    sorted_pixels = pixels.copy()
    sorted_pixels[edge_mask] = sorted_edge_pixels
    
    return sorted_pixels

def detect_edges(image):
    """Detect edges in an image using the Sobel operator."""
    grayscale = np.array(image.convert('L'))
    dx = sobel(grayscale, axis=0)
    dy = sobel(grayscale, axis=1)
    edge_magnitude = np.hypot(dx, dy)
    return  edge_magnitude

def create_edge_mask(edge_magnitude, threshold):
    return edge_magnitude > threshold

def sort_non_edge_sections(image, edge_mask, min_section_length):
    """Sort sections of consecutive non-edge pixels of length min_section_length or greater in an image based on the sum of their RGB values."""
    pixels = np.array(image)
    height, width, _ = pixels.shape
    for y in range(height):
        row = pixels[y]
        row_mask = edge_mask[y]

        # Find sections of consecutive non-edge pixels
        start_idx = 0
        while start_idx < width:
            # Find the start of a non-edge section
            while start_idx < width and row_mask[start_idx]:
                start_idx += 1

            if start_idx >= width:
                break

            # Find the end of the non-edge section
            end_idx = start_idx
            while end_idx < width and not row_mask[end_idx]:
                end_idx += 1

            # Sort the non-edge section if it's long enough
            if end_idx - start_idx >= min_section_length:
                section = row[start_idx:end_idx]
                sorted_section = quick_sum_and_sort(section)
                row[start_idx:end_idx] = sorted_section
            
            # Move to the next section
            start_idx = end_idx
    return pixels

im = Image.open('/home/sean/Documents/VindaugaProjects/taiwan-china-digizine/gfx/50-PST00143.JPG', 'r') #'./sonoshee_wp.png'
im = im.convert('RGBA')

edge_magnitude = detect_edges(im)
edge_mask = create_edge_mask(edge_magnitude, threshold=355)  # Adjust threshold as needed
lengths = [20, 50, 75, 100, 125, 150, 200, 300, 400]
for i in range(0, len(lengths)):
    min_section_length = random.choice(lengths)
    sorted_pix_val = sort_non_edge_sections(im, edge_mask, min_section_length)

    # Optional: Display the edge mask
    #edge_mask_image = Image.fromarray((edge_mask * 255).astype('uint8'))
    #edge_mask_image.save('./edge_mask.png')

    # Optional: Display edge magnitude
    #edge_magnitude_image = Image.fromarray(edge_magnitude.astype('uint8'))
    #edge_magnitude_image.save('./edge_magnitude.png')

    # Step 4: Combine Edge and Non-Edge Regions and Save Image
    sorted_image = Image.fromarray(sorted_pix_val.astype('uint8'), 'RGBA')
    sorted_image.save(f'./figures/{i}.png')
    print(f"Saved {i}.png")
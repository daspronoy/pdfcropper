PDF Content-Aware Border Cropper

Preserve vector graphics. Remove white margins. Produce clean, publication-ready PDFs.

This repository provides a Python-based utility for automatically cropping white margins from PDF pages without rasterizing them. Unlike many tools that convert each page into a bitmap image (which destroys vector content and reduces quality), this script preserves all vector drawings, text, and embedded images exactly as they are.

The cropping is performed by analyzing the actual content regions on each page:

    Text blocks

    Vector drawings (paths, shapes, curves, strokes)

    Embedded raster images

Optional annotations

The script then sets a new PDF crop box tightly wrapped around the union of all visible content, removing unused whitespace while keeping the internal structure untouched.


-Preserves vector graphics
    Your PDF may contain a mix of vector figures, mathematical text, and embedded bitmaps.
    This tool never rasterizes pages. Everything stays as crisp as the original.

-Content-aware crop

    Instead of relying on pixel detection, the script uses PyMuPDF’s structural page analysis to detect where actual content exists.

    It collects:

    Text bounding boxes

    Image placements

    Vector drawing bounds

    Annotation rectangles

    Then computes an exact content bounding box.

-Margin control

    You can specify how much padding to preserve around your content:

    margin=5.0   # PDF points (1 pt = 1/72 inch)



-Example Usage
    Command line (bash)
        python cropper.py input.pdf output.pdf

    Every page will be analyzed and cropped separately.

-Installation
    Dependencies

    Install required Python packages:
        pip install pymupdf


    PyMuPDF (the Python bindings of MuPDF) provides accurate access to text, image, and vector graphics bounding boxes.

How It Works (Technical Explanation)

The core idea is to scan each PDF page for all content-producing objects and take the geometric union of their bounding boxes.

1. Detect text regions
page.get_text("blocks")


Each block includes a rectangular region.

2. Detect embedded images
page.get_images(full=True)
page.get_image_rects(xref)

3. Detect vector drawings
page.get_drawings()


Each drawing element includes a rect bounding box whenever available.

4. Detect annotations

Links, highlights, notes, etc., all expose a .rect.

5. Construct union rectangle

All rectangles are merged into:

bbox |= rect

6. Apply margin and crop box

Finally:

page.set_cropbox(new_crop)


This adjusts how the PDF viewer displays the page without altering the underlying data.



Code Overview

The main components are:

1. compute_content_bbox(page)

    Computes the bounding rectangle of all visible content.

2. crop_pdf_content(input_pdf, output_pdf, margin)

    Cropping logic applied page-by-page.


Limitations

    If a page contains only white text on a white background, the script may not detect objects (rare).

    Some extremely complex vector graphics may not provide a bounding box via PyMuPDF, but this is uncommon.

    The crop box does not modify the media box, only the displayed content boundary.





License

    Free for all personal and academic (non-commercial) use.

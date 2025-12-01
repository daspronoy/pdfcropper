import sys
import fitz  # PyMuPDF


def compute_content_bbox(page):
    rects = []

    # 1) Text blocks
    # get_text("blocks") returns list of (x0, y0, x1, y1, text, block_no, block_type, ...)
    for block in page.get_text("blocks"):
        x0, y0, x1, y1 = block[:4]
        rects.append(fitz.Rect(x0, y0, x1, y1))

    # 2) Images
    # get_images() gives image xref; get_image_rects(xref) gives where it appears
    for img in page.get_images(full=True):
        xref = img[0]
        for r in page.get_image_rects(xref):
            rects.append(r)

    # 3) Drawings (vector graphics)
    # Each drawing dict usually has a 'rect' bounding box
    for d in page.get_drawings():
        if "rect" in d and d["rect"] is not None:
            rects.append(d["rect"])

    # 4) Annotations (optional)
    annot = page.first_annot
    while annot:
        rects.append(annot.rect)
        annot = annot.next

    if not rects:
        return None  # page is effectively empty

    # Take union of all rects
    bbox = rects[0]
    for r in rects[1:]:
        bbox |= r

    return bbox


def crop_pdf_content(input_pdf, output_pdf, margin=5.0):
    doc = fitz.open(input_pdf)

    for i, page in enumerate(doc):
        content_bbox = compute_content_bbox(page)

        # If page has no detectable content, skip cropping
        if content_bbox is None:
            print(f"Page {i+1}: no content detected, skipping.")
            continue

        # Expand bbox by a small margin
        content_bbox = content_bbox + (-margin, -margin, margin, margin)

        # Ensure we stay within the original mediabox
        mediabox = page.mediabox
        new_crop = fitz.Rect(
            max(content_bbox.x0, mediabox.x0),
            max(content_bbox.y0, mediabox.y0),
            min(content_bbox.x1, mediabox.x1),
            min(content_bbox.y1, mediabox.y1),
        )

        # Avoid degenerate rectangles
        if new_crop.width <= 0 or new_crop.height <= 0:
            print(f"Page {i+1}: computed invalid crop box, skipping.")
            continue

        # Set the page crop box (does not rasterize or change content)
        page.set_cropbox(new_crop)
        print(f"Page {i+1}: cropped to {new_crop}.")

    doc.save(output_pdf)
    doc.close()
    print(f"Saved cropped PDF to: {output_pdf}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python crop_pdf_content_box.py input.pdf output.pdf")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    crop_pdf_content(input_path, output_path)

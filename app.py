import cv2
import gradio as gr
import numpy as np
from tinyface import TinyFace

# Initialize TinyFace once at startup
tinyface = TinyFace()
tinyface.prepare()


def swap_face(original_image: np.ndarray, reference_image: np.ndarray) -> np.ndarray:
    # Gradio provides RGB numpy arrays; TinyFace/OpenCV expects BGR
    original_bgr = cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR)
    reference_bgr = cv2.cvtColor(reference_image, cv2.COLOR_RGB2BGR)

    # Detect the face in the original image (used to identify which face to replace)
    source_face = tinyface.get_one_face(original_bgr)
    if source_face is None:
        raise gr.Error("No face detected in the original image.")

    # Detect the new face to apply (from the reference image)
    new_face = tinyface.get_one_face(reference_bgr)
    if new_face is None:
        raise gr.Error("No face detected in the reference image.")

    # swap_face(image, reference_face=face to match, destination_face=new face to apply)
    result_bgr = tinyface.swap_face(original_bgr, source_face, new_face)

    # Convert back to RGB for Gradio
    return cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)


demo = gr.Interface(
    fn=swap_face,
    inputs=[
        gr.Image(label="Original Image (face to replace)", type="numpy"),
        gr.Image(label="Reference Image (new face to apply)", type="numpy"),
    ],
    outputs=gr.Image(label="Result"),
    title="Face Swap",
    description="Upload an original image and a reference image. The face in the original image will be replaced with the face from the reference image.",
)

if __name__ == "__main__":
    demo.launch()

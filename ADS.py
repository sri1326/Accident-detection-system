import streamlit as st
import cv2
import os
from pathlib import Path
import google.generativeai as genai
def video_input():
  video_input = st.file_uploader("Video Input", type=['mp4', 'avi'])
  return video_input

def video_to_frames(video_input, folder_path,frame_interval=5000):
    if video_input is None:
        st.error("Please upload a video file.")
        return
    temp_video_path = "temp_video.mp4"
    with open(temp_video_path, "wb") as f:
        f.write(video_input.read())

    # Open the video file
    cap = cv2.VideoCapture(temp_video_path)

    # Create the output folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Read frames and save as images
    frame_count = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Save the frame as an image
        if frame_count % frame_interval == 0:
            frame_name = f"frame_{frame_count:04d}.png"
            frame_path = os.path.join(folder_path, frame_name)
            cv2.imwrite(frame_path, frame)

        frame_count += 1

    # Release the video capture object
    cap.release()
    os.remove(temp_video_path)

# Get the video input from the user.
video_input = video_input()

# Display the video input.
folder_path = 'frames_output'
if video_input:
  st.video(video_input)
  video_to_frames(video_input, folder_path)

import os

genai.configure(api_key="AIzaSyBisghLF7UMfPcx2CG-07brnK5RLnaHNOE")

# Set up the model
generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


# Get a list of all files in the folder
files = os.listdir(folder_path)

# Filter out only files with image extensions (you can customize this based on your image types)
image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
for image_file in image_files:
  image_path = os.path.join(folder_path, image_file)
  if not Path(image_path).exists():
     continue

  while True:
    if not (img := Path(image_path)).exists():
      break
    image_parts = [
      {
        "mime_type": "image/jpeg",
        "data": Path(image_path).read_bytes()
      },
    ]

    prompt_parts = [
      "has an accident occurred? 'Accident Occured' or 'No Accident is Detected', give me response as instructed?",
      image_parts[0]
    ]

    response = model.generate_content(prompt_parts)
    st.header(response.text)
    break

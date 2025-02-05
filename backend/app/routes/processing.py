from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from app.utils.file_utils import create_directories, save_json, delete_folder, get_next_id
from app.models.models import whisper_model
from app.utils.vectordb import create_vector_db
from app.utils.similarity_search import perform_similarity_search
from app.services.pdfs_processing import get_text_from_pdfs
import os
import json
from pydantic import BaseModel
from typing import List

router = APIRouter()

@router.post("/process/")
async def processing(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    dateTime: str = Form(...),
    topic: str = Form(...),
    otherInfo: str = Form(...),
    audio: UploadFile = File(...),
    pdfs: List[UploadFile] = File(...),
):
    try:
        print('started')
        base_path = os.path.dirname(__file__)
        data_dir = os.path.join(base_path, "..", "..", "data")
        
        # Generate a unique ID for the submission
        id = str(get_next_id(data_dir))

        # video_dir = os.path.join(data_dir, id, "Video")
        audio_dir = os.path.join(data_dir, id, "Audio")
        pdfs_dir = os.path.join(data_dir, id, "PDFs")
        create_directories([ audio_dir, pdfs_dir])
        
        # video_path = os.path.join(video_dir, f"{id}.mp4")
        audio_path = os.path.join(audio_dir, f"{id}.mp3")
        # screenshots_path = os.path.join(data_dir, id, "Screenshots")

        # create_directories([screenshots_path])
        
        # Save the video file in chunks
        # try:
        #     with open(video_path, "wb") as f:
        #         while chunk := await video.read(1024 * 1024):  # Read in 1MB chunks
        #             f.write(chunk)
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=f"Failed to save video file: {str(e)}")

        # Save the audio file
        try:
            with open(audio_path, "wb") as f:
                while chunk := await audio.read(1024 * 1024):  # Read in 1MB chunks
                    f.write(chunk)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save audio file: {str(e)}")

        # Save the PDF files
        for index, pdf in enumerate(pdfs):
            pdf_path = os.path.join(pdfs_dir, f"{id}_{index}.pdf")
            try:
                with open(pdf_path, "wb") as f:
                    while chunk := await pdf.read(1024 * 1024):  # Read in 1MB chunks
                        f.write(chunk)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to save PDF file: {str(e)}")

        # Process video: extract audio and screenshots
        # extract_audio(video_path, audio_path)
        # extract_screenshots(video_path, screenshots_path, fps=0.2, id=id)

        # Classify and remove duplicates
        # classify_and_remove_duplicates(screenshots_path)
        
        # Generate image descriptions
        # descriptions = await get_image_descriptions(screenshots_path, id)

        # Transcribe audio
        transcription = whisper_model.transcribe(audio_path)
        pdfs = get_text_from_pdfs(pdfs_dir)
        # Save results
        result = {
            "id": id,
            "name": name,
            "email": email,
            "subject": subject,
            "dateTime": dateTime,
            "topic": topic,
            "otherinfo": otherInfo,
            "transcription": transcription["text"],
            "pdfs": pdfs,
        }
        result_path = os.path.join(data_dir, id, "result.json")
        save_json(result, result_path)
        create_vector_db(id)

        # Verify and Delete the folders
        # png_files_exist = any(file.endswith(".png") for file in os.listdir(screenshots_path)) 
        # description_failure = png_files_exist and not descriptions[0].startswith(f"Description for {id}")

        # if result["transcription"] != "" and not description_failure:
        #     # delete_folder(os.path.dirname(video_path))
        #     delete_folder(os.path.dirname(audio_path))
        #     # delete_folder(screenshots_path)
        # else:
        #     result = {"error": "Processing failed"}
        
        return JSONResponse(content={"message": "Form submitted successfully", "id": id}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/getlist")
async def get_meetings_list():
    try:
        base_path = os.path.dirname(__file__)
        data_dir = os.path.join(base_path, "..", "..", "data")
        subjects = []

        for folder_name in os.listdir(data_dir):
            folder_path = os.path.join(data_dir, folder_name)
            if os.path.isdir(folder_path):
                result_file = os.path.join(folder_path, "result.json")
                if os.path.exists(result_file):
                    with open(result_file, "r") as f:
                        result_data = json.load(f)
                        subject_name = result_data.get("subject", "Unknown subject")
                        subjects.append({"id": folder_name, "name": subject_name})

        return JSONResponse(content={"subjects": subjects}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class SimilaritySearchRequest(BaseModel):
    query: str
    id: str

@router.post("/similarity_search")
async def similarity_search(request: SimilaritySearchRequest):
    try:
        results = perform_similarity_search(request.query, request.id)
        # print(results)
        return JSONResponse(content={"results": [res.page_content for res in results]}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
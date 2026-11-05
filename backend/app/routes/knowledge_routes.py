from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.controllers.knowledge_controller import add_content_controller

router = APIRouter(
    prefix="/courses",
    tags=["Knowledge Base"]
)


@router.post("/{course_id}/knowledge-base")
async def add_content_route(
    course_id: str,
    type: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        result = add_content_controller(
            course_id=course_id,
            content_type=type.lower(),
            file_bytes=file_bytes
        )

        return result

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        await file.close()
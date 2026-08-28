from fastapi import APIRouter, status

from app.pets.pets_schemas import CreatePetDto, Pet, UpdatePetDto
from app.pets.pets_service import pets_service
from app.shared.api_response import ApiResponse

router = APIRouter(
    prefix="/api/students/{studentId}/pets",
    tags=["Pets"],
)


@router.get("", response_model=ApiResponse[list[Pet]])
def find_all(studentId: str) -> ApiResponse[list[Pet]]:
    pets = pets_service.find_all_for_student(studentId)

    return ApiResponse[list[Pet]].success_response(
        data=pets,
        message="Mascotas obtenidas correctamente",
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[Pet],
)
def create(
    studentId: str,
    body: CreatePetDto,
) -> ApiResponse[Pet]:
    pet = pets_service.create(studentId, body)

    return ApiResponse[Pet].success_response(
        data=pet,
        message="Mascota creada correctamente",
        status_code=status.HTTP_201_CREATED,
    )


@router.patch(
    "/{petId}",
    response_model=ApiResponse[Pet],
)
def update(
    studentId: str,
    petId: str,
    body: UpdatePetDto,
) -> ApiResponse[Pet]:
    pet = pets_service.update(studentId, petId, body)

    return ApiResponse[Pet].success_response(
        data=pet,
        message="Mascota actualizada correctamente",
    )


@router.delete(
    "/{petId}",
    response_model=ApiResponse[Pet],
)
def delete(
    studentId: str,
    petId: str,
) -> ApiResponse[Pet]:
    pet = pets_service.delete(studentId, petId)

    return ApiResponse[Pet].success_response(
        data=pet,
        message="Mascota eliminada correctamente",
    )

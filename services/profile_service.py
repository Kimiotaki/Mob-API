import datetime
from typing import Any

from fastapi import HTTPException, status

from models.user_model import UserRole
from repositories.profile_repository import ProfileDocument, ProfileRepository
from repositories.user_repository import UserRepository
from schemas.profile_schema import ProfileUpsertRequest


class ProfileService:
    def __init__(
        self,
        profile_repository: ProfileRepository,
        user_repository: UserRepository,
    ):
        self.profile_repository = profile_repository
        self.user_repository = user_repository

    async def get_profile(self, user_id: str):
        user = await self.user_repository.find_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        profile = await self.profile_repository.find_by_user_id(user_id)
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )

        return self._serialize_profile(profile)

    async def upsert_profile(self, user_id: str, profile_request: ProfileUpsertRequest):
        user = await self.user_repository.find_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user_role = int(user["role"])
        if user_role == UserRole.STUDENT and profile_request.educator_details is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Educator profile details are not allowed for a student user",
            )
        if user_role == UserRole.EDUCATOR and profile_request.student_details is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student profile details are not allowed for an educator user",
            )
        if user_role not in {UserRole.STUDENT, UserRole.EDUCATOR}:
            if profile_request.student_details is not None or profile_request.educator_details is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Role-specific profile details are only supported for student and educator users",
                )

        now = datetime.datetime.now(datetime.timezone.utc)
        profile_data = profile_request.model_dump(
            mode="python",
            exclude_unset=True,
        )
        set_fields = self._flatten_update_data(profile_data)
        set_fields["role"] = user_role

        update_document = {
            "$set": {
                **set_fields,
                "modified_at": now,
                "modified_by": user_id,
            },
            "$setOnInsert": {
                "user_id": user_id,
                "created_at": now,
                "created_by": user_id,
            },
        }

        if user_role != UserRole.STUDENT:
            update_document["$set"]["student_details"] = None
        if user_role != UserRole.EDUCATOR:
            update_document["$set"]["educator_details"] = None

        profile = await self.profile_repository.upsert_profile(user_id, update_document)
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create profile",
            )
        return self._serialize_profile(profile)

    def _serialize_profile(self, profile: ProfileDocument) -> dict[str, Any]:
        return {
            "id": str(profile["_id"]),
            "user_id": profile["user_id"],
            "role": profile["role"],
            "full_name": profile.get("full_name"),
            "phone_number": profile.get("phone_number"),
            "alternate_phone_number": profile.get("alternate_phone_number"),
            "gender": profile.get("gender"),
            "date_of_birth": profile.get("date_of_birth"),
            "bio": profile.get("bio"),
            "city": profile.get("city"),
            "state": profile.get("state"),
            "country": profile.get("country"),
            "qualification": profile.get("qualification") or {},
            "student_details": profile.get("student_details"),
            "educator_details": profile.get("educator_details"),
            "created_at": profile["created_at"],
            "modified_at": profile["modified_at"],
            "created_by": profile["created_by"],
            "modified_by": profile["modified_by"],
        }

    def _flatten_update_data(
        self,
        payload: dict[str, Any],
        prefix: str = "",
    ) -> dict[str, Any]:
        flattened: dict[str, Any] = {}

        for key, value in payload.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict) and value:
                flattened.update(self._flatten_update_data(value, full_key))
                continue

            flattened[full_key] = value

        return flattened

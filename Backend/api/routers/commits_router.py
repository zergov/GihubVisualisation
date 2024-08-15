from fastapi import APIRouter, HTTPException
from typing import List
from api.schemas.common_schema import CommitDetail
from api.services.pydriller_service import PydrillerService

commits_router = APIRouter(prefix="/commits", tags=['api'])

pydriller_service = PydrillerService()

@commits_router.get("/", response_model=List[CommitDetail])
def fetch_all_commits(repo_path: str, days: int = 30):
    return pydriller_service.fetch_all_commits(repo_path, days)
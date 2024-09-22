import cProfile
import datetime

from fastapi import APIRouter, HTTPException
from typing import List
from api.schemas.common_schema import CommitDetail
from api.services.pydriller_service import PydrillerService

commits_router = APIRouter(prefix="/commits", tags=['api'])

pydriller_service = PydrillerService()

@commits_router.get("/", response_model=List[CommitDetail])
def fetch_all_commits(repo_path: str, days: int = 30):
    with cProfile.Profile() as pr:
        commits = pydriller_service.fetch_all_commits(repo_path, days)

        now = int(datetime.datetime.now().timestamp())
        pr.dump_stats("%s_commits_route.prof" % (now))

        return commits

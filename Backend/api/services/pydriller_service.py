from datetime import datetime, timedelta, timezone
from pydriller import Repository
from fastapi import HTTPException
from api.services.file_service import FileService
from api.services.cache_service import CacheService
import logging

import time
logger = logging.getLogger(__name__)

class PydrillerService:
    def __init__(self):
        self.message = 'Fetching Data'
        self.file_service = FileService()
        self.cache = CacheService()

    def fetch_all_commits(self, repo_path: str, days: int = 30):
        since_date = datetime.now(timezone.utc) - timedelta(days=days)
        cached_commits, cache_since_date = self.cache.query(repo_path)
        if cached_commits and days <= cache_since_date:
             commits = cached_commits
        else :
            # If the specified repo is not cached in the db, we cache it before returning the commits
            try:
                repo = Repository(repo_path ,only_no_merge=True, since=since_date)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error accessing repository: {e}")
            commits = []
            try:
                for commit in repo.traverse_commits():
                    commits.append(self.process_commit(commit))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error processing repository: {e}")
            self.cache.db.insert({"repo":  repo_path, "commits" : commits, "since": days})

        return [c for c in commits
                    if since_date <= datetime.fromisoformat(c["committer_date"]) <= datetime.now(timezone.utc)
                ]

    def process_commit(self, commit):
        # Gather a list of files modified in the commit
        files = []
        total_added_lines = 0
        total_deleted_lines = 0
        try:
            modified_files = commit.modified_files
            for f in modified_files:
                if f.new_path is not None:
                    file_type = self.file_service.get_file_type(f.new_path)
                    change_type = f.change_type.name if f.change_type else 'UNKNOWN'

                    # these are not attributes, they are functions, so we just wanna call them once
                    added_lines = f.added_lines
                    deleted_lines = f.deleted_lines

                    total_added_lines += added_lines
                    total_deleted_lines += deleted_lines
                    files.append({
                        "path": f.new_path,
                        "type": file_type,
                        "change_type": change_type,
                        "added_lines": added_lines,
                        "deleted_lines": deleted_lines
                    })
        except Exception:
            print(f'Could not read files for commit {hash}')

        record = {
            'hash': commit.hash,
            'message': str(commit.msg),
            'author_name': str(commit.author.name),
            'author_email': str(commit.author.email),
            'author_date': str(commit.author_date),
            'author_tz': str(commit.author_timezone),
            'branches': ', '.join(commit.branches),
            'committer_name': str(commit.committer.name),
            'committer_email': str(commit.committer.email),
            'committer_date': str(commit.committer_date),
            'committer_tz': str(commit.committer_timezone),
            'num_deletes': total_deleted_lines,
            'num_inserts': total_added_lines,
            'net_lines': total_added_lines - total_deleted_lines,
            'num_files': str(len(modified_files)),
            'files': files,
            'parents': ', '.join(commit.parents),
        }
        return record

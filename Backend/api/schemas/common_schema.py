from pydantic import BaseModel
from typing import List, Dict

class Message(BaseModel):
    message: str

class FileDetail(BaseModel):
    path: str
    type: str
    change_type: str
    added_lines: int
    deleted_lines: int


class CommitDetail(BaseModel):
    hash: str
    message: str
    branches: str
    author_name: str
    author_email: str
    author_date: str
    author_tz: str
    committer_name: str
    committer_email: str
    committer_date: str
    committer_tz: str
    num_deletes: int
    num_inserts: int
    net_lines: int
    num_files: str
    files: List[FileDetail]
    parents: str

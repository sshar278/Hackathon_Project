from dotenv import load_dotenv
import os
load_dotenv()
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

import json
import datetime

def main(event_body):
    data = json.loads(event_body)
    repo = f"{data['repository']['owner']['name']}/{data['repository']['name']}"
    commit = data.get('head_commit', data.get('commits', [{}])[-1])
    sha = commit.get('id', '')
    author = commit.get('author', {}).get('username', 'unknown')
    files_changed = (commit.get('added', []) + 
                     commit.get('modified', []) + 
                     commit.get('removed', []))
    diff_text = f"Message: {commit.get('message', '')}\nFiles: {files_changed}"
    return {
        'repo': repo,
        'sha': sha,
        'author': author,
        'files_changed': files_changed,
        'diff_text': diff_text,
        'created_at': datetime.datetime.utcnow().isoformat()
    }


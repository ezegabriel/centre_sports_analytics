import requests
import os


# --- SETTINGS ---
# Get the token from an environment variable (safer than putting it in the file)
TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = 'ezegabriel/centre_sports_analytics'
FILE_TO_DELETE = 'placeholder.txt'

# Headers that GitHub requires for authentication
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def get_default_branch():

    """Ask GitHub what the main branch of the repo is (usually 'main' or 'master')."""
    url = f"https://api.github.com/repos/{REPO}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()    # crash with a clear error if something is wrong
    return r.json()["default_branch"]

def get_full_tree():

    """
    Get EVERY file and folder in the entire repository in one go.
    This includes all nested folders (mens_basketball, SAA, 2011_12, etc.).
    """
    branch = get_default_branch()

    # 1. Get the latest commit on that branch
    url = f"https://api.github.com/repos/{REPO}/git/ref/heads/{branch}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    commit_sha = r.json()["object"]["sha"]

    # 2. Ask for the full recursive tree of that commit
    url = f"https://api.github.com/repos/{REPO}/git/trees/{commit_sha}?recursive=1"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["tree"]     # a big list of every file and folder

def delete_file(path, sha):

    """Delete one specific file using its full path and its unique SHA."""
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    data = {
        "message": f"Automated deletion of {FILE_TO_DELETE}",
        "sha": sha      # GitHub requires the current SHA to allow the delete
    }
    r = requests.delete(url, headers=HEADERS, json=data)
    if r.status_code in (200, 201):
        print(f"Deleted: {path}")
    else:
        print(f"Failed: {path} → {r.status_code}")
        print(r.text)

# ---------- MAIN ----------
print("Getting full tree...")
tree = get_full_tree()

print("Looking for every placeholder.txt...")
count = 0
for item in tree:
    # We only care about real files (type == "blob"), not folders
    if item["type"] == "blob" and item["path"].endswith(FILE_TO_DELETE):
        count += 1
        print(f"Found: {item['path']}")
        delete_file(item["path"], item["sha"])

print(f"Done. Deleted {count} file(s).")
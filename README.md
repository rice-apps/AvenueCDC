# AvenueCDC
Official AvenueCDC repo.

## Setup

### Install `uv`:

For Mac/Linux:
```bash
brew install uv
``` 
OR 
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Windows:
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
OR
```bash
winget install --id=astral-sh.uv  -e
```

### Install dependencies:

This creates `.venv` and installs everything from `pyproject.toml`.
```bash
uv sync
```

To add a package, use `uv add <package>` (or `uv add --dev <package>`), not `pip install`, and commit the updated `pyproject.toml` and `uv.lock`.

## Startup
Copy the env template and fill in the values:
```bash
cp .env.example .env
```

Run the server (no need to activate the virtual environment, `uv run` handles it):
```bash
uv run uvicorn main:app --reload
```

## Repo structure:

```text
avenuecdc/
├── content/ # intake scripts, chatbot q&a scripts
    └── call_agent/ 
    └── chatbot/ 
├── app/
    └── api/ # routes & webhooks (AI Call Agent)
    └── chat/ # single routes & webhook (chatbot)
    └── intake/ # fastapi endpoints
    └── reports/ # jinja report/package building
    └── tests/ 
├── project/
    └── design.md # project architecture
├── db/ # database updates, seeding
├── main.py
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

# Policies & best practices

## Branches

Create a new branch each time you start working on a NEW feature.

**Branch naming scheme:**
`voice/<feature>` or `chat/<feature>` based on what you're working on.

```
git pull
git switch -c <new branch name>
```
Do NOT push to the main branch. Only focus on your feature branch. 
```
git add <your files> (no env!)
git commit -m <message>
git push -u origin <your branch name>
```
Once you have completed working on your feature branch, raise a PR for team leads to review. Add `uma-menon` and `mertyercel` as reviewers.

## PRs:

- **PR Title: Add Notion Ticket to the title alongside a short description**
- Features added
- Dependencies added
- High-level changes per file
- Concerns or potential conflicts

## Documentation

- Leave inline comments everywhere
- Documentation for all methods (purpose, parameters, retvals)

## Learn More

To learn more about our techstack, please make use of the following:
 - [Twilio Docs](https://www.twilio.com/docs)
 - [ElevenLabs Docs](https://elevenlabs.io/docs/overview/intro)
 - [FastAPI Docs](https://fastapi.tiangolo.com/)
 - [Python Docs](https://docs.python.org/3/)
 - [Supabase Docs](https://supabase.com/docs)
 - [Salesforce Docs](https://developer.salesforce.com/docs)
 - [Docusign Docs](https://developers.docusign.com/)
 - [Jinja Docs](https://jinja.palletsprojects.com/en/stable/)
 - [Next.js Docs](https://nextjs.org/docs)
 - [Learn Next.js](https://nextjs.org/learn)

## Updated ENV File

For the application to work, please have the same variables as [.env.example](.env.example) in your .env file.

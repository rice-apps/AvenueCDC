# AvenueCDC
Official AvenueCDC repo.

## Startup
-- fill in -- 

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
    └── tests/ # in Claude we trust?
├── db/ # database updates, seeding
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

# Policies & best practices

## Branches

Create a new branch each time you start working on a NEW feature. 
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

- **PR Title: Add Notion Ticket to the title alongisde a short description**
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

For the application to work, please have these variables in your ENV file:
 - TBD
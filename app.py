  from fastapi import FastAPI
  from fastapi.middleware.cors import CORSMiddleware
  from pydantic import BaseModel
  from set_QA_chatbot import get_response, get_next_options, EN_options_dict, ES_options_dict

  app = FastAPI()
  app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

  MENUS = {"EN": EN_options_dict, "ES": ES_options_dict}

  class ChatRequest(BaseModel):
      question: str
      language: str = "EN"

  @app.get("/initial")
  def initial(language: str = "EN"):
      greeting = next(iter(MENUS[language]))
      return {"greeting": greeting, "options": get_next_options(greeting, language)}

  @app.post("/chat")
  def chat(req: ChatRequest):
      try:
          reply = get_response(req.question, req.language)
      except ValueError:
          return {"status": "error"}
      greeting = next(iter(MENUS[language]))
      return {"greeting": greeting, "options": get_next_options(greeting, language)}

  @app.post("/chat")
  def chat(req: ChatRequest):
      try:
          reply = get_response(req.question, req.language)
      except ValueError:
          return {"status": "error"}
      try:
          options = get_next_options(reply, req.language)
      except ValueError:
          options = []
      return {"status": "success", "reply": reply, "options": options}

import requests
import json
import time
from PyQt6.QtCore import QThread, pyqtSignal
from core.rag_engine import RAGEngine

class AIWorker(QThread):
    response_ready = pyqtSignal(str)
    
    def __init__(self, user_text, context_info=None, image_data=None):
        super().__init__()
        self.user_text = user_text
        self.context_info = context_info
        self.image_data = image_data # Base64 string
        self.api_url = "http://localhost:11434/api/generate"
        self.tags_url = "http://localhost:11434/api/tags"
        self.default_model = "gemma2"
        self.vision_model = "llava" # Or moondream
        
        # Initialize RAG Engine
        self.rag = RAGEngine()

    def run(self):
        try:
            # Simulate thinking time for animation UX (1.5s)
            time.sleep(1.5)
            
            # Determine Logic: Vision vs Text
            if self.image_data:
                self.process_vision_request()
            else:
                self.process_text_request()
        except Exception as e:
            self.response_ready.emit(f"AI Error: {str(e)}")

    def process_vision_request(self):
        # Vision + RAG Hybrid Request
        rag_context = self.rag.retrieve_context(self.user_text, k=2)
        
        if rag_context:
            final_prompt = f"User has shared their screen. Screen Context: {self.context_info}.\n[User's Personal Database Context:\n{rag_context}]\nUser Question: {self.user_text}. \nAnalyze the image and the provided database context to answer the user's question accurately. \nCRITICAL INSTRUCTIONS:\n1. Answer ONLY what is asked. Do NOT explain what the screen shows unless asked.\n2. Do NOT define terms (e.g., don't explain what Chrome or a Portfolio is).\n3. MUST answer in KOREAN (한국어)."
        else:
            final_prompt = f"User has shared their screen. Context: {self.context_info}. User Question: {self.user_text}. \nAnalyze the image and answer the user's question accurately. \nCRITICAL INSTRUCTIONS:\n1. Answer ONLY what is asked. Do NOT explain what the screen shows unless asked.\n2. Do NOT define terms (e.g., don't explain what Chrome or a Portfolio is).\n3. MUST answer in KOREAN (한국어)."
            
        payload = {
            "model": self.vision_model,
            "prompt": final_prompt,
            "images": [self.image_data],
            "stream": False
        }
        self.send_request(payload)

    def process_text_request(self):
        # Prepare Prompt with Context (if available)
        final_prompt = ""
        
        # System Instruction (Enforce Korean & Persona & Conciseness)
        system_instruction = (
            "You are Joy, a helpful and cute AI desktop assistant.\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. Answer ONLY what the user asked. Be direct and concise.\n"
            "2. Do NOT explain the context or define terms (e.g. don't say 'You are using Chrome').\n"
            "3. MUST answer in KOREAN (한국어)."
        )
        
        # Retrieve RAG context if any
        rag_context = self.rag.retrieve_context(self.user_text, k=3)
        
        context_parts = []
        if self.context_info:
             context_parts.append(f"User is currently working on: '{self.context_info}'")
        if rag_context:
             context_parts.append(f"User's Personal Database Context:\n{rag_context}")
             
        if context_parts:
            combined_context = "\n".join(context_parts)
            final_prompt = f"{system_instruction}\n[Context:\n{combined_context}]\nUser: {self.user_text}"
        else:
            final_prompt = f"{system_instruction}\nUser: {self.user_text}"
            
        print(f"DEBUG: Final Prompt sent to Ollama: {final_prompt}")
            
        # Check rules first
        rule_based_response = self.check_rules(self.user_text)
        if rule_based_response:
            self.response_ready.emit(rule_based_response)
            return

        # Auto-detect model if possible (this part is now effectively skipped for text requests as default_model is used directly)
        # current_model = self.get_available_model() # Original logic, now replaced by direct use of self.default_model

        payload = {
            "model": self.default_model, # Using default_model directly
            "prompt": final_prompt,
            "stream": False
        }
        self.send_request(payload)

    def send_request(self, payload):
        try:
            response = requests.post(self.api_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("response", "음... 답변을 읽을 수 없어요. 😅")
                self.response_ready.emit(answer)
            elif response.status_code == 404:
                # The model name is in payload["model"]
                model_name = payload.get("model", "알 수 없는 모델")
                self.response_ready.emit(f"모델 '{model_name}'을 찾을 수 없어요. `ollama pull {model_name}`을 해주세요! 🥺")
            else:
                self.response_ready.emit(f"Ollama 서버 오류입니다. (상태 코드: {response.status_code})")
                
        except requests.exceptions.ConnectionError:
            self.response_ready.emit("Ollama가 꺼져 있는 것 같아요. 🥲\n`ollama serve`를 실행해주세요!")
        except Exception as e:
            print(f"AI Error: {e}")
            self.response_ready.emit("오류가 발생했습니다. 다시 시도해주세요.")

    def get_available_model(self):
        try:
            # Fetch list of models
            response = requests.get(self.tags_url, timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                if models:
                    # Pick the first one, or prefer llama3/mistral if available
                    names = [m['name'] for m in models]
                    for preferred in ['llama3', 'mistral', 'gemma']:
                         if any(preferred in name for name in names):
                             # Find exact match or close match
                             return next((name for name in names if preferred in name), names[0])
                    return names[0] # Fallback to first available
        except:
            pass
        return self.model # Return default if fetch fails

    def check_rules(self, text):
        # Fallback/Fast rules
        text = text.lower()
        if "안녕" in text:
            return "안녕하세요! 오늘도 즐거운 코딩 되세요! 🚀"
        if "종료" in text and "알려줘" not in text:
            return "우클릭 메뉴에서 '종료'를 누르면 헤어질 수 있어요... 🥲"
        return None

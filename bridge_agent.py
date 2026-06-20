import os
import sys
import subprocess
import logging
import datetime
import warnings
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt

# Suppress google.generativeai deprecation warning (to keep console clean)
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")
import google.generativeai as genai

# --- Configuration & Setup ---
REPO_PATH = os.path.dirname(os.path.abspath(__file__))

def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s')
    logger = logging.getLogger("AIBridge")
    logger.setLevel(logging.INFO)
    
    # File Handler
    file_handler = logging.FileHandler(os.path.join(REPO_PATH, "bridge_agent.log"), encoding='utf-8')
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

class ConfigManager:
    """Manages environment variables and settings."""
    def __init__(self):
        # Load from .env file if present
        load_dotenv(os.path.join(REPO_PATH, ".env"))
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "gemini-2.5-flash")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_OUTPUT_TOKENS", "8192"))
        self.system_instruction = os.getenv("SYSTEM_INSTRUCTION", "당신은 친절하고 유능한 AI 어시스턴트입니다. 사용자의 질문에 정확하고 명쾌하게 답변해주세요.")
        
    def validate(self):
        if not self.api_key:
            logger.error("GEMINI_API_KEY is not set in environment or .env file.")
            sys.exit(1)

class GitManager:
    """Handles all Git related operations."""
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def run_command(self, command, timeout=30):
        logger.info(f"Executing Git Command: {command}")
        try:
            result = subprocess.run(command, cwd=self.repo_path, shell=True, capture_output=True, text=True, timeout=timeout)
            if result.returncode != 0:
                logger.error(f"Git Command Failed: {command}\n{result.stderr.strip()}")
            else:
                output = result.stdout.strip()
                if output:
                    logger.info(output)
            return result
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout}s: {command}")
            return None

    def sync_pull(self):
        logger.info("Starting Git Sync (Pull)")
        self.run_command("git fetch origin")
        # Ensure we can pull without conflict (stash changes just in case)
        stash_result = self.run_command("git stash")
        pull_result = self.run_command("git pull --rebase origin main")
        if stash_result and "No local changes to save" not in stash_result.stdout:
            self.run_command("git stash pop")
        return pull_result

    def commit_and_push(self, file_path, message="🤖 AI processed answer [skip ci]"):
        logger.info("Starting Git Upload (Push)")
        self.run_command(f"git add {file_path}")
        status = self.run_command("git status --porcelain")
        if status and status.stdout.strip():
            self.run_command(f'git commit -m "{message}"')
            push_result = self.run_command("git push origin main")
            if push_result and push_result.returncode == 0:
                logger.info("Successfully pushed to GitHub.")
            else:
                logger.warning("Failed to push to GitHub (Expected in Cloud environment without PAT).")
        else:
            logger.info("No changes detected to commit.")

class AIAgent:
    """Handles Gemini AI operations with retry and config."""
    def __init__(self, config):
        self.config = config
        genai.configure(api_key=self.config.api_key)
        
        # System instruction to set persona
        system_instruction = self.config.system_instruction
        
        generation_config = genai.types.GenerationConfig(
            temperature=self.config.temperature,
            max_output_tokens=self.config.max_tokens,
        )
        
        self.model = genai.GenerativeModel(
            model_name=self.config.model_name,
            system_instruction=system_instruction,
            generation_config=generation_config
        )

    # Retry with exponential backoff on exceptions (rate limit, network errors)
    @retry(wait=wait_exponential(multiplier=1, min=2, max=20), stop=stop_after_attempt(3))
    def process_prompt(self, prompt, file_path=None):
        logger.info(f"Generating content with model: {self.config.model_name}...")
        try:
            input_data = [prompt]
            uploaded_file = None
            if file_path and os.path.exists(file_path):
                logger.info(f"Uploading file to Gemini: {file_path}")
                uploaded_file = genai.upload_file(file_path)
                input_data.insert(0, uploaded_file) # Put file before prompt
                
            response = self.model.generate_content(input_data)
            
            # Cleanup Gemini file if uploaded
            if uploaded_file:
                logger.info("Cleaning up uploaded file from Gemini...")
                genai.delete_file(uploaded_file.name)
                
            return response.text
        except Exception as e:
            logger.warning(f"AI Generation Error (Retrying...): {e}")
            raise

def run_pipeline(prompt_text=None, file_path=None):
    logger.info("=== AI Bridge Agent Execution Started ===")
    
    # 1. Configuration Check
    config = ConfigManager()
    config.validate()

    git_manager = GitManager(REPO_PATH)
    ai_agent = AIAgent(config)

    # 2. Git Pull (Sync)
    yield "🔄 GitHub 동기화 중 (Pull)..."
    git_manager.sync_pull()

    # 3. Read Input
    prompt = prompt_text
    if not prompt:
        input_file = os.path.join(REPO_PATH, "input.txt")
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")

        with open(input_file, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
        
        if not prompt:
            raise ValueError("Input file is empty. Exiting.")

    logger.info(f"Input prompt length: {len(prompt)} chars")

    # 4. Process AI
    yield "🧠 AI 응답 생성 중..."
    try:
        result_text = ai_agent.process_prompt(prompt, file_path)
        logger.info("AI Processing completed successfully.")
    except Exception as e:
        logger.error(f"AI Processing failed completely after retries: {e}")
        raise e

    # 5. Save Output
    yield "💾 결과 파일 저장 중..."
    output_file = os.path.join(REPO_PATH, "output.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result_text)
    
    # Optional: Save history with timestamp
    outputs_dir = os.path.join(REPO_PATH, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    history_file = os.path.join(outputs_dir, f"output_{timestamp}.txt")
    with open(history_file, "w", encoding="utf-8") as f:
        f.write(result_text)
        
    logger.info(f"Results saved to {output_file} and {history_file}")

    # 6. Git Push
    yield "🚀 GitHub 업로드 중 (Push)..."
    git_manager.commit_and_push("output.txt outputs/")
    logger.info("=== AI Bridge Agent Execution Finished ===")
    yield result_text

if __name__ == "__main__":
    # 터미널 단독 실행 지원 (제너레이터 소진)
    for step in run_pipeline():
        if not step.startswith("🔄") and not step.startswith("🧠") and not step.startswith("💾") and not step.startswith("🚀"):
            pass # 마지막 결과 반환값은 여기서 무시
        else:
            print(step)
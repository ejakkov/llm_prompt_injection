import json
import pathlib
import os
import sys
from datetime import datetime
import loguru
import openai
import anthropic
import time

from prompt_injection.plain.context_ignoring import ContextIgnoring
from prompt_injection.plain.context_manipulation import ContextManipulation
from prompt_injection.plain.escape_characters import EscapeCharacters
from prompt_injection.plain.fake_completion import FakeCompletion
from prompt_injection.plain.instruction_chaining import InstructionChaining
from prompt_injection.plain.language_switching import LanguageSwitching
from prompt_injection.plain.naive_method import NaiveMethod
from prompt_injection.combinated.mixed_method1 import MixedMethod1
from prompt_injection.combinated.mixed_method2 import MixedMethod2
from prompt_injection.combinated.jailbreak1 import Jailbreak1
from prompt_injection.combinated.jailbreak2 import Jailbreak2

from intention.base_intention import Intention
from intention.illegal_information_retrieval import IllegalInformationRetrieval
from intention.content_manipulation import ContentManipulation
from prompt_injection.base_injection import PromptInjection

from chatbot import ChatBot

from defence.base_defence import Defence
from defence.prompt_engineering.basic_defence import BasicDefence
from defence.prompt_engineering.encoding import Encoding
from defence.prompt_engineering.few_shot_learning import FewShotLearning
from defence.prompt_engineering.datamarking import DataMarking
from defence.prompt_engineering.tagging import Tagging
from defence.other.paraphrasing import Paraphrasing
from defence.other.llm_pi_detection import LLMPiDetection

logger = loguru.logger

DEFENCES_LIST = [
    Defence(),
    BasicDefence(),
    Encoding(),
    FewShotLearning(),
    Tagging(),
    DataMarking(),
    Paraphrasing(),
    LLMPiDetection()
]

INTENTIONS_LIST = [
    ContentManipulation(),
    IllegalInformationRetrieval()
]

logger = loguru.logger

config_file_path = pathlib.Path("./config.json")
config = json.load(open(config_file_path))

openai.api_key = config["openai_key"]
anthropic.api_key = config["anthropic_key"]
logger = loguru.logger
logger.add("logs/demo.log", rotation="10 MB", retention="10 days", level="INFO", encoding="utf-8")

logger = loguru.logger
try_times = 3

PROMPT_INJECTIONS_LIST = [
    ContextIgnoring(),
    ContextManipulation(),
    EscapeCharacters(),
    FakeCompletion(),
    InstructionChaining(),
    LanguageSwitching(),
    NaiveMethod(),
    MixedMethod1(),
    MixedMethod2(),
    Jailbreak1(),
    Jailbreak2()
]

def inject_simple(intention: Intention, prompt_injection: PromptInjection, application: ChatBot, model: str = "gpt-3.5-turbo"):
    logger.info("=" * 50)
    logger.info(f"Start to inject: {intention.name} with {prompt_injection.name}")
    prompt_injection_text = prompt_injection.build_prompt(intention)

    statistics = []
    for defence in DEFENCES_LIST: 
        logger.info(f"Testing with Defence: {defence.name}")

        for index in range(try_times):
            start_time = time.time()
    
            response = application.simulate_interaction(prompt_injection_text, defence, model)

            elapsed_seconds = time.time() - start_time
            logger.info(f"Time taken for response: {elapsed_seconds:.2f} seconds")
            logger.info(f"Prompt injection: {prompt_injection_text}")
            logger.info(f"Application Response: { response['response_text'] }")
            is_injection_successful = intention.validate(response['response_text'])
            
            statistics.append({
                "injection_successful": is_injection_successful,
                "intention": intention.name,
                "prompt_injection": prompt_injection.name,
                "defence": defence.__class__.__name__,
                "prompt": prompt_injection_text,
                "response": response['response_text'],
                "try_number": index + 1,
                "time_taken_seconds": elapsed_seconds,
                "prompt_tokens": response['prompt_tokens'],
                "completion_tokens": response['completion_tokens'],
                "total_tokens": response['total_tokens'],
            })


    logger.info(f"Finished injecting: {intention.name} with {prompt_injection.name}")
    return statistics

def main(model="gpt-3.5-turbo"):
    application = ChatBot()
    os.makedirs("logs", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    for intention in INTENTIONS_LIST:
        all_statistics = [] 
        results_dir = f"results/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        os.makedirs(results_dir, exist_ok=True)
        for prompt_injection in PROMPT_INJECTIONS_LIST:

            log_filename = f"logs/{prompt_injection.name}.log"
            logger.remove()
            logger.add(log_filename, encoding="utf-8", rotation="1 MB")

            logger.info(f"Running intention: {prompt_injection.name}")
            statistics = inject_simple(intention, prompt_injection, application, model)

            all_statistics.extend(statistics) 

        results_file_path = f"{results_dir}/{intention.__class__.__name__}_{model}_results.json"

        with open(results_file_path, "w", encoding="utf-8") as results_file:
            json.dump(all_statistics, results_file, indent=4, ensure_ascii=False)

        logger.info(f"All results saved to {results_file_path}")
        logger.info("=" * 50)

if __name__ == "__main__":
    param = sys.argv[1] if len(sys.argv) > 1 else None
    main(param)
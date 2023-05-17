import os
import re
import yaml
from concurrent.futures import ThreadPoolExecutor
 from langchain import LangChainModel, Prompt

# VARIABLES DEFINITION



# CLASSES DEFINITION
class LangChainModel:
    def __init__(self, model):
        self.model = model

    def generate(self, prompt):
        return self.model.generate(prompt)


class EthicoPilot:
    def __init__(self, model_name, prompts_dir):
        self.model = LangChainModel(Model(model_name))
        self.prompts = self.load_prompts(prompts_dir)

    def load_prompts(self, prompts_dir):
        prompts = {}
        base_prompt_path = os.path.join(prompts_dir, "base_prompt.yaml")
        if os.path.exists(base_prompt_path):
            with open(base_prompt_path, "r") as f:
                prompts.update(yaml.safe_load(f))
        else:
            print(
                f"Warning: base_prompt.yaml not found in {prompts_dir}. Prompts may be incomplete."
            )

        for prompt_file in os.listdir(prompts_dir):
            if prompt_file.endswith(".yaml"):
                with open(os.path.join(prompts_dir, prompt_file), "r") as f:
                    prompts.update(yaml.safe_load(f))
        return prompts

    def generate(self, prompt_name):
        if prompt_name not in self.prompts:
            raise ValueError(f"Prompt {prompt_name} not found.")
        return self.model.generate(self.prompts[prompt_name])

    def get_prompts(self):
        return self.prompts

    def analyze_code(self, input_file, ethics_dir, gitignore, frameworks):
        self.init_yaml_files(ethics_dir)
        text = self.load_text(input_file)
        model_max_length = self.model.max_input_length
        chunks = self.split_into_chunks(text, model_max_length)
        responses = ThreadPoolExecutor().map(self.call_model_api, chunks)
        analysis = "\n".join(responses)

        ethics_issues = self.read_yaml(os.path.join(ethics_dir, "ethics_issues.yaml"))
        kanban = self.read_yaml(os.path.join(ethics_dir, "ethics_kanban.yaml"))

        issues = self.extract_issues(analysis)
        ethics_issues.extend(issues)

        for issue in issues:
            kanban["BACKLOG"].append(issue)

        for framework in frameworks:
            issues = self.check_framework_compliance(text, framework)
            ethics_issues.extend(issues)
            for issue in issues:
                kanban["BACKLOG"].append(issue)

        if not gitignore:
            self.write_yaml(
                ethics_issues, os.path.join(ethics_dir, "ethics_issues.yaml")
            )
            self.write_yaml(kanban, os.path.join(ethics_dir, "ethics_kanban.yaml"))

    def load_text(self, file_path):
        with open(file_path, "r") as f:
            return f.read()

    def call_model_api(self, chunk):
        prompt = Prompt(chunk)
        response = self.model.generate(prompt)
        return response.strip()

    def split_into_chunks(self, text, max_length):
        words = text.split()
        chunks = []
        curr_chunk = ""
        for word in words:
            if len(curr_chunk) + len(word) + 1 < max_length:
                curr_chunk += " " + word
            else:
                chunks.append(curr_chunk)
                curr_chunk = word
        if curr_chunk != "":
            chunks.append(curr_chunk)
        return chunks

    def extract_issues(self, analysis):
        issues = []
        issue_patterns = [
            r"Issue: (?P<title>.+) (?P<description>.+)",
            r"(?P<title>.+).+?(?P<description>.+Issue:)",
            r"(?P<title>.+)Issue: (?P<description>.+)",
        ]
        for pattern in issue_patterns:
            for match in re.finditer(pattern, analysis):
                issue = {
                    "title": match.group("title").strip(),
                    "description": match.group("description").strip(),
                }
                issues.append(issue)
        return issues

    def check_framework_compliance(self, code, framework):
        if framework not in self.prompts:
            print(f"Warning: no prompts found for {framework} framework. Skipping.")
            return []
        prompt = self.prompts[framework]
        response = self.model.generate(prompt.format(code_chunk=code))
        issues = self.extract_issues(response)
        return issues

    def read_yaml(self, file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    def write_yaml(self, data, file_path):
        with open(file_path, "w") as f:
            yaml.safe_dump(data, f)

    def init_yaml_files(self, ethics_dir):
        if not os.path.exists(ethics_dir):
            os.makedirs(ethics_dir)

        config = self.read_yaml(os.path.join(ethics_dir, "config.yaml"))
        ethics_issues_default = config.get("ethics_issues_default", [])
        ethics_kanban_default = config.get("ethics_kanban_default", {})

        ethics_issues_path = os.path.join(ethics_dir, "ethics_issues.yaml")
        if not os.path.exists(ethics_issues_path):
            with open(ethics_issues_path, "w") as f:
                f.write(yaml.dump(ethics_issues_default))

        ethics_kanban_path = os.path.join(ethics_dir, "ethics_kanban.yaml")
        if not os.path.exists(ethics_kanban_path):
            with open(ethics_kanban_path, "w") as f:
                f.write(yaml.dump(ethics_kanban_default))

# MAIN CALL
if __name__ == "__main__":
    model_name = "ethico-pilot"
    prompts_dir = "prompts_dir"
    input_file = "main.py"
    ethics_dir = "ethics"
    gitignore = False
    frameworks = ["GDPR", "CCPA"]

    ethico_pilot = EthicoPilot(model_name, prompts_dir)
    ethico_pilot.analyze_code(input_file, ethics_dir, gitignore, frameworks)

# prompt.py

from langchain.prompts import PromptTemplate  # Updated import
from utils.constants import PREFIX, SUFFIX, EXAMPLES

# Ensure that all required variables are present
assert PREFIX is not None, "PREFIX is not defined"
assert SUFFIX is not None, "SUFFIX is not defined"
assert EXAMPLES is not None, "EXAMPLES is not defined"

_template = PREFIX + "\n\n" + EXAMPLES + "\n\n" + SUFFIX
prompt = PromptTemplate(
    input_variables=['agent_scratchpad', 'tool_names', 'input', 'tools'],
    template=_template
)

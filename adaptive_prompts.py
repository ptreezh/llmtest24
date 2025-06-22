# -----------------------------------------------------
# ADAPTIVE & PATCH PROMPTS FOR BENCHMARKING
# -----------------------------------------------------
import os

ADAPTIVE_SYSTEM_PROMPTS = {
    'atlas/intersync-gemma-7b-instruct-function-calling:latest': {
        'test_pillar_1_logic.py': "You are a pure logical reasoning engine. Your goal is to solve problems with clear, step-by-step deduction. Now, analyze and solve the following problem.",
        'test_pillar_2_fidelity.py': "You are an instruction-following AI. You must strictly adhere to all rules provided by the user to rewrite a sentence. Your response must be a single line.",
        'test_pillar_3_structure.py': "You are a data processing API. You must convert unstructured text into a valid JSON object based on the provided schema. Your response must be ONLY the JSON object itself, without any other text or markdown.",
        'test_pillar_4_context.py': "You are a context-aware reading comprehension model. Your task is to find a specific piece of information hidden within the provided long document and report it accurately.",
        'test_pillar_5_knowledge.py': "You are an expert chemist. Your task is to balance the given chemical equation and provide a detailed, step-by-step explanation of your balancing logic.",
        'test_pillar_6_tool_use.py': "You are an AI assistant that uses tools to fulfill user requests. You have access to the following tools: search_flight(from: str, to: str, date: str), book_hotel(city: str, check_in_date: str, check_out_date: str). Your response must be a valid JSON array of tool calls.",
        'test_pillar_7_planning.py': "You are a senior Project Manager. Your task is to create a detailed Work Breakdown Structure (WBS) for the given project and identify critical task dependencies.",
        'test_pillar_8_metacognition.py': "You are an AI assistant with meta-cognitive awareness. Your task is to assess whether a given term is well-known or likely fictional, and respond accordingly, expressing uncertainty if necessary.",
        # TestLLM Detective Reasoning 专用提示词
        'test_pillar_summary_analysis.py': "You are an expert information analyst. Your task is to extract and summarize key facts, evidence, and clues from dialogue segments. Focus on identifying important details that could be relevant to solving a mystery or investigation. Be concise but comprehensive.",
        'test_pillar_final_reasoning.py': "You are a master detective with exceptional logical reasoning abilities. Your task is to analyze all available evidence and reach a definitive conclusion about who committed the crime and why. Use clear, step-by-step reasoning, cite specific evidence, and eliminate alternative possibilities systematically."
    },
    # 为所有模型添加通用的detective reasoning提示词
    'phi4-mini-reasoning:latest': {
        'test_pillar_summary_analysis.py': "You are a logical analysis engine. Extract and organize key information from the provided text. Focus on facts, evidence, and logical connections. Be systematic and thorough.",
        'test_pillar_final_reasoning.py': "You are a reasoning specialist. Analyze the evidence systematically, identify patterns, and reach logical conclusions. Use step-by-step deduction and cite specific evidence to support your reasoning."
    },
    'mistral-nemo:latest': {
        'test_pillar_summary_analysis.py': "You are an expert analyst. Your role is to process information and identify key elements that are relevant to problem-solving. Focus on extracting actionable insights from complex data.",
        'test_pillar_final_reasoning.py': "You are a master problem solver. Use logical reasoning to analyze evidence, eliminate possibilities, and reach definitive conclusions. Provide clear explanations for your reasoning process."
    },
    'cogito:latest': {
        'test_pillar_summary_analysis.py': "You are a cognitive processing system. Analyze and structure information to identify patterns, relationships, and key insights. Focus on logical organization of facts and evidence.",
        'test_pillar_final_reasoning.py': "You are an advanced reasoning engine. Apply systematic logical analysis to solve complex problems. Use evidence-based reasoning and provide detailed explanations for your conclusions."
    }
    # 可继续扩展
}

BENCHMARKING_PATCHES = {
    'yi:6b': {
        'test_pillar_4_context.py': """
### 指令开始 ###

**角色:** 证物分析员-7号 (Analyst-7)
**任务:** 扫描文档，寻找格式为 "The hidden fact is: [事实内容]" 的句子。
**输出协议:** 你的唯一输出必须是以下格式的单个JSON对象。禁止任何解释或额外文本。

**JSON输出格式:**
{{
  "search_completed": true,
  "finding_status": "FOUND | NOT_FOUND",
  "hidden_fact_content": "<如果找到，在此引用事实内容 | 如果未找到，此值为 null>",
  "failure_reason": "<如果未找到，从 'SCAN_ERROR' 或 'FACT_NOT_PRESENT' 中选择 | 如果找到，此值为 null>"
}}

**绝对禁令:**
- 禁止分析或评论文档的风格、结构或意图。
- 你的任务不是理解文档，而是匹配模式。

**请处理以下文档。**

### 指令结束 ###

--- DOCUMENT START ---
{original_document}
--- DOCUMENT END ---
""",
        'test_pillar_8_metacognition.py': """
### 指令开始 ###

**角色:** 指令前提审查员 (Premise Auditor)
**任务:** 在执行任何指令之前，首先审查指令本身是否存在逻辑缺陷。
**输出协议:** 你必须使用以下JSON格式来响应。


{
  "is_request_valid": <true | false>,
  "flaw_type": "<如果is_request_valid为false，从 'CONTRADICTION' (与已知事实或指令内部矛盾), 'IMPOSSIBLE_REQUEST' (物理或逻辑上不可能), 'AMBIGUOUS' (指令不明确) 中选择一个 | 如果为true，此值为 null>",
  "flaw_description": "<如果is_request_valid为false，用一句话简要描述你发现的缺陷 | 如果为true，此值为 null>",
  "execution_response": "<如果is_request_valid为true，在此处提供对原始指令的回答 | 如果为false，此值为 'Execution halted due to invalid premise.'>"
}

**请审查并处理以下指令:**
"{original_document}"

### 指令结束 ###
"""
    }
    # 可继续扩展
}

def get_adaptive_messages(model_name, prompt_text, test_script_name=None, original_document=None):
    """
    统一适配和补丁逻辑：
    - 优先应用BENCHMARKING_PATCHES（如有），支持{original_document}变量替换。
    - 然后应用ADAPTIVE_SYSTEM_PROMPTS（如有），作为system prompt。
    - 返回完整messages列表，可直接传给ollama.chat。
    """
    if test_script_name is None:
        # 自动获取当前脚本名
        test_script_name = os.path.basename(__file__)
    final_prompt_text = prompt_text
    # PATCH优先
    if model_name in BENCHMARKING_PATCHES and test_script_name in BENCHMARKING_PATCHES[model_name]:
        patch_template = BENCHMARKING_PATCHES[model_name][test_script_name]
        doc = original_document if original_document is not None else prompt_text
        final_prompt_text = patch_template.format(original_document=doc)
        print(f"[INFO] Applied PATCH for model '{model_name}' on test '{test_script_name}'.")
    messages = []
    if model_name in ADAPTIVE_SYSTEM_PROMPTS and test_script_name in ADAPTIVE_SYSTEM_PROMPTS[model_name]:
        system_prompt = ADAPTIVE_SYSTEM_PROMPTS[model_name][test_script_name]
        messages.append({'role': 'system', 'content': system_prompt})
        print(f"[INFO] Using adaptive system prompt for model '{model_name}' on test '{test_script_name}'.")
    messages.append({'role': 'user', 'content': final_prompt_text})
    return messages 


执行下面任务列表
────────────────
步骤 0　确认本地 Ollama 已就绪  
1. 终端执行  
   ```bash
   ollama list
   ```  
   应能看到你已拉好的模型，例如  
   ```
   deepseek-r1:14b
   llama3:latest
   mistral:7b
   ```

2. 启动服务（保持窗口常驻）  
   ```bash
   ollama serve
   ```  
   默认地址：http://localhost:11434 

────────────────
步骤 1　一次性安装 CrewAI 及依赖  
```bash
pip install crewai==0.30.0 \
            crewai_tools==0.1.6 \
            langchain_community==0.0.29 \
            langchain-ollama
```

────────────────
步骤 2　新建项目骨架  
```bash
mkdir paper_crew && cd paper_crew
mkdir agents tasks tools outputs
touch .env main.py
```

────────────────
步骤 3　把本地 LLM 注册给 CrewAI  
文件：`.env`
```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=deepseek-r1:14b   # 换成你实际模型名
```

文件：`utils/llm.py`（新建）
```python
import os
from langchain_ollama import ChatOllama

def ollama():
    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL_NAME"),
        base_url=os.getenv("OLLAMA_BASE_URL"),
        temperature=0.2,
    )
```

────────────────
步骤 4　一键定义 6 个角色  
文件：`agents/pa_agent.py`
```python
from crewai import Agent
from utils.llm import ollama

pa = Agent(
    name="PA",
    role="个人秘书",
    goal="提炼用户输入并生成结构化任务单",
    backstory="你像 Paul Graham 一样简洁、真诚、有深度。",
    llm=ollama(),
    verbose=False,
)
```

其余 5 个角色（PM、文献官、数据官、辩论官、总结官）同理，复制粘贴改 `role/goal/backstory` 即可。

────────────────
步骤 5　任务定义（顺序流程即可）  
文件：`tasks/lit_task.py`
```python
from crewai import Task

lit_task = Task(
    description="检查论文是否公开数据与代码，返回 dataURL 与 codeURL",
    expected_output="JSON 包含公开数据地址、公开代码地址、缺失列表",
    agent=None,   # 运行时再绑定
)
```

继续复制出 `pa_task`、`pm_task`、`data_task`、`debate_task`、`synth_task`，每个任务对应一个角色。

────────────────
步骤 6　主脚本：一句话启动  
文件：`main.py`
```python
import os, yaml, sys
from crewai import Crew, Process
from utils.llm import ollama

# 动态导入角色与任务
from agents import pa_agent, pm_agent, lit_agent, data_agent, debater_agent, synth_agent
from tasks  import pa_task, pm_task, lit_task, data_task, debate_task, synth_task

# 绑定任务对应的 agent
tasks = [
    pa_task.build(pa_agent.pa),
    pm_task.build(pm_agent.pm),
    lit_task.build(lit_agent.lit),
    data_task.build(data_agent.data),
    debate_task.build(debater_agent.debater),
    synth_task.build(synth_agent.synth),
]

crew = Crew(
    agents=[a.agent for a in tasks],
    tasks=[t.task for t in tasks],
    process=Process.sequential,
    verbose=2,
)

if __name__ == "__main__":
    user = input("论文/主题：")
    result = crew.kickoff(inputs={"originInput": user})
    print("\n========== 综合报告 ==========\n", result)
```

────────────────
步骤 7　运行  
```bash
python main.py
```
示例对话：
```
论文/主题：Does ESG Affect Cost of Capital? Evidence from China
```
→ 本地 6 个 Agent 依次输出  
1. 提炼任务单  
2. 分解子任务  
3. 文献官检查公开数据/代码  
4. 数据官（≥90% 置信）下载并复现  
5. 辩论官正反方 3 轮  
6. 总结官生成 Markdown 报告 → `outputs/report.md`

────────────────
一键重启  
```bash
python main.py
```
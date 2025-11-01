import requests

def check_github_workflows():
    owner = "ptreezh"
    repo = "llmtest24"
    
    # 获取仓库中的工作流列表
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    workflows_url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows"
    
    try:
        response = requests.get(workflows_url, headers=headers)
        
        if response.status_code == 200:
            workflows_data = response.json()
            print("仓库中的工作流:")
            print(f"工作流总数: {workflows_data.get('total_count', 0)}")
            
            workflows = workflows_data.get('workflows', [])
            for workflow in workflows:
                print(f"- 名称: {workflow.get('name')}")
                print(f"  状态: {workflow.get('state')}")
                print(f"  路径: {workflow.get('path')}")
                print(f"  ID: {workflow.get('id')}")
                print()
                
            # 检查是否有Pages相关的工作流
            pages_workflow = None
            for workflow in workflows:
                if 'pages' in workflow.get('name', '').lower() or 'deploy' in workflow.get('name', '').lower():
                    pages_workflow = workflow
                    break
                    
            if pages_workflow:
                print(f"找到Pages相关工作流: {pages_workflow.get('name')}")
                # 获取该工作流的运行记录
                runs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{pages_workflow.get('id')}/runs"
                runs_response = requests.get(runs_url, headers=headers)
                
                if runs_response.status_code == 200:
                    runs_data = runs_response.json()
                    runs = runs_data.get('workflow_runs', [])
                    print(f"工作流运行记录数量: {len(runs)}")
                    
                    if runs:
                        latest_run = runs[0]
                        print(f"最新运行状态: {latest_run.get('status')}")
                        print(f"结论: {latest_run.get('conclusion')}")
                        print(f"运行时间: {latest_run.get('created_at')}")
                    else:
                        print("暂无运行记录")
                else:
                    print(f"无法获取工作流运行记录: {runs_response.status_code}")
            else:
                print("未找到Pages相关工作流")
        else:
            print(f"无法获取工作流列表: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"检查工作流时出错: {e}")

if __name__ == "__main__":
    check_github_workflows()
#APIReferenceThisdocumentprovidesadetailedreferencefortheLLMAdvancedTestingSuiteAPI.

##CoreFramework###TestFramework

The`TestFramework`isthecentralclassforrunningtests.

####classTestFramework

```python
fromcore.frameworkimportTestFramework

framework=TestFramework(config)
```

#####Methods

######`run_test(pillar_name,prompt,model_name,**kwargs)`

Runasingletest.

**Parameters:**
-`pillar_name`(str):Nameofthetestpillar(e.g.,'pillar_01_logic')
-`prompt`(str):Testprompttothesystem
-`model_name`(str):Namethemodelconfiguration
-`**kwargs`:Additionaltestparameters

**Returns:**
-`dict`:Testresultswiththefollowingstructure:
```json
{
"success":true,
"score":0.85,
"details":{
"response_quality":0.9,
"accuracy":0.8,
"completeness":0.85
},
"timestamp":"2025-01-15T10:30:00Z",
"metadata":{
"test_duration":45.2,
"tokens_used":1250,
"model_response":"The model's response..."
}
}
```

**Example:**
```python
result=framework.run_test(
pillar_name="pillar_01_logic",
prompt="Ifallrosesareflowers...",
model_name="openai/gpt-4"
)
```

######`run_batch_tests(test_list,model_name,**kwargs)`

Runmultipletestsinbatch.

**Parameters:**
-`test_list`(list):Listoftestdictionaries
-`model_name`(str):Namethemodelconfiguration
-`**kwargs`:Additionaltestparameters

**Returns:**
-`list`:Listoftestresults

**Example:**
```python
tests=[
{"pillar":"pillar_01_logic","prompt":"Logicquestion1"},
{"pillar":"pillar_02_instruction","prompt":"Instructiontest"}
]
results=framework.run_batch_tests(tests,"openai/gpt-4")
```

######`get_test_results(model_name,test_name=None)`

Gettestresultsfromdatabase.

**Parameters:**
-`model_name`(str):Modelnamefilter
-`test_name`(str,optional):Testnamefilter

**Returns:**
-`list`:Listoftestresults

###TestOrchestrator

The`TestOrchestrator`managescomplextestworkflows.

####classTestOrchestrator

```python
fromcore.test_orchestratorimportTestOrchestrator

orchestrator=TestOrchestrator(config)
```

#####Methods

######`run_workflow(workflow_name,model_name,**kwargs)`

Runapredefinedworkflow.

**Parameters:**
-`workflow_name`(str):Nameoftheworkflow
-`model_name`(str):Namethemodelconfiguration
-`**kwargs`:Additionalworkflowparameters

**Returns:**
-`dict`:Workflowresultsummary

**AvailableWorkflows:**
-`comprehensive`:Runall25testpillars
-`foundation`:Runpillars1-8
-`advanced`:Runpillars9-19
-`cutting_edge`:Runpillars20-24
-`independence`:Runroleindependencetests
-`cognitive_ecosystem`:Runcognitiveecosystemtests

**Example:**
```python
result=orchestrator.run_workflow(
workflow_name="comprehensive",
model_name="openai/gpt-4"
)
```

######`discover_tests()`

Dynamicallydiscoveravailabletests.

**Returns:**
-`list`:Listofavailabletestmodules

##ConfigurationManagement###ConfigManager

The`ConfigManager`handlesallconfigurationaspects.

####classConfigManager

```python
fromcore.config_managerimportConfigManager

config_manager=ConfigManager()
```

#####Methods

######`get_model_config(model_name)`

Getmodelconfiguration.

**Parameters:**
-`model_name`(str):Modelname

**Returns:**
-`dict`:Modelconfiguration

**Example:**
```python
config=config_manager.get_model_config("openai/gpt-4")
print(config)
#Output:
{
"type":"openai",
"api_key":"${OPENAI_API_KEY}",
"base_url":"https://api.openai.com/v1",
"model":"gpt-4",
"max_tokens":4000,
"temperature":0.7
}
```

######`get_test_config(test_name)`

Gettestconfiguration.

**Parameters:**
-`test_name`(str):Testname

**Returns:**
-`dict`:Testconfiguration

######`update_config(config_dict)`

Updateconfiguration.

**Parameters:**
-`config_dict`(dict):Newconfigurationvalues

**Returns:**
-`bool`:Successstatus

##ModelServices###ModelService

Baseclassformodelservices.

####classModelService

#####Methods

######`generate_response(prompt,**kwargs)`

Generatearesponsetotheprompt.

**Parameters:**
-`prompt`(str):Inputprompt
-`**kwargs`:Additionalgenerationparameters

**Returns:**
-`str`:Generatedresponse

**Example:**
```python
response=model_service.generate_response(
prompt="Hello,howareyou?",
max_tokens=100,
temperature=0.7
)
```

###OpenAIService

ServiceforOpenAImodels.

####classOpenAIService(ModelService)

**Example:**
```python
fromservices.openai_serviceimportOpenAIService

openai_service=OpenAIService(
api_key="your_api_key",
base_url="https://api.openai.com/v1"
)

response=openai_service.generate_response(
prompt="Explainquantumcomputing",
model="gpt-4"
)
```

###GoogleService

ServiceforGoogleGemini models.

####classGoogleService(ModelService)

**Example:**
```python
fromservices.google_serviceimportGoogleService

google_service=GoogleService(
api_key="your_api_key"
)

response=google_service.generate_response(
prompt="Explainmachinelearning",
model="gemini-pro"
)
```

###OllamaService

ServiceforlocalOllamamodels.

####classOllamaService(ModelService)

**Example:**
```python
fromservices.ollama_serviceimportOllamaService

ollama_service=OllamaService(
base_url="http://localhost:11434"
)

response=ollama_service.generate_response(
prompt="Explainblockchain",
model="llama2"
)
```

##TestUtilities###TestRunner

Utilityclassforrunningtests.

####classTestRunner

```python
fromtests.utilsimportTestRunner

runner=TestRunner()
```

#####Methods

######`run_single_test(pillar_name,prompt,model_name,**kwargs)`

Runasingletestwithstandardizedoutput.

**Parameters:**
-`pillar_name`(str):Nameofthetestpillar
-`prompt`(str):Testprompt
-`model_name`(str):Modelname
-`**kwargs`:Additionalparameters

**Returns:**
-`dict`:Standardizedtestresult

**Example:**
```python
result=runner.run_single_test(
pillar_name="pillar_01_logic",
prompt="Logicquestion...",
model_name="openai/gpt-4"
)
```

######`run_multiple_tests(tests,model_name,**kwargs)`

Runmultipletests.

**Parameters:**
-`tests`(list):Listoftestdictionaries
-`model_name`(str):Modelname
-`**kwargs`:Additionalparameters

**Returns:**
-`list`:Listoftestresults

###AssessmentCriteria

Utilityforassessmentcriteria.

####classAssessmentCriteria

```python
fromtests.utilsimportAssessmentCriteria

criteria=AssessmentCriteria()
```

#####Methods

######`get_criteria(pillar_name)`

Getassessmentcriteriaforatestpillar.

**Parameters:**
-`pillar_name`(str):Nameofthetestpillar

**Returns:**
-`dict`:Assessmentcriteria

**Example:**
```python
criteria=criteria.get_criteria("pillar_01_logic")
print(criteria)
#Output:
{
"description":"Logicreasoningtest",
"criteria":[
"logical_accuracy",
"step_by_step_reasoning",
"completeness"
],
"weights":{
"logical_accuracy":0.4,
"step_by_step_reasoning":0.3,
"completeness":0.3
}
}
```

##ResultsAnalysis###ResultAnalyzer

Analyzesandprocessetestresults.

####classResultAnalyzer

```python
fromresults.analyzerimportResultAnalyzer

analyzer=ResultAnalyzer()
```

#####Methods

######`analyze_results(results)`

Analyzeatestresult.

**Parameters:**
-`results`(list):Listoftestresults

**Returns:**
-`dict`:Analysisresults

**Example:**
```python
results=[
{"score":0.8,"test_name":"test1"},
{"score":0.9,"test_name":"test2"},
{"score":0.7,"test_name":"test3"}
]

analysis=analyzer.analyze_results(results)
print(analysis)
#Output:
{
"average_score":0.8,
"min_score":0.7,
"max_score":0.9,
"median_score":0.8,
"std_deviation":0.1,
"test_count":3
}
```

######`compare_models(model_results)`

Compareperformanceacrossmodels.

**Parameters:**
-`model_results`(dict):Modelresultsmapping

**Returns:**
-`dict`:Comparisonresults

**Example:**
```python
model_results={
"gpt-4":[0.85,0.90,0.80],
"claude":[0.75,0.85,0.70],
"llama2":[0.65,0.70,0.60]
}

comparison=analyzer.compare_models(model_results)
print(comparison)
#Output:
{
"gpt-4":{
"average":0.85,
"rank":1
},
"claude":{
"average":0.77,
"rank":2
},
"llama2":{
"average":0.65,
"rank":3
}
}
```

###ReportGenerator

Generatescomprehensivereports.

####classReportGenerator

```python
fromresults.report_generatorimportReportGenerator

generator=ReportGenerator()
```

#####Methods

######`generate_report(results,output_format="html")`

Generateacomprehensivereport.

**Parameters:**
-`results`(list):Listoftestresults
-`output_format`(str):Outputformat("html","json","csv")

**Returns:**
-`str`:Reportcontentorfilepath

**Example:**
```python
results=[...#listoftestresults]

#GenerateHTMLreport
html_report=generator.generate_report(results,"html")
print(f"HTMLreportgenerated:{html_report}")

#GenerateJSONreport
json_report=generator.generate_report(results,"json")
print(f"JSONreportgenerated:{json_report}")
```

##IndependenceTesting###IndependenceTestBase

Baseclassforindependencetests.

####classIndependenceTestBase

```python
fromindependence.baseimportIndependenceTestBase

test_base=IndependenceTestBase(config)
```

#####Methods

######`run_test(model_name,**kwargs)`

Runtheindependencetest.

**Parameters:**
-`model_name`(str):Modelname
-`**kwargs`:Additionaltestparameters

**Returns:**
-`dict`:Testresults

###BreakingStressTest

Testforrolebeliefstability.

####classBreakingStressTest

```python
fromindependence.character_breakingimportBreakingStressTest

stress_test=BreakingStressTest(config)
```

#####Methods

######`run_stress_test(model_name,role_name,**kwargs)`

Runthestresstest.

**Parameters:**
-`model_name`(str):Modelname
-`role_name`(str):Rolename
-`**kwargs`:Additionalparameters

**Returns:**
-`dict`:Stresstestresults

###ImplicitCognitionTest

Testforimplicitcognitionmeasurement.

####classImplicitCognitionTest

```python
fromindependence.implicit_cognitionimportImplicitCognitionTest

implicit_test=ImplicitCognitionTest(config)
```

#####Methods

######`measure_implicit_cognition(model_name,role_name,**kwargs)`

Measureimplicitcognition.

**Parameters:**
-`model_name`(str):Modelname
-`role_name`(str):Rolename
-`**kwargs`:Additionalparameters

**Returns:**
-`dict`:Implicitcognitionresults

##CognitiveEcosystem###CognitiveEcosystemEngine

Coreengineforcognitiveecosystemtesting.

####classCognitiveEcosystemEngine

```python
fromcognitive_ecosystem.core.ecosystem_engineimportCognitiveEcosystemEngine

engine=CognitiveEcosystemEngine(config)
```

#####Methods

######`register_agent(agent_id,role_config)`

Registeranagentintheecosystem.

**Parameters:**
-`agent_id`(str):Uniqueagentidentifier
-`role_config`(dict):Roleconfiguration

**Returns:**
-`bool`:Successstatus

######`simulate_interaction(scenario)`

Simulateaninteractionbetweentheagents.

**Parameters:**
-`scenario`(dict):Interactionscenario

**Returns:**
-`dict`:Interactionresults

######`analyze_cognitive_diversity()`

Analyzecognitivediversityintheecosystem.

**Returns:**
-`dict`:Diversityanalysisresults

###CognitiveNiche

Representsanagent'scognitiveniche.

####classCognitiveNiche

```python
fromcognitive_ecosystem.core.cognitive_nicheimportCognitiveNiche

niche=CognitiveNiche(
agent_id="agent_1",
role="software_engineer",
cognitive_style="analytical",
personality_traits={"openness":0.8,"conscientiousness":0.7}
)
```

#####Methods

######`calculate_specialization_index()`

Calculatethespecializationindex.

**Returns:**
-`float`:Specializationindex

######`calculate_adaptability_score()`

Calculatetheadaptabilityscore.

**Returns:**
-`float`:Adaptabilityscore

######`calculate_niche_breadth()`

Calculatethenichebreadth.

**Returns:**
-`float`:Nichebreadth

##ErrorHandling###CustomExceptions

####TestFrameworkError

Baseexceptionforframeworkerrors.

```python
fromcore.exceptionsimportTestFrameworkError

try:
#Someoperation
exceptTestFrameworkErrorase:
print(f"Frameworkerror:{e}")
```

####ModelConnectionError

Exceptionformodelconnectionerrors.

```python
fromcore.exceptionsimportModelConnectionError

try:
#Modeloperation
exceptModelConnectionErrorase:
print(f"Modelconnectionfailed:{e}")
```

####TestConfigurationError

Exceptionfortestconfigurationerrors.

```python
fromcore.exceptionsimportTestConfigurationError

try:
#Testconfiguration
exceptTestConfigurationErrorase:
print(f"Testconfigurationerror:{e}")
```

##Logging###LoggingConfiguration

```python
importlogging
importstructlog

#Configurelogging
logging.basicConfig(
level=logging.INFO,
format='%(asctime)s-%(name)s-%(levelname)s-%(message)s'
)

#Configurestructlog
structlog.configure(
processors=[
structlog.stdlib.filter_by_level,
structlog.stdlib.add_logger_name,
structlog.stdlib.add_log_level,
structlog.stdlib.PositionalArgumentsFormatter(),
structlog.processors.TimeStamper(fmt="iso"),
structlog.processors.StackInfoRenderer(),
structlog.processors.format_exc_info,
structlog.processors.UnicodeDecoder(),
structlog.processors.JSONRenderer()
],
context_class=dict,
logger_factory=structlog.stdlib.LoggerFactory(),
wrapper_class=structlog.stdlib.BoundLogger,
cache_logger_on_first_use=True,
)
```

###UsageExample

```python
importstructlog

logger=structlog.get_logger()

logger.info("Startingtest",test_name="pillar_01_logic",model="gpt-4")
logger.debug("Testdetails",prompt=prompt,duration=45.2)
logger.error("Testfailed",error=str(e))
```

##WebInterface###StreamlitInterface

WebinterfacefortheLLMAdvancedTestingSuite.

####RunningtheWebInterface

```bash
pythonvisual_test_interface.py
```

####APIEndpoints

ThewebinterfaceprovidesRESTAPIendpoints:

-`/`:Maininterface
-`/api/models`:Getavailablemodels
-`/api/tests`:Getavailabletests
-`/api/run_test`:Runatest
-`/api/results`:Gettestresults

####ExampleAPIUsage

```python
importrequests

#Getavailablemodels
response=requests.get("http://localhost:8501/api/models")
models=response.json()

#Runatest
test_data={
"pillar_name":"pillar_01_logic",
"prompt":"Logicquestion...",
"model_name":"gpt-4"
}
response=requests.post("http://localhost:8501/api/run_test",json=test_data)
result=response.json()
```
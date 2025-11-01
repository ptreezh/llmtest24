#!/bin/bash#LLMAdvancedTestingSuite-QuickSetupScript#Thisscripthelpsuserssetupthetestingsuiteenvironmentquickly.

set-eecho"=================================================================="
echo"🚀LLMAdvancedTestingSuite-QuickSetup"
echo"=================================================================="
echo#CheckifPythonisavailableecho"🔍CheckingPythonavailability..."
if!command-vpython3&>/dev/null;thenecho"❌Python3isnotinstalled"
echo"PleaseinstallPython3.8orhigherfirst"
exit1fiPYTHON_VERSION=$(python3-c'importsys;print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo"✅Python$PYTHON_VERSIONisavailable"

#Checkifpipisavailableecho"🔍Checkingpipavailability..."
if!command-vpip3&>/dev/null;thenecho"❌pip3isnotavailable"
echo"Pleaseinstallpip3first"
exit1fiecho"✅pip3isavailable"

#Createvirtualenvironmentecho"🔍Checkingforvirtualenvironment..."
if[!-d"venv"];thenecho"📦Creatingvirtualenvironment..."
python3-mvenvvenvecho"✅Virtualenvironmentcreated"
elseecho"✅Virtualenvironmentalreadyexists"
fi#Activatevirtualenvironmentecho"🔧Activatingvirtualenvironment..."
sourcevenv/bin/activateecho"✅Virtualenvironmentactivated"

#Upgradepipecho"📦Upgradingpip..."
pipinstall--upgradepip#Installdependenciesecho"📦Installingdependencies..."
pipinstall-rrequirements.txt#Installoptionaldependenciesecho"🤔Installoptionaldependencies?(y/N):"
read-rinstall_optionalif[[$install_optional=~^[Yy]$]];thenecho"📦Installingoptionaldependencies..."
pipinstall-rrequirements-optional.txtfi#Createnecessarydirectoriesecho"📁Creatingnecessarydirectories..."
mkdir-ptestoutresultstest_logsmemory_dbdocs/buildexamplesecho"✅Directoriescreated"

#Setupenvironmentconfigurationecho"⚙️Settingupenvironmentconfiguration..."
if[!-f"config/.env"]&&[-f"config/.env.example"];thenecho"📝Creating.envfilefromtemplate..."
cpconfig/.env.exampleconfig/.envecho"✅.envfilecreated"
echo"📝Pleaseeditconfig/.envwithyourAPIkeysandmodelconfigurations"
elif[-f"config/.env"];thenecho"✅.envfilealreadyexists"
elseecho"⚠️.env.examplenotfound,pleasecreateconfig/.envmanually"
fi#Runinitialtestsecho"🧪Runninginitialtests..."
python3-c"
importsyssys.path.append('.')
try:
fromcore.frameworkimportTestFrameworkfromconfig.configimportMODEL_TO_TESTprint('✅Coremodulesimportedsuccessfully')
exceptImportErrorase:
print(f'❌Importerror:{e}')
sys.exit(1)
"
if[$?-eq0];thenecho"✅Initialtestspassed"
elseecho"❌Initialtestsfailed"
exit1fiechoecho"🎉Installationcompletedsuccessfully!"
echoecho"📋Nextsteps:"
echo"1.Configureyourmodels:"
echo"-Editconfig/.envwithyourAPIkeys"
echo"-Updateconfig/models.txtwithyourmodelconfigurations"
echoecho"2.Runyourfirsttest:"
echo"sourcevenv/bin/activate"
echo"pythonscripts/main_orchestrator.py--modelyour_model_name"
echoecho"3.Formoreinformation,see:"
echo"-README.mdforquickstartguide"
echo"-docs/fordetaileddocumentation"
echo"-CONTRIBUTING.mdfordevelopmentguidelines"
echo
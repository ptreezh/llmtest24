@echooffREMLLMAdvancedTestingSuite-WindowsSetupScriptREMThisscripthelpsuserssetupthetestingsuiteenvironmentonWindows.

echo====================================================================
echo🚀LLMAdvancedTestingSuite-QuickSetup(Windows)
echo====================================================================
echo.

REMCheckifPythonisavailableecho🔍CheckingPythonavailability...
python--version>nul2>&1iferrorlevel1(
echo❌PythonisnotinstalledechoPleaseinstallPython3.8orhigherfirstpauseexit/b1)

echo✅Pythonisavailableecho.

REMCheckifpipisavailableecho🔍Checkingpipavailability...
pip--version>nul2>&1iferrorlevel1(
echo❌pipisnotavailableechoPleaseinstallpipfirstpauseexit/b1)

echo✅pipisavailableecho.

REMCreatevirtualenvironmentecho🔍Checkingforvirtualenvironment...
ifnotexist"venv"(
echo📦Creatingvirtualenvironment...
python-mvenvvenvecho✅Virtualenvironmentcreated)else(
echo✅Virtualenvironmentalreadyexists)

echo.

REMActivatevirtualenvironmentecho🔧Activatingvirtualenvironment...
callvenv\Scripts\activate.batecho✅Virtualenvironmentactivatedecho.

REMUpgradepipecho📦Upgradingpip...
python-mpipinstall--upgradepipecho.

REMInstalldependenciesecho📦Installingdependencies...
pipinstall-rrequirements.txtecho.

REMInstalloptionaldependenciesecho🤔Installoptionaldependencies?(y/N):
set/pinstall_optional=
if/i"%install_optional%"=="y"(
echo📦Installingoptionaldependencies...
pipinstall-rrequirements-optional.txtecho.
)

REMCreatenecessarydirectoriesecho📁Creatingnecessarydirectories...
ifnotexist"testout"mkdirtestoutifnotexist"results"mkdirresultsifnotexist"test_logs"mkdirtest_logsifnotexist"memory_db"mkdirmemory_dbifnotexist"docs\build"mkdirdocs\buildifnotexist"examples"mkdirexamplesecho✅Directoriescreatedecho.

REMSetupenvironmentconfigurationecho⚙️Settingupenvironmentconfiguration...
ifnotexist"config\.env"(
ifexist"config\.env.example"(
echo📝Creating.envfilefromtemplate...
copyconfig\.env.exampleconfig\.envecho✅.envfilecreatedecho📝Pleaseeditconfig\.envwithyourAPIkeysandmodelconfigurations)else(
echo⚠️.env.examplenotfound,pleasecreateconfig\.envmanually)
)else(
echo✅.envfilealreadyexists)

echo.

REMRuninitialtestsecho🧪Runninginitialtests...
python-c"
importsyssys.path.append('.')
try:
fromcore.frameworkimportTestFrameworkfromconfig.configimportMODEL_TO_TESTprint('✅Coremodulesimportedsuccessfully')
exceptImportErrorase:
print(f'❌Importerror:{e}')
sys.exit(1)
"
if%errorlevel%equ0(
echo✅Initialtestspassed)else(
echo❌Initialtestsfailedpauseexit/b1)

echo.
echo🎉Installationcompletedsuccessfully!
echo.
echo📋Nextsteps:
echo1.Configureyourmodels:
echo-Editconfig\.envwithyourAPIkeysecho-Updateconfig\models.txtwithyourmodelconfigurationsecho.
echo2.Runyourfirsttest:
echovenv\Scripts\activate.batechopythonscripts\main_orchestrator.py--modelyour_model_nameecho.
echo3.Formoreinformation,see:
echo-README.mdforquickstartguideecho-docs\fordetaileddocumentationecho-CONTRIBUTING.mdfordevelopmentguidelinesecho.
pause
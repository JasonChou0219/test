:: The standard wheel installation of protobuf doesn't allow the use of multiple files with the same name in the same
:: pool. All SiLA device implement the standard features, thus, this is problematic. The protobuf --no-binary
:: installation is different to the wheel and allows just that.All

:: The following code uninstalls the standard installation and replaces it with the binary build. pipenv doesn't
:: implement the --no-binary flag. Thus pip is used. Protobuf is added to the pipfile afterwards for completenes sake
:: (Cosmetic issue).

pip cache purge
set PIP_NO_CACHE_DIR=false
set PIP_NO_BINARY=":all"
:: set  PIP_NO_BINARY=protobuf
pip install --no-binary=:all: protobuf
pipenv install protobuf
set PIP_NO_CACHE_DIR=true

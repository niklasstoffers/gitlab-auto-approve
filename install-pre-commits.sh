#!/bin/bash
echo "Installing necessary packages..."
pip_output=$(pip install pre-commit==3.6.0 2>&1)
ret=$?

if [ $ret -ne 0 ]; then
    echo "Package installation failed"
    echo $pip_output
else
    echo "Successfully installed necessary packages!"
fi

echo "Please enter GitGuardian API key for ggshield pre-commit scan job"
stty -echo
read -p 'Gitguardian API key: ' gg_api_key; echo
stty echo

export_global=
while ! [[ $export_global = "y" || $export_global = "N" ]]; do
    read -p 'Do you want to add the API key as a global variable? Otherwise it has to be set each time environment variables are being reloaded [y/N]: ' export_global
done

export GITGUARDIAN_API_KEY=$gg_api_key
if [ $export_global = "y" ]; then
    echo "Exporting GitGuardian API key..."
    echo "export GITGUARDIAN_API_KEY="$gg_api_key"">>~/.bashrc
else
    echo "GitGuardian API key will not be exported"
fi

echo "Installing pre-commit..."
install_output=$(pre-commit install 2>&1)
ret=$?

if [ $ret -ne 0 ]; then
    echo "Installing pre-commit hooks failed"
    echo $install_output
else
    echo "Successfully installed pre-commit hooks!"
fi

python3.7 -m venv /home/phil/vscode_proj/gcp_arb_dashboard/.env
source /home/phil/vscode_proj/gcp_arb_dashboard/.env/bin/activate

pip install -r requirements.txt


gcloud functions deploy dashboard --memory=256MB --runtime python37 --trigger-http

test
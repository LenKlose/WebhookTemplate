# Webhook App-Template

## Prerequisites
- Python 3.9 - 3.11
    - with pip installed (if you know/have Poetry you can also do the following steps with Poetry)

## Get started
1. Create venv
    ```bash
    python -m venv .venv
    ```
2. Activate venv
    - Windows:
    ```bash
    .venv\Scripts\activate.bat
    ```
    - Linux:
    ```bash
    source .venv/bin/activate
    ```
3. Install packages
    ```bash
    pip install -r requirements.txt
    ```
4. Start service
    ```bash
    uvicorn main:app --reload --port 5000
    ```

<br>

- Your app should now be accessible via `http://localhost:5000/APP_NAME`
- You can change the appname in `core/constants.py`

<br>

5. Forward local port to the internet
    Run
    ```bash
    ssh -R <SOME_IDENTIFIER>:80:127.0.0.1:5000 tunnel.appbuilder.community
    ```

<br>

- Your app should now be accessible via `https://<SOME_IDENTIFIER>.tunnel.appbuilder.community/APP_NAME`

## Update Webhook
1. Open `https://<base_uri>/dmsconfig/r/<repo_uuid>/events`
2. Open "Dokumente oder Akten erstellen"
3. Select "Nach dem Erstellen eines Dokuments oder einer Akte"
4. Change the URL of the Webhook to: `/{APP_NAME}/predict_document/{repo_uuid}`


## Update App URL
1. Overwrite app url with your custom url (`http://<SOME_IDENTIFIER>.tunnel.appbuilder.community`)


# Test your code
Change `EDITOR` and `API_KEY` in `core/constants.py`.

## Trigger webhooks
```bash
python repo_utils.py upload
```

## Reset repository
```bash
python repo_utils.py reset
```
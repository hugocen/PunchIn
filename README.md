# PunchIn
Automatic punch in/out with GitHub Action

## Monthly Auto Update

Please reference to [auto_punch_last_mont.yaml](.github/workflows/auto_punch_last_mont.yaml)

## Manully Update

### Setup

```
pip install -r requirements.txt
```

And you also need a GCP account, a service account, and service account's credential.  
[Create credentials](https://developers.google.com/workspace/guides/create-credentials)

### Usage

```
python history_make_up.py -c authorization.json -i <GOOGLE_SPREADSHEET_ID> -y 2021 -s 4 -e 9
```

### Notices
Using sleeps to avoid Google Sheets API quota limit for 100 requests per 100 seconds.

## Next Steps

- [ ] Use GitHub Actions to automate daily punch in/out.
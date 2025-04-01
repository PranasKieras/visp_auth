# visp_auth
Install app osdk

```
export FOUNDRY_TOKEN=YOUR_FOUNDRY_TOKEN
export FOUNDRY_CLIENT_ID=FOUNDRY_CLIENT_ID
export FOUNDRY_CLIENT_SECRET=FOUNDRY_CLIENT_SECRET
```
```commandline
pip install test_viisp_login_sdk==0.5.0  --upgrade
--extra-index-url "https://user:$FOUNDRY_TOKEN@vdv.stat.gov.lt/artifacts/api/repositories/ri.artifacts.main.repository.6fedef84-16f9-4104-b888-8579f26cebb7/contents/release/pypi/simple"
--extra-index-url "https://user:$FOUNDRY_TOKEN@vdv.stat.gov.lt/artifacts/api/repositories/ri.foundry-sdk-asset-bundle.main.artifacts.repository/contents/release/pypi/simple"
```

Run app locally
``` 
uvicorn main:app --reload --host 0.0.0.0 --port 3001 
```

- start API server locally 
  - `sam build; sam local start-api`
- deploy
  - `sam build; sam deploy`
  - `DOCKER_BUILDKIT=0 sls deploy --stage dev --aws-profile zume --region ap-northeast-3 --debug`
- test
  - `pytest -vvs --cov --cov-branch --cov-report=html`


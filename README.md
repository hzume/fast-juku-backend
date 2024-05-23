- start API server locally 
  - `sam build; sam local start-api`
- deploy
  - `sam build; sam deploy`
  - `sls deploy --stage dev --aws-profile zume_aws`
- test
  - `pytest -vvs --cov --cov-branch --cov-report=html`


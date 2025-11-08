#!/bin/bash
source .env
curl -X POST http://localhost:8787/sources/github_webhook \
  -H "Content-Type: application/json" \
  -d @mock_push.json
curl http://localhost:8787/api/reviews/latest?limit=1


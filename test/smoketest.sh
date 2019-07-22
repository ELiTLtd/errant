#!/bin/bash

curl -d "@fixtures.json" -X POST http://localhost:3000/annotate -H "Content-Type: application/json"

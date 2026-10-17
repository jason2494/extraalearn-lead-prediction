---
title: ExtraaLearn Backend
sdk: docker
app_port: 7860
---

# ExtraaLearn Backend

Flask API serving the uploaded tuned Gradient Boosting pipeline.
GET `/` checks availability. POST `/v1/predict` accepts a JSON lead.
POST `/v1/predict_batch` accepts a CSV in multipart field `file`.

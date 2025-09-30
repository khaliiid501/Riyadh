FROM python:3.11-slim
WORKDIR /app
COPY apps/backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY apps/backend/app ./app
# مجلدات للمخرجات والنماذج
RUN mkdir -p /models /reports
ENV AVM_MODEL_PATH=/models/avm_catboost.joblib
ENV REPORT_OUTPUT_DIR=/reports
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
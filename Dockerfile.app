FROM python:3.10-slim

WORKDIR /app

COPY . .

# Upgrade pip + fix network/hash issues + faster install
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=200 \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    streamlit \
    streamlit-autorefresh \
    pandas \
    numpy==1.26.4 \
    matplotlib \
    seaborn \
    plotly \
    scikit-learn

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]

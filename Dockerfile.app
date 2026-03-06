FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --default-timeout=100 --prefer-binary \
    streamlit \
    streamlit-autorefresh \
    pandas \
    numpy \
    matplotlib \
    seaborn \
    plotly \
    scikit-learn

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]

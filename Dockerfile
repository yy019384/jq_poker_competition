FROM python:3.5
RUN pip install pypokerengine -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app

COPY ./main.py /app/

ENTRYPOINT ["python3", "/app/main.py"]

# docker run -it --rm --name=pokerengine_test -v $(pwd)/players:/app/players pokerengine

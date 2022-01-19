# jq_poker_competition
JQ wintership 2022 poker AI competition



## Dependency

- Docker

## How to use

1. build (for once) with

  ```
docker build -t pokerengine .
```

2. run with

  ```
docker run -it --rm --name=pokerengine_test -v $(pwd)/players:/app/players pokerengine
```

3. add custom poker AI

  you have full control over the `players` folder, feel free to add your own AI or remove the existing dummy AIs. You don't need to rebuild image after change `players` folder, as you can see it is mounted to the container.

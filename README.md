# jq_poker_competition
JQ wintership 2022 poker AI competition



## Dependency

- Docker

## How to use

1. Build (for once) with

  ```
docker build --network=host -t pokerengine .
```

2. Run with

  ```
docker run -it --rm --name=pokerengine_test -v /path/to/players:/app/players pokerengine
```
  Replace `/path/to/players` with the absolute path to `players` folder.

  It has 3 optional parameters, run above command with an extra `-h` for details

3. Add custom poker AI

  You have full control over the `players` folder, feel free to add your own AI or remove the existing dummy AIs. You don't need to rebuild image after change `players` folder, as you can see it is mounted to the container.

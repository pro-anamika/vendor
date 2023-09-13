# How to run project.
-   ## Make virtual environment:
    ```sh
    python -m venv env
    ```
-   ## Activate virtual environment
    windows 
    ```sh
    env\Scripts\activate
    ```
    Linux
    ```sh
    source env/bin/activate
    ```
-   ## Install dependency
    ```sh
    pip install -r requirements.txt
    ```
-   ## Start redis server
    Open a new tab and run redis server. You can run it natively or run on docker. Since redis is not natively supported on windows hence it needs to be run through docker
    ```sh
    docker run --name some-redis -d redis
    ```
    Docker engine should already be installed.
 
-   ## Start django server
    ```sh
    python manage.py runserver
    ```


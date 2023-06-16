# Pharmeasy Customer Reviews Scraper

A web-scraper application that scrapes Customer Reviews of a product on [Pharmeasy](https://pharmeasy.in/) and injects them in a csv file.


## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

<h2>Installation</h2>

Run the following to install all the dependencies
```bash
pip install -r requirements.txt
```

<h2>Usage</h2>

- To run the application, run the following command on the terminal

```bash
uvicorn app:app --reload
```

- Now, open the following local host link on your browser: `http://127.0.0.1:8000/docs`. This should open the SwaggerUI for FastAPI.

- Expand the `POST` request dropdown.

- Press Try it Out, paste the desired link and excecute the code.


# Fitster - A fitness subscription application


## Testing

This project contains unit tests for each app as well as tests for templates. We have tested each view, model, and form of each app using the following tools and technologies:

- pytest
- pytest-django
- factory-boy
- pytest-factoryboy
- faker
- coverage
- django's default test module

The front end is tested manually from the user end and admin end. We've also used chrome dev tools for front-end testing.

## Running Tests

To test all the apps of the project, follow the following procedures:

- For testing all the apps, run

```bash
pytest
```

or

```bash
pytest -rP
```

- To test contact app models, forms and views, run

```bash
pytest contact -rP
```

> -rP is optional

<details>
<summary>Last test results for contact app</summary>

![tests](readme/src/images/contact_tests_results.png)
</details>

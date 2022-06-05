# Fitster - A fitness subscription & e-commerce application

Fitster is a fitness subscription & e-commerce application built to sell subscriptions and fitness products to customers in a simple, easy, and secure way and grow the business by increasing sales.

## Purpose

Fitster is designed and developed to sell fitness subscriptions and fitness products to customers so that customers can enjoy the benefits of a subscription and purchase products while the business owner can focus on growing the business.

The main purpose of Fitster is to build such a platform for a fitness/gym center that is secure and helps the business owners easily manage their business and the customers to purchase fitness subscriptions and fitness products. The application is designed with an MVC architecture and developed with modern technologies including Python3, Django, HTMX, Bootstrap, HTML5, SCSS, CSS3, Javascript, JQuery, and PostgreSQL to make the application secure, fast and user-friendly.

## Goals

### Project Goals

- Develop a web application to promote fitness classes, subscriptions, and products.
- Implement e-commerce features to sell fitness subscriptions and products to customers.
- Produce a secure and comprehensive backend structure for the application.
- Allow customers to create an account and log in to the application.
- Create an Admin access panel to manage the business and the customers.
- Allow customers to purchase fitness subscriptions and fitness products.
- Implement a payment system(Stripe) to allow customers to pay for their fitness subscriptions and products.
- Allow customers to review fitness products.
- Build a blog to share fitness tips and articles.
- Allow customers to create blog posts to share their success stories.
- Build a contact form to allow customers to contact the business owner.
- Design and develop a user-friendly and responsive website.

### Business Goals

- Increase sales by increasing the number of customers.
- Automate the process of selling fitness subscriptions and fitness products.
- Expand the business by adding more classes and instructors when required.
- Provide better customer service by providing a more personalized experience.
- Provide the best instructors and quality classes to the customers.
- Build a user-friendly and intuitive user interface to make the application more user-friendly.
- Retain customers by providing a better user experience from online shopping.

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

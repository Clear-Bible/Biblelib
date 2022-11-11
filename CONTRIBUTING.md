# Contributing

> Remember that our Lord Jesus said, “More blessings come from giving
> than from receiving.” (Acts 20:35, Contemporary English Version)

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

There are several different ways you can contribute.

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/Clear-Bible/Biblelib/issues .

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement a fix for it.

### Extend or Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

If you find an issue that's not addressed by the documentation, feel
free to flag it (that's really a bug). You're also welcome to submit
improvements.

It's particularly important to acknowledge the work of the many individuals and
organizations that have contributed to Bible metadata standards over
the years. Please let me know if you have any improvements in this
area.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/Clear-Bible/Biblelib/issues .

If you are proposing a new feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Code contributions are always welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `Biblelib` for local
development. Please note this documentation assumes you already have
`poetry` and `Git` installed and ready to go.

1. Fork the `Biblelib` repo on GitHub.

2. Clone your fork locally:
```bash
cd <directory_in_which_repo_should_be_created>
git clone git@github.com:YOUR_NAME/Biblelib.git
```

3. Now we need to install the environment. Navigate into the directory
```bash
cd Biblelib
```

  * If you are using `pyenv`, select a version to use locally. (See installed versions with `pyenv versions`)
```bash
pyenv local <x.y.z>
```
  * Then, install and activate the environment with:
```bash
poetry install
poetry shell
```

4. Install pre-commit to run linters/formatters at commit time:
```bash
poetry run pre-commit install
```

5. Create a branch for local development:
```bash
git checkout -b name-of-your-bugfix-or-feature
```
  * Now you can make your changes locally.

6. Don't forget to add test cases for your added functionality to the ``tests`` directory.
7. When you're done making changes, check that your changes pass the formatting tests.
```bash
make lint
```
8. Now, validate that all unit tests are passing:
```bash
make lint
```
9. Before raising a pull request you should also run tox. This will run the
   tests across different versions of Python:
```bash
tox
```
  * This requires you to have multiple versions of python
    installed. This step is also triggered in the CI/CD pipeline, so
    you could also choose to skip this step locally.
10. Commit your changes and push your branch to GitHub:
```bash
git add .
git commit -m "Your detailed description of your changes."
git push origin name-of-your-bugfix-or-feature
```
11. Submit a pull request through the GitHub website.

Pull Request Guidelines
---------------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.

2. If the pull request adds functionality, the docs should be updated. Put your
   new functionality into a function with a docstring, and add the feature to
   the list in README.rst.

# Contributing Guide

## Branch Strategy
  main - stable release (PR only)
    develop - daily integration
      feature/xxx - new feature
      fix/xxx - bug fix

## Workflow
1. git checkout develop && git pull
2. git checkout -b feature/my-feature
3. Code and commit:
   feat: add bearing animation
   fix: resolve login bug
4. git push -u origin feature/my-feature
5. Create Pull Request to develop on GitHub

## Commit Prefixes
  feat: new feature
  fix: bug fix
  refactor: code refactoring
  docs: documentation
  chore: build/tooling
  test: tests

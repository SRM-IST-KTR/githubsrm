# AWS Lambdas for Project Management

This section of the repository contains 2 AWS lambdas' source codes:

- **`add-contributor`** : Adds a contributor to a team, once their application is accepted by the maintainer.
- **`create-project`** : Once a project is approved, teams are created and maintainers are added to the team. Empty repository is created which the team can access.

## Pre-requisites

- Set up AWS CLI, a lot of scripts in the sub-folders depend on AWS CLI.
- Set up a AWS profile named **'gcsrm'** with appropriate keys and permissions.
- Obtain a GitHub PAT (Personal Access Token) with the minimum permissions:
  - **`repo`**
  - **`admin:org`**
  - **`write:discussion`**

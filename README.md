
fsdjfskajdf

[![Airthings][logo]](https://www.airthings.com)

# terraform-platform-template
Use this repo as a template for platform module repos

[logo]: https://upload.wikimedia.org/wikipedia/commons/d/d1/Airthings_logo.svg

# Testing and Security

We use [tfsec](https://github.com/aquasecurity/tfsec) and [terratest](https://github.com/gruntwork-io/terratest/)
The tools will run automatically on your PRs 🚀.

## Running security analysis
1. `tfsec .`

## Running automated tests against this module
1. Install [Terraform](https://www.terraform.io/) and make sure it's on your `PATH`.
1. Install [Golang](https://golang.org/) and make sure this code is checked out into your `GOPATH`.
1. `cd test`
1. `go get -v -t -d && go mod tidy`
1. `go test -v -run TestExample`

## Update from template

1. `git remote add template git@github.com:Airthings/terraform-platform-template.git`
1. `git fetch --all`
1. `git merge template/[branch to merge] --allow-unrelated-histories`

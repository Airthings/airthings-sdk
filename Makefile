define TITLE
_______  _        _______ _________ _______  _______  _______  _______
(  ____ )( \      (  ___  )\__   __/(  ____ \(  ___  )(  ____ )(       )
| (    )|| (      | (   ) |   ) (   | (    \/| (   ) || (    )|| () () |
| (____)|| |      | (___) |   | |   | (__    | |   | || (____)|| || || |
|  _____)| |      |  ___  |   | |   |  __)   | |   | ||     __)| |(_)| |
| (      | |      | (   ) |   | |   | (      | |   | || (\ (   | |   | |
| )      | (____/\| )   ( |   | |   | )      | (___) || ) \ \__| )   ( |
|/       (_______/|/     \|   )_(   |/       (_______)|/   \__/|/     \|

endef

export TITLE
show-perfect-title: ; @echo "$$TITLE"
init-test:
	cd ./infra/test && go get -v -t -d && go mod tidy

test: show-perfect-title init-test
	cd ./infra/test && go test -v -run TestTerraformHelloWorldExample

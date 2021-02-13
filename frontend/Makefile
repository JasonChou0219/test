INSTALL_DIR = /var/www/html/device-manager-frontend
DIST_DIR = ./dist
NODE_MODULES_DIR = ./node_modules
BUILD_DIR = $(DIST_DIR)/frontend

.PHONY: all
all: build 

.PHONY: install
install: $(BUILD_DIR)
	rm -rf $(INSTALL_DIR)/*
	cp -R $(BUILD_DIR)/* $(INSTALL_DIR)

.PHONY: build
build: 
	npm install
	npm run build-prod

.PHONY: clean
clean:
	rm -rf $(NODE_MODULES_DIR)
	rm -rf $(DIST_DIR)

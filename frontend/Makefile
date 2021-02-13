INSTALL_DIR = /var/www/html/device-manager-frontend
DIST_DIR = ./dist
BUILD_DIR = $(DIST_DIR)/frontend

.PHONY: all
all: install

.PHONY: install
install: build
	rm -rf $(INSTALL_DIR)/*
	cp -R $(BUILD_DIR)/* $(INSTALL_DIR)

.PHONY: build
build: $(BUILD_DIR)

$(BUILD_DIR):
	npm run build-prod

.PHONY: clean
clean:
	rm -rf $(DIST_DIR)

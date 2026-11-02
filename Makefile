SCRIPT := mmatrix.py
INSTALL_DIR := /usr/local/bin
INSTALL_NAME := mmatrix
REPO := https://github.com/miaa-chan/mmatrix
TMP_DIR := $(shell mktemp -d)

.PHONY: all install uninstall update

all:
	@echo "Run 'make install' to install mmatrix."
	@echo "Run 'make update' to update mmatrix."

install:
	@test -f "$(SCRIPT)" || { echo "Error: $(SCRIPT) not found."; exit 1; }
	@echo "Installing mmatrix..."
	@sudo install -m 755 "$(SCRIPT)" "$(INSTALL_DIR)/$(INSTALL_NAME)"
	@echo "Installed successfully. Run '$(INSTALL_NAME)'."

uninstall:
	@echo "Uninstalling mmatrix..."
	@sudo rm -f "$(INSTALL_DIR)/$(INSTALL_NAME)"
	@echo "Uninstalled successfully."

update:
	@set -e
	@tmp=$$(mktemp -d)
	@trap 'rm -rf "$$tmp"' EXIT
	@echo "Updating mmatrix..."
	@git clone --depth 1 "$(REPO)" "$($tmp/repo)"
	@sudo install -m 755 "$(tmp/repo)/$(SCRIPT)" "$(INSTALL_DIR)/$(INSTALL_NAME)"
	@echo "mmatrix updated successfully."


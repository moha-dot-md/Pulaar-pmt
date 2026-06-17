# -------- Settings --------
TARGET = launch.exe
BINDIR = bin
SRCDIR = src
INCDIR = Include
INPUTS = src/inputs
OUTPUTS = src/outputs
PDFS = ../prepare_documents/pdfs

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2 -I$(INCDIR)

SRCS = $(SRCDIR)/main.cpp \
       $(SRCDIR)/Processors.cxx \
       $(SRCDIR)/CWordsHandler.cxx

# -------- OS Detection --------
ifeq ($(OS),Windows_NT)
    RM_FILE = del /f /q
    RM_DIR  = rmdir /s /q
    MK_DIR  = mkdir
else
    RM_FILE = rm -f
    RM_DIR  = rm -rf
    MK_DIR  = mkdir -p
endif

# -------- Build --------
all:
	@echo "Building executable..."
	@$(CXX) $(CXXFLAGS) $(SRCS) -o $(BINDIR)/$(TARGET)
	@echo "Build complete: $(BINDIR)/$(TARGET)"

clean:
	@echo "Cleaning executable..."
	-$(RM_FILE) "$(BINDIR)/$(TARGET)"

# Clean folders for git push
pushing:
	@echo "Cleaning outputs, inputs, and pdfs..."
	-$(RM_DIR) "$(OUTPUTS)"
	-$(RM_DIR) "$(INPUTS)"
	-$(RM_DIR) "$(PDFS)"
	@echo "Recreating folders..."
	@$(MK_DIR) "$(OUTPUTS)"
	@$(MK_DIR) "$(INPUTS)"
	@$(MK_DIR) "$(PDFS)"
	@echo "Folders cleared and ready for git push."

.PHONY: all clean pushing

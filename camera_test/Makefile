##### Make sure all is the first target.
all:

CXX ?= g++
CC  ?= gcc

CFLAGS += -I./src/ -DLINUX_ENABLED  -DUSE_GRALLOC1  -DDISABLE_META_MODE=1 
CFLAGS += -DCAMERA_STORAGE_DIR="\"/data/misc/camera/\"" -I./include
CFLAGS += -g -pthread -Wall 

LDFLAGS += -lcutils -lutils -llog
LDFLAGS += -lhardware
LDFLAGS += -lcamera_metadata
LDFLAGS += -lglib-2.0
LDFLAGS += -ldl
LDFLAGS += -lstdc++
LDFLAGS += -latomic
LDFLAGS += -lpthread
#LDFLAGS += -lomx_encoder
LDFLAGS += -lOmxCore
LDFLAGS += -lcamera_client
LDFLAGS += -lbinder

C_SRC=
CXX_SRC=
OBJ=
DEP=

CXX_SRC+=src/BufferManager.cpp
CXX_SRC+=src/QCameraHAL3Device.cpp
CXX_SRC+=src/QCameraHAL3Base.cpp
CXX_SRC+=src/QCameraHAL3TestSnapshot.cpp
#CXX_SRC+=src/QCameraHALTestMain.cpp
CXX_SRC+=src/QCameraHAL3TestVideo.cpp
CXX_SRC+=src/QCameraTestVideoEncoder.cpp
CXX_SRC+=src/QCameraHAL3TestConfig.cpp
CXX_SRC+=src/QCameraHAL3TestPreview.cpp
CXX_SRC+=src/QCameraHAL3TestTOF.cpp
CXX_SRC+=src/TestLog.cpp
CXX_SRC+=src/OMX_Encoder.cpp
CXX_SRC+=src/BufferManager.cpp

OBJ_CE = src/QCameraHALTestMain.o

hal3_test: $(OBJ_CE)
TARGET_OBJ += $(OBJ_CE)
TARGETS    += hal3_test

include ./common.mk

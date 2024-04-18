import torch
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import sys, os

# Get environment variable 
MAGMA_INSTALL_DIR = os.getenv("MAGMA_INSTALL_DIR")

if "KILONERF_CUDA_ARCHITECTURES" in os.environ and os.environ["KILONERF_CUDA_ARCHITECTURES"]:
	compute_capabilities = [int(x) for x in os.environ["KILONERF_CUDA_ARCHITECTURES"].replace(";", ",").split(",")]
	print(f"Obtained compute capabilities {compute_capabilities} from environment variable KILONERF_CUDA_ARCHITECTURES")
elif torch.cuda.is_available():
	major, minor = torch.cuda.get_device_capability()
	compute_capabilities = [major * 10 + minor]
	print(f"Obtained compute capability {compute_capabilities[0]} from PyTorch")
else:
	raise EnvironmentError("Unknown compute capability. Specify the target compute capabilities in the "
        "KILONERF_CUDA_ARCHITECTURES ""environment variable or install PyTorch with the CUDA backend to detect it automatically.")

min_compute_capability = min(compute_capabilities)
print(f"Minimum Compute Capability: {min_compute_capability}")

# Compile flags
cxx_flags = [
    "-std=c++17"
]
nvcc_flags = [
	"-std=c++17",
    "-Xptxas", 
    "-v,-warn-lmem-usage"
]
nvcc_flags += [f"-gencode=arch=compute_{compute_capability},code={code}_{compute_capability}" for code in ["compute", "sm"] for compute_capability in compute_capabilities]

# Some containers set this to contain old architectures that won"t compile. We only need the one installed in the machine.
os.environ["TORCH_CUDA_ARCH_LIST"] = ""

source_files =     [   
    "fourier_features.cu", 
    "generate_inputs.cu", 
    "global_to_local.cu", 
    "pybind.cu",
    "integrate.cu", 
    "multimatmul.cu", 
    "network_eval.cu", 
    "reorder.cu", 
    "utils.cu",
    "render_to_screen.cpp"
]

extension = CUDAExtension("kilonerf_cuda",
    source_files,
    include_dirs = [
        f"{MAGMA_INSTALL_DIR}/include"
    ],
    libraries = [ "GL", "GLU", "glut", "magma" ],
    library_dirs = [ f"{MAGMA_INSTALL_DIR}/lib" ],
    extra_compile_args = {
        "cxx": cxx_flags, 
        "nvcc": nvcc_flags
    }
)

setup(
    name="kilonerf_cuda",
    ext_modules=[extension],
    cmdclass={
        "build_ext": BuildExtension
    }
)

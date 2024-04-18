from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import os

# get environment variable 
MAGMA_INSTALL_DIR = os.getenv('MAGMA_INSTALL_DIR')

extension = CUDAExtension('kilonerf_cuda',
    ['fourier_features.cu', 'generate_inputs.cu', 'global_to_local.cu', 'pybind.cu',
     'integrate.cu', 'multimatmul.cu', 'network_eval.cu', 'reorder.cu', 'utils.cu',
     'render_to_screen.cpp'],
    include_dirs = [
        f'{MAGMA_INSTALL_DIR}/include'
    ],
    libraries = [ 'GL', 'GLU', 'glut', 'magma' ],
    library_dirs = [ f'{MAGMA_INSTALL_DIR}/lib' ],
    extra_compile_args = {
        'cxx': [], 
        'nvcc': [ '-Xptxas', '-v,-warn-lmem-usage' ]
    }
)

setup(
    name='kilonerf_cuda',
    ext_modules=[extension],
    cmdclass={
        'build_ext': BuildExtension
    }
)

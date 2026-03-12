import numpy as np

def generate_elliptical_source(shape, dx, wavelength, w_x, w_y):
    nx, ny = shape
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(-ny//2, ny//2, ny) * dx
    X, Y = np.meshgrid(x, y)
    E = np.exp(-(X**2 / w_x**2 + Y**2 / w_y**2))
    return E.astype(complex)

def propagate_asm(E_initial, wavelength, z, dx):
    nx, ny = E_initial.shape
    fx = np.fft.fftshift(np.fft.fftfreq(nx, d=dx))
    fy = np.fft.fftshift(np.fft.fftfreq(ny, d=dx))
    FX, FY = np.meshgrid(fx, fy)
    k = 2 * np.pi / wavelength
    kz = np.sqrt(np.complex128(k**2 - (2*np.pi*FX)**2 - (2*np.pi*FY)**2))
    H = np.exp(1j * kz * z)
    obj_fft = np.fft.fftshift(np.fft.fft2(E_initial))
    E_final = np.fft.ifft2(np.fft.ifftshift(obj_fft * H))
    return E_final

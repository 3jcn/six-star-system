import streamlit as st
import pandas as pd
import numpy as np
import lightkurve as lk
from lightkurve import TessTargetPixelFile
from PIL import Image

# author: Thomas Nguyen; June 22, 2021

st.markdown("""
	<style>
	.main{
	background-color: #F0F7F8;
	}
        .stButton>button {
        background-color: #0000ff;
        color: #ffffff;
        }
        .stTextInput>div>div>input {
        background-color: yellow;
        color: brown;
        }
	</style>
	""",
	unsafe_allow_html=True
)

st.title('A Simple Method to Compute the Orbital Periods of the Three Eclipsing Binaries in TIC 168789840 System')

st.write('@author: [Thomas Nguyen](https://www.new3jcn.com)')

st.markdown("""
    A big international team, led by data scientist Brian P. Powell and astrophysicist Veselin Kostov wrote
    the paper, **"TIC 168789840: A Sextuply-Eclipsing Sextuple Star System"**. It's published on The Astronomical Journal website in April 2021.
    
    **The Paper:** [Open pdf file](https://arxiv.org/pdf/2101.03433.pdf)  

    By using a high-performance computing: 129,000-core Discover supercomputer at the NASA Center for Climate
    Simulation at NASA GSFC, the team discovered three eclipsing binaries from TESS data. 
    Each eclipse causes a dip in the system’s overall brightness. Astronomers designate the binaries by the letters A, B, and C. 
    The stars in the A and C systems orbit each other roughly every day and a half, and the two binaries orbit each other 
    about every four years. The B binary’s members circle each other about every eight days, but the pair is much farther away, 
    orbiting around the inner systems roughly every 2,000 years. 
    The orbial periods of the three eclipsing binaries are shown in the following photo (from NASA's Goddard Space Flight Center):
    """)

image = Image.open('TYC_7037-89-1.jpg')
st.image(image,use_column_width=True)

st.markdown("""
    In this project, I employed a simple Python/Lightkurve code and was able to obtain the orbital periods for the three eclipsing binaries A, B, and C from TESS data.    

    **Data source from:** [MAST: Barbara A. Mikulski Archive for Space Telescopes](https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html)  

    """)

st.set_option('deprecation.showPyplotGlobalUse', False)

tpf = TessTargetPixelFile("tess2020294194027-s0031-0000000168789840-0198-s_tp.fits")
tpf
if st.button('Show TessTargetPixelFile Metadata'):
    st.write(tpf.get_header(ext=0))

aperture_mask = tpf.create_threshold_mask(threshold=10)
lc = tpf.to_lightcurve(aperture_mask=aperture_mask)

if st.button('Show TESSLightCurve object data:'):
    lc 

st.write("First frame in the pixel file (the first observation cadence in the Sector):")
tpf.plot(aperture_mask=tpf.pipeline_mask)
st.pyplot()

st.write("TESS lightcurve of TIC 168789840 in sector 31 (Plot 1):")
lc = lc.remove_outliers(sigma=6)
lc.scatter()
st.pyplot()

st.write("Apply the 'Box Least Squares' (BLS) method for identifying transit signals (Plot 2):")
lc2 = lc.remove_nans().flatten(window_length=401)

periodogram = lc2.to_periodogram(method="bls",period=np.arange(0.5,10,0.001))
periodogram.plot()
st.pyplot()
st.write("From the above graph, the best period can be found at:")
p1 = periodogram.period_at_max_power
p1
st.write("Fold the lightcurve with this specific period, we can see the dip (3.5%) in the overall brightness of the system as follows:")
lc2.fold(period=p1).bin(time_bin_size=0.005).plot(label='Binary A')
st.pyplot()

st.write("Also from Plot 2, the second best period is:")
periodogram2 = lc2.to_periodogram(method="bls",period=np.arange(8.2,8.27,0.001))
p2 = periodogram2.period_at_max_power
p2
st.write("Fold the lightcurve with this period, we can see the dip (5.5%) as follows:")
lc2.fold(period=p2).bin(time_bin_size=0.007).plot(label='Binary B')
st.pyplot()

st.write("And this is lightcurve phase-folded (1.5% dip) with period of:")
periodogram3 = lc2.to_periodogram(method="bls",period=np.arange(1.29,1.32,0.001))
p3 = periodogram3.period_at_max_power
p3
lc2.fold(period=p3).bin(time_bin_size=0.003).plot(label='Binary C')
st.pyplot()

st.write("Let's compare the above results with the results from ASAS-SN & WASP (Powell at el.)") 
image = Image.open('compare.png')
st.image(image,use_column_width=True)

st.subheader("Conclusion:")
st.markdown("""
    With several lines of python code & LightKurve package ran on an i3 laptop, the periods of the three eclipsing binaries 
    in TIC 168789840 system were able to obtain.  \nAccording to Powell at el., the primary stars in the binaries have masses 
    between 1.23 and 1.3 times that of the Sun and radii between 1.46 and 1.69 solar radii, 
    and the secondary stars have masses and radii of 0.56-0.66 solar masses and 0.52-0.62 solar radii.  \nBecause binary B caused 
    more dip (55%) than binaries A and C on the overall brightness of the system, I can conclude that the primary star in binary B
    has the biggest size in the system.
    """)

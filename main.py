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

from lightkurve import TessTargetPixelFile
import lightkurve as lk
from astropy.io import fits
import pandas as pd
st.set_option('deprecation.showPyplotGlobalUse', False)

tpf = TessTargetPixelFile("tess2020294194027-s0031-0000000168789840-0198-s_tp.fits")
tpf

aperture_mask = tpf.create_threshold_mask(threshold=10)
lc = tpf.to_lightcurve(aperture_mask=aperture_mask)

if st.button('Show TESS pixel data:'):
    lc 

st.write("First frame in the pixel file:")
tpf.plot(aperture_mask=tpf.pipeline_mask)
st.pyplot()

st.write("TESS lightcurve of TIC 168789840 in sector 31 (Plot 1):")
lc = lc.remove_outliers(sigma=6)
lc.scatter()
st.pyplot()

st.write("Apply the 'Box Least Squares' (BLS) method for identifying transit signals (Plot 2):")
import numpy as np
periodogram = lc.remove_nans().flatten(window_length=401).to_periodogram(method="bls",period=np.arange(0.5,10,0.001))
periodogram.plot()
st.pyplot()
st.write("From the above graph, by using 'period_at_max_power' method, the best period can be found:")
periodogram.period_at_max_power
 
st.write("Fold the lightcurve with this specific period, we can see the dip (35%) in the overall brightness of the system as follows:")
lc.remove_nans().flatten(window_length=1001).fold(period=1.57).bin(binsize=15).plot(label='Binary A')
st.pyplot()

st.write("Also from Plot 2, we can get the second best period is 8.215, fold the lightcurve with this period, we can see the dip (55%) as follows:")
lc.remove_nans().flatten(window_length=401).fold(period=8.217).bin(binsize=15).plot(label='Binary B')
st.pyplot()

st.write("And this is lightcurve folded with period of 1.306 (15% dip):")
lc.remove_nans().flatten(window_length=1001).fold(period=1.306).bin(binsize=15).plot(label='Binary C')
st.pyplot()

st.write("Let's compare the above results with the results from ASAS-SN & WASP (Powell at el.)") 
image = Image.open('compare.png')
st.image(image,use_column_width=True)

st.subheader("Final Thoughts:")
st.markdown("""
    With several lines of python code & LightKurve library ran on an i3 laptop, the periods of the three eclipsing binaries 
    in TIC 168789840 system were able to obtain. According to Powell at el., the primary stars in the binaries have masses 
    between 1.23 and 1.3 times that of the Sun and radii between 1.46 and 1.69 solar radii, 
    and the secondary stars have masses and radii of 0.56-0.66 solar masses and 0.52-0.62 solar radii. That information makes me wonder why
    binary B caused a bigger effect (55%) than binaries A and C on the overall brightness of the system?
    """)

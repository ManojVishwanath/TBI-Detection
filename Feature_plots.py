# import lib
import numpy as np
import mne
from scipy import signal
import matplotlib.pyplot as plt
import scipy
from Frequency_filtering import filt


def plots(sub,data,data2,p):
    """plots 5 figures (EEG after ICA, Filtering, band power, phase amplitude asymmetry)

    Args:
        sub (_type_): _description_
        data (_type_): _description_
        data2 (_type_): _description_
        p (dictionary): contains all parameters of the dataset
    """
    
    #=========================================================================================================
    
    raw = mne.io.read_raw_edf(p['data_folder']+'\\'+sub+".edf", preload=True)
    raw2=raw[:,:][0]
    raw2=raw2-(np.mean(raw2,axis=1).reshape(np.shape(raw2)[0],1))
    raw1 = mne.io.read_raw_fif(p['data_folder']+'\\'+sub+'_ica'+".fif", preload=True)
    raw3=raw1[:,:][0]
    raw3=raw3-(np.mean(raw3,axis=1).reshape(np.shape(raw3)[0],1))
    sos = signal.butter(6, [0.5,50], 'bp', fs=200, output='sos')
    filtered1 = signal.sosfilt(sos,raw2[raw.ch_names.index('O2-A1'),6356*200:6359*200] )
    filtered2 = signal.sosfilt(sos,raw2[raw.ch_names.index('ECG'),6356*200:6359*200] )
    filtered3 = signal.sosfilt(sos,raw3[raw1.ch_names.index('O2'),6356*200:6359*200] )

    fig = plt.figure()
    #fig.subplots_adjust(top=0.5)
    ax1 = fig.add_subplot(311)
    ax1.set_ylabel('\u03BC volts')
    ax1.set_title('EEG')

    t = np.arange(0,3,1/200)
    s = filtered1*10**6
    line, = ax1.plot(t, s, lw=1)
    ax1.set_xlabel('time (s)')

    ax2 = fig.add_subplot(312)
    #ax2 = fig.add_axes([0.2, 0.1, 0.7, 0.3])
    ax2.set_ylabel('\u03BC volts')
    ax2.set_title('ECG')

    #t = np.arange(0,3,1/200)
    s = filtered2*10**6
    line, = ax2.plot(t, s, color='r',lw=1,)
    ax2.set_xlabel('time (s)')

    ax3 = fig.add_subplot(313)
    #ax2 = fig.add_axes([0.2, 0.1, 0.7, 0.3])
    ax3.set_ylabel('\u03BC volts')
    ax3.set_title('EEG after ICA')

    #t = np.arange(0,3,1/200)
    s = filtered3*10**6
    line, = ax3.plot(t, filtered1*10**6,lw=1,)
    line, = ax3.plot(t, s,lw=1,)
    ax3.set_xlabel('time (s)')
    plt.tight_layout()
    plt.show()
  
    
    #=========================================================================================================
    
    
    fig = plt.figure()

    yf = scipy.fftpack.fft(data2)

    N=len(yf)
    T=1/200
    xf = np.linspace(0.0, 1.0/(2.0*T), int(N/2))

    sos = signal.butter(6, [0.5,50], 'bp', fs=200, output='sos')
    y = signal.sosfilt(sos,data2 )
    yf1 = scipy.fftpack.fft(y)

    yf2 = scipy.fftpack.fft(data)

    ax2 = fig.add_subplot(211)
    ax2.set_ylabel('Amplitude (\u03BCV)')
    ax2.set_title('Time-domain signal')
    line0, = ax2.plot( data2[500:600], lw=1,label='No filtering')
    line1, = ax2.plot( y[500:600], lw=1,label='Butterworth filtering')
    line2, = ax2.plot(data[500:600], lw=1,label='Frequeny filtering')
    ax2.set_xlabel('Time')
    plt.legend(loc='upper right')
    plt.tight_layout()


    ax2 = fig.add_subplot(212)
    ax2.set_ylabel('dB (log10)')
    ax2.set_title('FFT plot')

    line0, = ax2.plot(xf, np.log10(2.0/N * np.abs(yf[:N//2])),lw=1,label='No filtering')
    line1, = ax2.plot(xf, np.log10(2.0/N * np.abs(yf1[:N//2])),lw=1,label='Butterworth filtering')
    line2, = ax2.plot(xf, np.log10(2.0/N * np.abs(yf2[:N//2])),lw=1,label='Frequeny filtering')
    ax2.set_xlabel('Frequency (Hz)')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()


    #=========================================================================================================

    win=4*p['fs']
    freqs,psd=signal.welch(data,p['fs'],nperseg=win)

    # Define delta lower and upper limits
    low, high = 0.5, 4
    idx_delta = np.logical_and(freqs >= low, freqs <= high)

    # Plot the power spectral density and fill the delta area
    plt.figure(figsize=(7, 4))
    plt.plot(freqs, psd, lw=0.5, color='k')
    plt.fill_between(freqs, psd, where=idx_delta, color='skyblue',label='Delta')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('PSD (\u03BCv^2 / Hz)')
    plt.xlim([0, 25])
    plt.ylim([0, psd.max() * 1.1])
    plt.title("Welch's periodogram")

    low, high = 4, 8
    idx_delta = np.logical_and(freqs >= low, freqs <= high)
    plt.fill_between(freqs, psd, where=idx_delta, color='orange',label='Theta')

    low, high = 8,12
    idx_delta = np.logical_and(freqs >= low, freqs <= high)
    plt.fill_between(freqs, psd, where=idx_delta, color='green',label='Alpha')

    low, high = 12,16
    idx_delta = np.logical_and(freqs >= low, freqs <= high)
    plt.fill_between(freqs, psd, where=idx_delta, color='red',label='Sigma')
    
    low, high = 16,25
    idx_delta = np.logical_and(freqs >= low, freqs <= high)
    plt.fill_between(freqs, psd, where=idx_delta, color='yellow',label='Gama')
    
    plt.legend()
    plt.tight_layout()
    
    #=========================================================================================================                    
    
    data = data[1000:1500]
    x1=filt(data,p,3.5,4,8,8.5)
    x2=filt(data,p,24.5,25,40,40.5)

    analytic_signal = signal.hilbert(x2)
    amplitude_envelope = np.abs(analytic_signal)

    y1 = x2
    N=len(y1)
    T=1/200
    x = np.linspace(0.0, N*T, N)

    f1,ax = plt.subplots(2,1)
    ax[0].plot(x,y1, linewidth=1,label='Gama Filtered EEG')
    ax[0].set(xlim=[0,N*T],ylim=[min(y1)-0.1,max(y1)+2])
    ax[0].set_ylabel('\u03BC volts')
    ax[0].set_xlabel('time (s)')

    phase_x1=(np.angle(signal.hilbert(x1),deg=True))+150
    ax[0].plot(x,amplitude_envelope, linewidth=1,label='Amplitude Envelope')
    ax[0].legend(loc="upper left")

    y1=data
    ax[1].plot(x,y1, linewidth=1,label='Raw EEG')
    ax[1].set(xlim=[0,N*T])
    ax[1].set_ylabel('\u03BC volts')
    ax[1].set_xlabel('time (s)')
    ax[1].set_title('Raw EEG')

    #ax[2].set_visible(False)
    plt.tight_layout()
    plt.show()

    y1 = x1
    N=len(y1)
    T=1/200
    x = np.linspace(0.0, N*T, N)

    f,ax1 = plt.subplots(figsize=(6.4,2))
    ax1.plot(x,y1, linewidth=1,label='Theta Filtered EEG')
    ax1.set(xlim=[0,N*T],ylim=[min(y1)-5,max(y1)+10])
    ax1.set_ylabel('\u03BC volts')
    ax1.set_xlabel('time (s)')
    ax1.legend(loc="upper left")

    phase_x1=(np.angle(signal.hilbert(x1),deg=True))+150
    ax2=ax1.twinx()
    ax2.plot(x,phase_x1,color='r', linewidth=1,label='Phase')
    ax2.set(ylim=[min(phase_x1)-5,max(phase_x1)+100])
    ax2.set_ylabel('Phase (degree)')
    ax2.set_xlabel('time (s)')
    ax2.legend(loc="upper center")
    #ax[1].set(title='Angle at each Timepoint')

    
    rates = amplitude_envelope
    zenith_angles = phase_x1
    zen_bins = np.linspace(0, 360, 20)
    norm_binned_zen = [np.mean(rates[np.where((zenith_angles > low) & (zenith_angles <= high))]) for low, high in zip(zen_bins[:-1], zen_bins[1:])]
    norm_binned_zen=norm_binned_zen/np.sum(norm_binned_zen[:-1])
    plt.figure()
    x_pos = np.arange(1,len(norm_binned_zen[:-1])*2,2)
    #f, ax = plt.subplots(figsize=(11, 9))
    plt.bar(x_pos,norm_binned_zen[:-1],width=1.5)
    x_pos = np.arange(0,len(norm_binned_zen[:-1])*2+2,2)
    zen_bins = np.linspace(0, 360, 19)
    plt.xticks(x_pos,zen_bins,rotation=90)
    plt.xlim([0,x_pos[-1]])
    plt.ylim([0,0.1])
    plt.xlabel('Phase (degree)')
    plt.ylabel('Normalized Mean Amplitude')
    plt.tight_layout()
    
    #=========================================================================================================                    

    filename='Sounds/E.wav'
    sP.fb = 329.6275569129; % base frequency. NaN: random
    sP.ratio = 2; % the frequency ratio between components (2 is Shepard) 
    sP.freqmin = 20; % minimum frequency
    sP.freqmax = 20000; % maximum frequency
    sP.sigma = 1; % sigma for the Gaussian envelope. NaN: no envelope
    sP.tonedur = 0.500;   % tone duration (s)
    sP.noiseSNR = -50;
    sP.ramptime = 0.005;  % ramp time (s)
    sP.rmsfact = 4;
    sP.fs = 44100; % sampling frequency
    
    
    
    newfreq=sP.fb;
    ok=1;
    freqs=sP.fb;
    while ok
        newfreq = newfreq*sP.ratio;
        if newfreq > sP.freqmax
            ok = 0;
        else
            freqs = [freqs newfreq];
        end
    end
    % next add as many frequencies as possible below fb
    newfreq=sP.fb;
    ok=1;
    while ok
        newfreq = newfreq/sP.ratio;
        if newfreq < sP.freqmin
            ok = 0;
        else
            freqs = [newfreq freqs];
        end
    end
    
    fc = sqrt(sP.freqmin*sP.freqmax); % centre frequency of the Gaussian at the geometric mean between min and max
    a = exp(-0.5*(log(freqs/fc)/log(2)/sP.sigma).^2);
    
    
    xt = dosynth(freqs,a,zeros(size(freqs)),sP.tonedur,sP.fs);
    xt = ramp(xt,sP.ramptime,sP.fs);
    xt = xt/rms(xt)/sP.rmsfact;
    
    if sP.noiseSNR > -99
    n = pinknoise2(length(xt),sP.freqmin,sP.freqmax*2,3);
    n = ramp(n,sP.ramptime,sP.fs);
    n = n/rms(n)*10^(sP.noiseSNR/20);    
    xt = xt(1,:)+n ;
    end
    
    audiowrite(filename,xt,sP.fs)
    %soundsc(xt,sP.fs)
    
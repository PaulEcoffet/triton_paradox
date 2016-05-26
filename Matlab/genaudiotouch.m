function [x,sP] = genaudiotouch(sP,sigint);

if nargin == 0
    sP.fb = NaN; % base frequency. NaN: random
    sP.ratio = 2; % the frequency ratio between components (2 is Shepard) 
    sP.freqmin = 20; % minimum frequency
    sP.freqmax = 20000; % maximum frequency
    sP.sigma = 1; % sigma for the Gaussian envelope. NaN: no envelope
    sP.biascond = 10; % biasing condition. -N: bias down; 0: no context; +N: bias up
    sP.seqint = NaN; % will be filled by gen: intervals to play
    sP.istest = NaN; % will be filled by gen: is it a test tone
    sP.tonedur = 0.330;   % tone duration (s)
    sP.intertonegap = 0.125; % silence during context (s)
    sP.switchgap = 0.50;     % silence during test (s)
    sP.noiseSNR = -50;
    sP.ramptime = 0.005;  % ramp time (s)
    sP.rmsfact = 20;
    sP.fs = 44100; % sampling frequency
end

% get confused
rng('shuffle');

% build the frequency sequence
% first, base frequency
if isnan(sP.fb)
    sP.fb = sP.freqmin+rand(1)*sP.freqmin*sP.ratio;
end

% now the various context intervals
% interval is like musical interval: ratio^(interval/12), so 12 for an
% 'octave' and 6 for 'tritone'
idx = 0;
for icontext = 1:1:abs(sP.biascond)
    idx = idx+1;
    sP.seqint(idx) = 6-rand(1)*6*sign(sP.biascond);
    sP.istest(idx) = 0;
end

% test pair
idx = idx+1;
sP.seqint(idx) = 0;
sP.istest(idx) = 1;
idx = idx+1;
sP.seqint(idx) = 6;
sP.istest(idx) = 2;

% now do the sound synthesis. Big loop
xintertonegap = zeros(2,round(sP.intertonegap*sP.fs));
xswitchgap =  zeros(2,round(sP.switchgap*sP.fs));

x = [];
for iseq = 1:1:length(sP.seqint)
    % first find the appropriate frequencies. 
    freqs = [sP.fb*sP.ratio^(sP.seqint(iseq)/12)]; 
    % add as many frequencies as possible above fb
    ok = 1;
    while ok
        newfreq = freqs(end)*sP.ratio;
        if newfreq > sP.freqmax
            ok = 0;
        else
            freqs = [freqs newfreq];
        end
    end
    % next add as many frequencies as possible below fb
    ok = 1;
    while ok
        newfreq = freqs(1)/sP.ratio;
        if newfreq < sP.freqmin
            ok = 0;
        else
            freqs = [newfreq freqs];
        end
    end
    % now the amplitude envelope
    if isnan(sP.sigma)
        a = ones(size(freqs));
    else
        fc = sqrt(sP.freqmin*sP.freqmax); % centre frequency of the Gaussian at the geometric mean between min and max
        a = exp(-0.5*(log(freqs/fc)/log(2)/sP.sigma).^2);
    end
    
    % generate the sound
    xt = dosynth(freqs,a,zeros(size(freqs)),sP.tonedur,sP.fs);
    xt = ramp(xt,sP.ramptime,sP.fs);
    xt = xt/rms(xt)/sP.rmsfact;
    
    % assign to correct channel
    if sP.istest(iseq) == 0; % context
        xtstereo = [xt*0;xt/max(abs(xt))];
    else
        xtstereo = [xt;xt*0];
    end        
    
    if (sP.istest(iseq) == 1) & (sP.biascond ~= 0)
        x = [x, xswitchgap, xtstereo];
    else
        x = [x, xintertonegap, xtstereo];
    end
end
x = [x xintertonegap]; % finish with a silence too

% now add noise if needed
if sP.noiseSNR > -99
    n = pinknoise2(length(x),sP.freqmin,sP.freqmax*2,3);
    n = ramp(n,sP.ramptime,sP.fs);
    n = n/rms(n)*10^(sP.noiseSNR/20);    
    x = [x(1,:)+n ; x(2,:)];
end
        
x = x'; % right shape

if max(abs(x))>0.9999
    error('clipped')
end
%soundsc(x,sP.fs)

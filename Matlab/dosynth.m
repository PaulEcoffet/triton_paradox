function [x] = dosynth(freqs,amps,phase,d,fs);

t = [0:1/fs:d-1/fs];
x = zeros(size(t));
for i = 1:1:length(freqs);
	x = x+amps(i)*cos(2*pi*freqs(i)*t+phase(i));
end


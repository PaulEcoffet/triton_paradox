function [r] = rms(x)

if size(x,1)>size(x,2)
  x = x';
end

if size(x,1) == 1
  r = sqrt(x*x'/size(x,2));
else
  r(1) = sqrt(x(1,:)*x(1,:)'/size(x,2));
  r(2) = sqrt(x(2,:)*x(2,:)'/size(x,2));
end

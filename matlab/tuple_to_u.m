%this function will transform tuple to u (0.6,0.1,0.1)=>6
function y = tuple_to_u(x)
u = sscanf(x,'(%f,%f,%f)');
y = num2str(u(1)*10);
end
c={};
names={};
counter = 1;
for i = [1:length(satdata)]
    if (i~=1 && ((etime(str_to_time(satdata{i,7}),str_to_time(satdata{i,8})))/31556926 < 25.0))
    %id
    %c{i,1} = satdata{i,6};
    %name
    names{counter,1} = strcat(tuple_to_u(satdata{i,2}),'U');
    %time
    if i ~= 1 
        c{counter,1} = (etime(str_to_time(satdata{i,7}),str_to_time(satdata{i,8})))/31556926;
    else
        c{counter,1} = (0.010951637051087);
    end
    %u
    %c{i,4} = tuple_to_u(satdata{i,2});
    %dragArea
    c{counter,2} = satdata{i,3};
    %reflectingArea
    c{counter,3} = satdata{i,4};
    %semiMajor
    c{counter,4} = satdata{i,9};
    %eccentricity
    c{counter,5} = satdata{i,10};
    %inclination
    c{counter,6} = rad2deg(satdata{i,11});
    %mass
    c{counter,7} = satdata{i,1};
    counter = counter + 1;
    end
end
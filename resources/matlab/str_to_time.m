function y = str_to_time(x)
date_str = sscanf(x,'%d-%d-%d');
date_str_cocat = strcat(num2str(date_str(3)),'-',num2str(date_str(2)),'-',num2str(date_str(1)));
formatIn = 'dd-mm-yy';
y = datevec(date_str_cocat,formatIn);
end
%ploter functions
main;
A= cell2mat(c);
labels = {'time','drag area','reflect area','height','ecc','incl','u'};
parallelcoords(A,'group',names,'labels',labels);